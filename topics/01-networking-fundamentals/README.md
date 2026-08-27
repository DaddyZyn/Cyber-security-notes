# 🌐 Module 01: Networking Fundamentals — IPs, Subnets, Gateways & DNS

Understanding how data moves across Layer 2 and Layer 3 of the OSI model is mandatory before discussing operational security, privacy, or tracking. If you do not understand packet routing and address resolution, you cannot properly conceal your network footprint.

---

## 📑 Table of Contents
- [1. Public vs. Private IP Addresses](#1-public-vs-private-ip-addresses)
  - [1.1 The Core Difference](#11-the-core-difference)
  - [1.2 RFC 1918 Private Address Ranges](#12-rfc-1918-private-address-ranges)
  - [1.3 NAT (Network Address Translation)](#13-nat-network-address-translation)
- [2. IPv4 vs. IPv6 & The Dual-Stack Trap](#2-ipv4-vs-ipv6--the-dual-stack-trap)
  - [2.1 Technical Comparison](#21-technical-comparison)
  - [2.2 The IPv6 Privacy & Tracking Nightmare](#22-the-ipv6-privacy--tracking-nightmare)
- [3. Subnets, Subnet Masks, & Default Gateways](#3-subnets-subnet-masks--default-gateways)
  - [3.1 Subnets & CIDR Notation](#31-subnets--cidr-notation)
  - [3.2 The Default Gateway & Packet Forwarding](#32-the-default-gateway--packet-forwarding)
- [4. DNS (Domain Name System) Mechanics & Leaks](#4-dns-domain-name-system-mechanics--leaks)
  - [4.1 How Resolution Works](#41-how-resolution-works)
  - [4.2 Why Plaintext DNS Destroys Anonymity](#42-why-plaintext-dns-destroys-anonymity)
  - [4.3 Encrypted DNS Protocols (DoH / DoT)](#43-encrypted-dns-protocols-doh--dot)
  - [4.4 DNS Leaks Under VPNs](#44-dns-leaks-under-vpns)

---

## 1. Public vs. Private IP Addresses

### 1.1 The Core Difference
* **Public IP**: A globally unique IP address assigned to your router/modem by your Internet Service Provider (ISP). Every machine directly communicating across the public internet uses public IPs.
* **Private IP**: Non-routable IP addresses reserved exclusively for local area networks (LAN). They sit behind a router and cannot be contacted directly from the wider internet without port forwarding or tunneling.

```
[ Your PC: 192.168.1.50 ] ---\
[ Phone:   192.168.1.51 ] ----+--> [ Router/Gateway: 192.168.1.1 ] ---> [ Public Internet: 203.0.113.42 ]
[ Laptop:  192.168.1.52 ] ---/          (NAT Translation)
```

### 1.2 RFC 1918 Private Address Ranges
These address blocks are reserved for private internal subnets:

| Class | IP Range | CIDR Prefix | Typical Use Case |
| :--- | :--- | :--- | :--- |
| **Class A** | `10.0.0.0` – `10.255.255.255` | `10.0.0.0/8` | Large enterprise networks, data centers, VPN subnets |
| **Class B** | `172.16.0.0` – `172.31.255.255` | `172.16.0.0/12` | Medium networks, Docker default (`172.17.0.0/16`) |
| **Class C** | `192.168.0.0` – `192.168.255.255` | `192.168.0.0/16` | Home routers and standard consumer Wi-Fi |

### 1.3 NAT (Network Address Translation)
Your router translates private internal IPs to your single public IP when you make outbound requests. It assigns an ephemeral source port on the public IP to track which internal device requested which packet.
> **Security Implication**: External websites and remote observers only see your router's public IP and ephemeral source port. However, any adversary with access to your local Wi-Fi / LAN can inspect internal un-NATed traffic.

---

## 2. IPv4 vs. IPv6 & The Dual-Stack Trap

### 2.1 Technical Comparison

| Feature | IPv4 | IPv6 |
| :--- | :--- | :--- |
| **Address Length** | 32-bit (4 octets: `192.0.2.1`) | 128-bit (8 hextets: `2001:0db8:85a3::8a2e:0370:7334`) |
| **Address Space** | ~4.29 billion ($2^{32}$) | ~$3.4 \times 10^{38}$ ($2^{128}$) |
| **NAT Requirement** | Standard due to address exhaustion | Unnecessary; every device receives a global IP |
| **Security Risk** | NAT provides accidental inbound masking | Every device is directly addressable by default |

### 2.2 The IPv6 Privacy & Tracking Nightmare
In IPv4, your entire home network shares one public IP via NAT. In IPv6:
1. **Global Unicast Addresses (GUA)**: Every single device (phone, smart TV, PC) gets its own globally routable public IPv6 address.
2. **EUI-64 MAC Leaks**: Historically, IPv6 generated the host portion of an address directly from the physical MAC address (splitting the MAC and inserting `FF:FE`). This permanently tied your physical network card to your outbound IP traffic across any network.
3. **IPv6 Privacy Extensions (RFC 4941)**: Modern OSes generate temporary, randomized IPv6 interface identifiers that rotate periodically, but misconfigured endpoints can still leak static identifiers.
4. **Dual-Stack VPN Bypass**: Many VPN clients only route IPv4 traffic. If your ISP supports IPv6 and your VPN does not disable or route IPv6, outbound IPv6 requests will bypass the VPN tunnel entirely and leak your real ISP-assigned IPv6 address.

---

## 3. Subnets, Subnet Masks, & Default Gateways

### 3.1 Subnets & CIDR Notation
A subnet divides a network into smaller chunks. The **Subnet Mask** defines which bits belong to the network prefix and which belong to host addresses.

* CIDR (Classless Inter-Domain Routing) shorthand: `/24` means the first 24 bits are the network ID.
* Example: `192.168.1.0/24`
  * Netmask: `255.255.255.0`
  * Total IP addresses: 256 ($2^{32-24}$)
  * Usable host IPs: 254 (`192.168.1.1` to `192.168.1.254`)
  * Network address: `192.168.1.0`
  * Broadcast address: `192.168.1.255`

### 3.2 The Default Gateway & Packet Forwarding
The gateway is the router interface connecting your local subnet to other subnets or the internet (typically `192.168.1.1` or `10.0.0.1`).
* If destination IP is in the **same subnet**: The OS resolves the target MAC address via ARP and sends frames directly across the switch/Wi-Fi.
* If destination IP is **outside the subnet**: The OS forwards the packet to the Default Gateway's MAC address, letting the gateway route it upstream.

---

## 4. DNS (Domain Name System) Mechanics & Leaks

### 4.1 How Resolution Works
DNS converts human-readable domain names (`target.com`) into IP addresses (`93.184.216.34`).

```
[ Client ] -> [ Local DNS Cache / Hosts File ]
                 | (Cache miss)
                 v
             [ Recursive Resolver (ISP / 1.1.1.1 / 8.8.8.8) ]
                 |
                 +---> [ Root Nameserver (.) ]
                 +---> [ TLD Nameserver (.com) ]
                 +---> [ Authoritative Nameserver (target.com) ]
```

### 4.2 Why Plaintext DNS Destroys Anonymity
By default, standard DNS queries run over **UDP Port 53 in plaintext**.
* Your ISP, local Wi-Fi sniffers, or upstream routers can see every domain you look up in real time, even if you connect to the site using HTTPS.
* HTTPS encrypts the HTTP payload (Layer 7), but standard DNS queries happen *before* the TLS handshake and reveal who you are contacting.

### 4.3 Encrypted DNS Protocols (DoH / DoT)
* **DoH (DNS over HTTPS - Port 443)**: Wraps DNS queries in standard HTTPS traffic, making them indistinguishable from normal web requests to passive observers.
* **DoT (DNS over TLS - Port 853)**: Direct TLS tunnel for DNS queries. Easier for firewalls to identify and block because of the dedicated port.
* **DNSCrypt**: Encrypts traffic between the client and DNS resolver using elliptic-curve crypto.

### 4.4 DNS Leaks Under VPNs
A **DNS Leak** occurs when your VPN routes normal internet traffic through the encrypted VPN tunnel, but your operating system continues sending DNS queries to your ISP's DNS resolver or local router.
* **Cause**: Windows multi-homed name resolution (Smart Multi-Homed Name Resolution), IPv6 fallback, or DHCP-provided DNS servers overriding the virtual adapter settings.
* **Result**: An eavesdropper monitoring your ISP line sees all the sites you visit despite your active VPN.

---

<div align="center">
  <sub>Published and maintained by <a href="https://draxo.dev"><b>draxo.dev</b></a></sub>
</div>
