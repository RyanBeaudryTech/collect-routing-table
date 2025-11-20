# Network Automation Lab – Routing Table Collector

This project is part of my ongoing network automation lab built using Cisco Modeling Labs (CML).  
The goal of this script is to connect to multiple Cisco routers, run the `show ip route` command, and save each router’s routing table to its own text file.

This project demonstrates:

- Secure SSH access to multiple routers
- Using a YAML inventory file to define device details
- Looping through devices and handling per-device exceptions
- Writing structured output to files
- Practical Netmiko usage in a real lab topology

---

## Features

- Connects to any number of routers using data from a `routers.yaml` file  
- Supports devices using different ports (e.g., port-forwarded devices from CML)  
- Automatically names output files based on the router hostname  
- Gracefully handles authentication or connection failures  
- Designed for expansion into more advanced automation tasks  
- Fully compatible with CML virtual labs

---

## Lab Topology

This script was tested in a CML environment with:

- A NAT/gateway router connected to my home LAN  
- Multiple internal routers accessed through SSH port forwarding  
- YAML-based inventory storing hostname, IP, and SSH port

> A diagram of this topology can be found in the `topology/` directory.

---


