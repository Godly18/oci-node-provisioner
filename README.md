# OCI Ampere A1 Node Provisioner

An automated, lightweight Python and GitHub Actions engine designed to continuously request and provision an 
**Oracle Cloud Infrastructure (OCI) Always Free Ampere A1 Compute Instance** (`VM.Standard.A1.Flex` with 2 vCPUs and 12 GB RAM) 
across multiple Availability Domains.

---

## Default Image Details

This repository is configured to deploy **Ubuntu 24.04 LTS (aarch64)**.

* **Region:** `us-phoenix-1` (Phoenix) - you can change your region to whichever you like

* **Architecture:** ARM64 (`aarch64`)

* **OS:** Canonical Ubuntu Server 24.04 LTS

* **Default Image OCID:**
  ```text
  ocid1.image.oc1.phx.aaaaaaaagrsiqy75p2vblxtrqn7ttjyafrzronnu7sfaibu6pfz6y2beeb2q
