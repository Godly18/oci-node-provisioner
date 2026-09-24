import oci
import os
import time
from dotenv import load_dotenv

load_dotenv()

# Setup configuration from environment variables
config = {
    "user": os.getenv("OCI_USER_ID"),
    "key_content": os.getenv("OCI_PRIVATE_KEY"),
    "fingerprint": os.getenv("OCI_FINGERPRINT"),
    "tenancy": os.getenv("OCI_TENANCY_ID"),
    "region": os.getenv("OCI_REGION")
}

try:
    compute_client = oci.core.ComputeClient(config)
    print("OCI Authentication Successful. Initializing loop sequence...")
except Exception as e:
    print(f"Authentication Failed: {e}")
    exit(1)

# Execution parameters
compartment_id = os.getenv("OCI_TENANCY_ID")
subnet_id = os.getenv("OCI_SUBNET_ID")
image_id = os.getenv("OCI_IMAGE_ID")
public_ssh_key = os.getenv("OCI_PUBLIC_SSH_KEY") 

# SAFETY CHECK: Verify the key actually loaded from GitHub Secrets
if not public_ssh_key or public_ssh_key.strip() == "":
    print("CRITICAL ERROR: OCI_PUBLIC_SSH_KEY is empty or missing from your secrets!")
    exit(1)

# Availability Domains to cycle through
ads = ["uufj:PHX-AD-1", "uufj:PHX-AD-2", "uufj:PHX-AD-3"]

total_attempts = 60 

for i in range(1, total_attempts + 1):
    current_ad = ads[(i - 1) % len(ads)]
    print(f"[Attempt {i}/{total_attempts}] Requesting instance in {current_ad}...")
    
    try:
        request = oci.core.models.LaunchInstanceDetails(
            display_name="FX-Backend-Server",
            compartment_id=compartment_id,
            availability_domain=current_ad,
            shape="VM.Standard.A1.Flex",
            shape_config=oci.core.models.LaunchInstanceShapeConfigDetails(
                ocpus=2,
                memory_in_gbs=12
            ),
            source_details=oci.core.models.InstanceSourceViaImageDetails(
                source_type="image",
                image_id=image_id,
                boot_volume_size_in_gbs=100
            ),
            create_vnic_details=oci.core.models.CreateVnicDetails(
                subnet_id=subnet_id,
                assign_public_ip=True,
                assign_private_dns_record=True,
                display_name="forexalertsvnic"
            ),
            metadata={
                "ssh_authorized_keys": str(public_ssh_key).strip()
            }
        )
        
        response = compute_client.launch_instance(request)
        if response.status == 200:
            print("SUCCESS! Authorized Server creation initialized perfectly.")
            exit(0)
            
    except oci.exceptions.ServiceError as e:
        if "Out of host capacity" in str(e) or e.status == 500:
            print(f"-> Capacity Unavailable. Resting 60 seconds...")
        else:
            print(f"-> API Error: {e.message}")
            
    if i < total_attempts:
        time.sleep(60)
