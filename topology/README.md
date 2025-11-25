# Network Automation Lab – OSPF Multisite Topology

This repository contains a lab environment built in Cisco Modeling Labs (CML) focused on collecting routing tables programmatically from a multi-site OSPF network. The topology simulates multiple interconnected sites, each running OSPF, and includes a NAT gateway connected to a real home network.

---

## Topology Overview

The lab represents a **multi-site OSPF environment**, where:

- Each “site” is an OSPF area
- The WAN area is **Area 0**
- **Area 3** does *not* directly connect to the backbone, so an **OSPF Virtual Link** is used through Area 2
- R1 serves as the **NAT Gateway** between CML and the home LAN
- All routers authenticate via **RADIUS** (FreeRADIUS running on an Ubuntu VM)

The topology includes:

- **7 Cisco routers** (R1–R7)
- **3 PCs** (Alpine Linux VMs inside CML)
- **Structured OSPF area design**
- **NAT + port-forwarding** for external SSH access
- **Centralized RADIUS authentication**

A full visual diagram can be found in:  
`/topology/network-topology.png`

---

### **OSPF Virtual-Link**
Since **Area 3 does not touch Area 0**, an OSPF virtual-link is configured:

- Backbone router: **R4**
- Remote router: **R6**
- Transit area: **Area 2**

This restores backbone connectivity for LSAs originating in Area 3.

---

## NAT Gateway + Port Forwarding (R1)

R1 acts as the gateway between CML and the home LAN.

### **Functions of NAT Gateway (R1)**
- Provides **Internet access** to all routers via NAT  
- Exposes internal CML devices externally via **port forwarding**  
- Allows Python automation scripts running on the host PC to SSH into each router through unique ports

### **SSH Port-Forwarding Scheme**
Each router listens on port **222(R#)** on the home LAN:

| Router | CML Mgmt IP | External SSH Port |
|--------|--------------|------------------|
| R2 | 192.168.1.145 | **2222** |
| R3 | 192.168.1.145 | **2223** |
| R4 | 192.168.1.145 | **2224** |
| R5 | 192.168.1.145 | **2225** |
| R6 | 192.168.1.145 | **2226** |
| R7 | 192.168.1.145 | **2227** |

R1 forwards `TCP/222X → TCP/22` of the appropriate CML router.

### **RADIUS Forwarding**
R1 also forwards RADIUS traffic to the FreeRADIUS VM:

- **UDP/1812 & UDP/1813** → Ubuntu VM running FreeRADIUS

This enables centralized AAA across all routers in the lab.

## R1 NAT Configuration
<pre>
ip nat inside source static tcp 10.3.67.7 22 interface GigabitEthernet4 2227
ip nat inside source static tcp 10.2.46.6 22 interface GigabitEthernet4 2226
ip nat inside source static tcp 10.0.34.4 22 interface GigabitEthernet4 2224
ip nat inside source static tcp 10.1.35.3 22 interface GigabitEthernet4 2225
ip nat inside source static udp 192.168.1.88 1813 interface GigabitEthernet4 1813
ip nat inside source static udp 192.168.1.88 1812 interface GigabitEthernet4 1812
ip nat inside source static tcp 10.0.12.2 22 interface GigabitEthernet4 2222
ip nat inside source static tcp 10.0.13.3 22 interface GigabitEthernet4 2223
ip nat inside source list 1 interface GigabitEthernet4 overload
!
!
ip access-list standard 1
 10 permit 10.0.0.0 0.255.255.255
</pre>
---

## RADIUS and Remote Access Configuration
<pre>
aaa new-model
aaa authentication login LOGIN group radius local

radius server FREERADIUS
 address ipv4 192.168.1.88 auth-port 1812 acct-port 1813
 key mysecret


line vty 0 4
 exec-timeout 0 0
 privilege level 15
 login authentication LOGIN
 transport input ssh
</pre>

### **How it integrates**
- Each Cisco router is configured with:
  - RADIUS server pointing to the home PC
  - Shared secret
  - Login authentication using RADIUS first, local fallback second



