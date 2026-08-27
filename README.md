<div align="center">

# 🛡️ CYBERSECURITY & OPSEC FIELD NOTES
### *Low-Level Systems Architecture, Network Forensics & Adversarial Threat Modeling*

[![Author](https://img.shields.io/badge/Author-DaddyZyn%20%7C%20DRAXO.dev-000000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/DaddyZyn)
[![Topic](https://img.shields.io/badge/Focus-OPSEC%20%26%20Networking-000000?style=for-the-badge&logo=shield&logoColor=white)](#)
[![Request Topic](https://img.shields.io/badge/Request-New%20Topic-000000?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/DaddyZyn/Cyber-security-notes/issues/new?template=topic_request.yml)
[![Contributions](https://img.shields.io/badge/PRs-Welcome-000000?style=for-the-badge)](./CONTRIBUTING.md)

<p align="center">
  <b>A structured, deep technical documentation repository for security researchers, systems developers, and learners.</b><br>
  <i>Published and maintained by <a href="https://github.com/DaddyZyn"><b>DaddyZyn (DRAXO.dev)</b></a></i>
</p>

---

</div>

## 💡 Request a Topic or Suggest Concepts

Have a concept you want explained or documented in deep technical detail?
* 👉 **[Open a Topic Request on GitHub Issues](https://github.com/DaddyZyn/Cyber-security-notes/issues/new?template=topic_request.yml)**
* Or submit a pull request following our **[Contributing Guide](./CONTRIBUTING.md)**.

---

## 📑 Core Documentation Modules

| # | Topic Directory | Focus Areas | Quick Link |
| :---: | :--- | :--- | :---: |
| **01** | **[`01-networking-fundamentals`](./topics/01-networking-fundamentals/)** | Public vs. Private IPs, RFC 1918, NAT Translation, IPv4 vs. IPv6 Dual-Stack Leaks, Subnets (`/24`, `/16`), Gateways, DNS UDP 53 & DoH/DoT | [📖 Read Module](./topics/01-networking-fundamentals/README.md) |
| **02** | **[`02-hardware-identifiers`](./topics/02-hardware-identifiers/)** | Layer 2 vs. Layer 3 Boundaries, Why MACs never leave routers, Captive Portals, Client-side WinAPI Telemetry (`GetAdaptersAddresses`), MAC Spoofing | [📖 Read Module](./topics/02-hardware-identifiers/README.md) |
| **03** | **[`03-ip-tracking-and-geolocation`](./topics/03-ip-tracking-and-geolocation/)** | How IPs are pulled (P2P, WebRTC STUN), The GeoIP Centroid Myth, **Wi-Fi BSSID Triangulation (WiGLE/Skyhook 5-10m)**, ISP DHCP Subpoenas, Data Breaches | [📖 Read Module](./topics/03-ip-tracking-and-geolocation/README.md) |
| **04** | **[`04-vpn-mechanics-and-opsec`](./topics/04-vpn-mechanics-and-opsec/)** | TUN/TAP Adapters, Kernel Routing, The Trust Shift Rule, VPN Leak Vectors, **Commercial Traps (Proton/Nord KYC & Legal Logs) vs. Mullvad (16-Digit Zero-Data & Police Raid)** | [📖 Read Module](./topics/04-vpn-mechanics-and-opsec/README.md) |

---

## 🔍 Module Overviews

### 🌐 [01. Networking Fundamentals](./topics/01-networking-fundamentals/README.md)
* **NAT (Network Address Translation)**: How private subnets (`192.168.x.x`, `10.x.x.x`, `172.16.x.x`) are multiplexed behind a single public IPv4 gateway via ephemeral source ports.
* **The IPv6 Dual-Stack Trap**: Why VPN tunnels that only handle IPv4 expose your true identity through native IPv6 SLAAC address routing.
* **Encrypted DNS vs. Plaintext**: Why standard UDP port 53 reveals every visited domain to ISPs despite HTTPS, and how DNS-over-HTTPS (DoH) / DNS-over-TLS (DoT) solve Layer 7 visibility.

```
[ Local PC: 192.168.1.50 ] ➔ (LAN Ethernet) ➔ [ NAT Gateway: 192.168.1.1 ] ➔ (WAN Uplink) ➔ [ Target Server: 203.0.113.42 ]
```

---

### 💻 [02. Hardware Identifiers & MAC Addresses](./topics/02-hardware-identifiers/README.md)
* **The Layer 2 vs. Layer 3 Hard Boundary**:
  * Ethernet frames (and MAC addresses) exist **strictly inside the local broadcast domain**.
  * Your router **strips off your PC's MAC address** and generates a brand-new Ethernet frame before forwarding packets across the WAN. Remote web servers and game servers **cannot** read your MAC from an incoming IP packet.
* **How Hardware is Actually Tracked**:
  * Captive portals on public Wi-Fi APs recording physical association logs.
  * Native desktop applications and anti-cheats invoking `GetAdaptersAddresses()` or `GetAdaptersInfo()` and transmitting serialized HWIDs over encrypted HTTPS payloads.

```
+------------------------------------+------------------------------------+
|  OUI (Organization Unique ID)      |    NIC-Specific Serial             |
|  First 3 Bytes (00:1A:2B)          |    Last 3 Bytes (3C:4D:5E)         |
|  Identifies Chip Manufacturer      |    Unique Hardware Serial Number   |
+------------------------------------+------------------------------------+
```

---

### 🛰️ [03. IP Tracking, Geolocation Realities & House-Level Doxxing](./topics/03-ip-tracking-and-geolocation/README.md)
* **The GeoIP Myth**:
  * IP Geolocation databases (MaxMind, IP2Location) map IP blocks to **ISP regional routing hubs or city center centroids**—never physical rooftops.
  * City-level accuracy ranges between 50–75%; street-level accuracy via pure IP is **0%**.
* **How Physical Addresses are Actually Located**:
  * **Wi-Fi BSSID Trilateration**: Querying nearby wireless router MAC addresses against war-driving databases (WiGLE / Skyhook) calculates rooftop locations down to **5–10 meters**.
  * **OSINT & Data Breaches**: Chaining leaked delivery app databases, e-commerce records, and billing receipts.
  * **ISP DHCP Subpoenas**: Correlating millisecond IP assignments directly with subscriber installation contracts.

---

### 🔒 [04. VPN Mechanics, OPSEC & Provider Breakdown](./topics/04-vpn-mechanics-and-opsec/README.md)
* **The Trust Shift Rule**: A VPN does not magically grant anonymity; it merely shifts trust from your local ISP to the VPN server operator.
* **Commercial Providers (Proton / Nord) vs. Mullvad**:
  * **Proton / Commercial**: Requires account registration (email/password), payment trails, and operates under legal jurisdictions that compel target IP logging (e.g. 2021 Swiss court orders).
  * **Mullvad**: Anonymous 16-digit token generation (zero emails/passwords), cash-in-mail & Monero (XMR) support, diskless RAM-only infrastructure, and proven zero-log architecture verified during a real-world Swedish Police raid.

```
+---------------------------------------------------------------------------------------+
|                                THE 5-LAYER OPSEC STACK                                |
|                                                                                       |
|  [ LAYER 5 ]  Human Discipline & Zero Cross-Contamination (No personal account leaks) |
|  [ LAYER 4 ]  Ephemeral Operating Systems (Tails OS / Qubes OS / Whonix)               |
|  [ LAYER 3 ]  Anti-Fingerprinting Browser (Mullvad Browser / Tor Browser)             |
|  [ LAYER 2 ]  Protocol Hardening (Encrypted DNS, WebRTC disabled, IPv6 disabled)      |
|  [ LAYER 1 ]  Network Proxy (Mullvad WireGuard / Multi-Hop Tor)                       |
+---------------------------------------------------------------------------------------+
```

---

## 🤝 Contributing

Contributions, corrections, and new module submissions are welcome. Please check **[`CONTRIBUTING.md`](./CONTRIBUTING.md)** for details on structure and formatting.

---

## ⚖️ License & Credits

* **Author & Maintainer**: [DaddyZyn (DRAXO.dev)](https://github.com/DaddyZyn)
* **Purpose**: Educational, defensive security research, and systems engineering documentation.
* **Repository**: [https://github.com/DaddyZyn/Cyber-security-notes](https://github.com/DaddyZyn/Cyber-security-notes)
