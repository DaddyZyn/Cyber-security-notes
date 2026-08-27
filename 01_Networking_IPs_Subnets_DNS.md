# Module 01: Networking Fundamentals — IPs, Subnets, Gateways & DNS

Understanding how data moves across Layer 2 and Layer 3 of the OSI model is mandatory before talking about anonymity, privacy, or tracking. If you don't know how packets are addressed and routed, you can't properly conceal them.

---

## 1. Public vs. Private IP Addresses

### 1.1 The Core Difference
* **Public IP**: Globally unique IP assigned to your gateway/router by your Internet Service Provider (ISP). Every device directly reachable on the public internet communicates using public IPs.
* **Private IP**: Non-routable IP addresses used strictly inside local area networks (LAN). They exist behind a router and cannot be reached directly from the wider internet without port forwarding or tunneling.

<div class="network-flow-container">
  <div class="flow-step">
    <div class="flow-badge">LOCAL CLIENT</div>
    <div class="flow-title">Your Computer</div>
    <div class="flow-pill">192.168.1.50</div>
    <div class="flow-desc">Private Subnet (RFC 1918)</div>
  </div>
  <div class="flow-arrow">
    <div class="arrow-symbol">➔</div>
    <div class="arrow-text">LAN Ethernet / Wi-Fi</div>
  </div>
  <div class="flow-step">
    <div class="flow-badge">LOCAL GATEWAY</div>
    <div class="flow-title">Router (NAT)</div>
    <div class="flow-pill">192.168.1.1</div>
    <div class="flow-desc">Translates Port & IP</div>
  </div>
  <div class="flow-arrow">
    <div class="arrow-symbol">➔</div>
    <div class="arrow-text">WAN Public Uplink</div>
  </div>
  <div class="flow-step highlight-step">
    <div class="flow-badge">GLOBAL INTERNET</div>
    <div class="flow-title">Target Server</div>
    <div class="flow-pill public-pill">203.0.113.42</div>
    <div class="flow-desc">Only sees Router Public IP</div>
  </div>
</div>

### 1.2 RFC 1918 Private Address Ranges
These blocks are reserved specifically for private networks:
* **Class A**: `10.0.0.0` – `10.255.255.255` (`10.0.0.0/8`) — Used in large enterprise networks, data centers, and VPN internal subnets.
* **Class B**: `172.16.0.0` – `172.31.255.255` (`172.16.0.0/12`) — Medium networks, container networks (Docker default is `172.17.0.0/16`).
* **Class C**: `192.168.0.0` – `192.168.255.255` (`192.168.0.0/16`) — Home routers and standard consumer Wi-Fi.

### 1.3 NAT (Network Address Translation)
Your router translates private IPs to your single public IP when you make outbound requests. It assigns an ephemeral source port on the public IP to keep track of which internal machine requested the packet.
* *Security implication*: Devices on the public internet only see your router's public IP and the assigned source port, not your internal private IP (`192.168.x.x`). However, local network adversaries can see all internal IP traffic un-NATed.

---

## 2. IPv4 vs. IPv6 & The Dual-Stack Trap

### 2.1 Technical Comparison

| Feature | IPv4 | IPv6 |
| :--- | :--- | :--- |
| **Address Length** | 32-bit (4 octets: `192.0.2.1`) | 128-bit (8 hextets: `2001:0db8:85a3::8a2e:0370:7334`) |
| **Address Space** | ~4.29 billion ($2^{32}$) | ~$3.4 \times 10^{38}$ ($2^{128}$) |
| **NAT Requirement** | Standard due to address exhaustion | Unnecessary; every device gets a globally unique address |
| **Security Risk** | NAT provides accidental inbound masking | Every device is directly addressable by default |

### 2.2 The IPv6 Privacy & Tracking Nightmare
In IPv4, your whole household shares one public IP via NAT. In IPv6:
1. **Global Unicast Addresses (GUA)**: Every single device (phone, smart TV, desktop) receives its own public, globally routable IPv6 address.
2. **EUI-64 MAC Leaks**: Historically, IPv6 generated the host portion of an address directly from the hardware MAC address (splitting the MAC and inserting `FF:FE`). This permanently tied your physical network card to your outbound IP traffic across any network.
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

### 3.2 The Default Gateway
The gateway is the router interface connecting your local subnet to other subnets or the internet (typically `192.168.1.1` or `10.0.0.1`).
* If destination IP is in the **same subnet**: The OS resolves the target MAC address via ARP and sends frames directly across the switch/Wi-Fi.
* If destination IP is **outside the subnet**: The OS forwards the packet to the Default Gateway's MAC address, letting the gateway route it upstream.

---

## 4. DNS (Domain Name System) Mechanics & Leaks

### 4.1 How Resolution Works
DNS converts human-readable domain names (`target.com`) into IP addresses (`93.184.216.34`).

<div class="dns-tree-container">
  <div class="dns-node dns-client">
    <div class="dns-pill">STEP 1</div>
    <div class="dns-title">Client Browser</div>
    <div class="dns-desc">Checks Local Hosts & Cache</div>
  </div>
  <div class="dns-arrow">➔</div>
  <div class="dns-node dns-resolver">
    <div class="dns-pill">STEP 2</div>
    <div class="dns-title">Recursive Resolver</div>
    <div class="dns-desc">ISP / 1.1.1.1 / 8.8.8.8</div>
  </div>
  <div class="dns-arrow">➔</div>
  <div class="dns-tier-group">
    <div class="dns-subnode">Root Server (.)</div>
    <div class="dns-subnode">TLD Server (.com)</div>
    <div class="dns-subnode highlight-subnode">Authoritative Server (target.com)</div>
  </div>
</div>

### 4.2 Why Plaintext DNS Destroys Anonymity
By default, standard DNS queries run over **UDP Port 53 in plaintext**.
* Your ISP, local Wi-Fi sniffers, or upstream routers can see every domain you look up in real time, even if you connect to the site using HTTPS.
* HTTPS encrypts the HTTP payload (Layer 7), but standard DNS queries happen *before* the TLS handshake and reveal who you are contacting.

### 4.3 Encrypted DNS Protocols
* **DoH (DNS over HTTPS - Port 443)**: Wraps DNS queries in standard HTTPS traffic, making them indistinguishable from normal web requests to passive observers.
* **DoT (DNS over TLS - Port 853)**: Direct TLS tunnel for DNS queries. Easier for firewalls to identify and block because of the dedicated port.
* **DNSCrypt**: Encrypts traffic between the client and DNS resolver using elliptic-curve crypto.

### 4.4 DNS Leaks Under VPNs
A **DNS Leak** occurs when your VPN routes normal internet traffic through the encrypted VPN tunnel, but your operating system continues sending DNS queries to your ISP's DNS resolver or local router.
* **Cause**: Windows multi-homed name resolution (Smart Multi-Homed Name Resolution), IPv6 fallback, or DHCP-provided DNS servers overriding the virtual adapter settings.
* **Result**: An eavesdropper monitoring your ISP line sees all the sites you visit despite your active VPN.
