# 🛠️ Network Security & OPSEC Tool Suite

A collection of lightweight, standalone, zero-dependency Python security utilities built to audit local network posture, detect live Man-in-the-Middle attacks, calculate bitwise subnets, and analyze covert DNS exfiltration.

---

## 📑 Tools Overview

| Tool | Focus Area | Command Usage | Key Functionality |
| :--- | :--- | :--- | :--- |
| **[`opsec_audit.py`](./opsec_audit.py)** | Endpoint Security | `python tools/opsec_audit.py` | Audits outbound SMB port 445 leaks, IPv6 dual-stack bypass, and DNS bindings |
| **[`arp_watch.py`](./arp_watch.py)** | MITM Detection | `python tools/arp_watch.py --watch` | Real-time sentinel monitoring local ARP cache for duplicate MAC collisions |
| **[`subnet_calc.py`](./subnet_calc.py)** | Network Math | `python tools/subnet_calc.py 10.0.0.0/16` | Bitwise CIDR calculator: Netmask, Wildcard, Broadcast, Host ranges, and Binary |
| **[`dns_entropy.py`](./dns_entropy.py)** | Exfil Analysis | `python tools/dns_entropy.py <domain>` | Calculates Shannon Entropy to detect DNS tunneling (dnscat2/iodine) and DGA botnets |

---

## 🚀 Tool Usage & Instructions

### 1. `opsec_audit.py` — Local Network Leak & OPSEC Auditor
Audits whether your endpoint is actively leaking unencrypted identifying traffic:
```bash
python tools/opsec_audit.py
```
* **Checks Performed**:
  * Outbound TCP Port 445 (SMB) exposure (detects vulnerability to forced UNC path NetNTLMv2 theft).
  * Outbound IPv6 route status (detects dual-stack VPN bypass risks).
  * Active DNS server bindings.
  * Public IP & ISP classification (residential vs. datacenter/VPN).

---

### 2. `arp_watch.py` — Real-Time ARP Poisoning Sentinel
Monitors the local operating system ARP table to detect active Man-in-the-Middle (MITM) attacks:
```bash
# Single snapshot check
python tools/arp_watch.py

# Continuous live monitoring (polls every 2 seconds)
python tools/arp_watch.py --watch --interval 2
```
* **Alert Triggers**:
  * Multiple IP addresses mapped to the exact same physical MAC address (`arpspoof` signature).
  * Gateway MAC address mutation during active sessions.

---

### 3. `subnet_calc.py` — CIDR & Subnet Bitwise Calculator
Quickly parses and breaks down any IPv4 network prefix:
```bash
python tools/subnet_calc.py 192.168.1.0/24
python tools/subnet_calc.py 172.16.50.0/22
python tools/subnet_calc.py 10.0.0.0/8
```
* **Outputs**:
  * RFC 1918 Private vs. Public space classification.
  * Subnet Mask and Wildcard Mask.
  * Usable First and Last host addresses.
  * Total vs. Usable host count.
  * 32-bit binary dotted representation of network, netmask, and broadcast.

---

### 4. `dns_entropy.py` — Shannon Entropy & DNS Tunneling Analyzer
Analyzes domain strings to detect covert data exfiltration and DGA botnet domains:
```bash
python tools/dns_entropy.py a7f93b8c2d1e04b8921a8f90c3e.tunnel.darknet-c2.net
```
* **Evaluates**:
  * FQDN and Subdomain length thresholds.
  * Mathematical Shannon Entropy: $H(X) = -\sum P(x) \log_2 P(x)$.
  * High-entropy ($H > 4.2$) flag alerts indicating Base32/Hex/Base64 encoded data payloads.

---

<div align="center">
  <sub>Published and maintained by <a href="https://github.com/DaddyZyn"><b>DaddyZyn (DRAXO.dev)</b></a></sub>
</div>
