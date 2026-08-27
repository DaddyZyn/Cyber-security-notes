# Module 02: Hardware Identifiers — MAC Addresses & Local Footprints

Many beginners confuse MAC addresses with IP addresses and misunderstand where hardware identifiers travel. Let's break down the mechanics at Layer 2 vs Layer 3.

---

## 1. What is a MAC Address?

A **Media Access Control (MAC)** address is a 48-bit (6-byte) physical identifier permanently assigned to a Network Interface Card (NIC) by the manufacturer.

<div class="mac-breakdown-card">
  <div class="mac-hex-display">
    <div class="mac-block block-oui">
      <div class="mac-badge">ORGANIZATION IDENTIFIER</div>
      <div class="mac-hex">00 : 1A : 2B</div>
      <div class="mac-label">OUI (First 3 Bytes / 24 Bits)</div>
      <div class="mac-sub">Registered to Vendor (Intel, Realtek, Apple)</div>
    </div>
    <div class="mac-block block-nic">
      <div class="mac-badge">DEVICE SERIAL</div>
      <div class="mac-hex">3C : 4D : 5E</div>
      <div class="mac-label">NIC Specific ID (Last 3 Bytes / 24 Bits)</div>
      <div class="mac-sub">Unique Physical Hardware Serial</div>
    </div>
  </div>
</div>

---

## 2. Where Does a MAC Address Travel? (The Layer 2 vs Layer 3 Rule)

### 2.1 The Hop-by-Hop Principle
* **MAC addresses operate exclusively at OSI Layer 2 (Data Link Layer).**
* **MAC addresses NEVER leave your local broadcast domain.**

<div class="layer2-flow-container">
  <div class="layer2-card">
    <div class="l2-header">HOP 1: YOUR PC ➔ LOCAL ROUTER</div>
    <div class="l2-body">
      <div class="l2-item"><span class="l2-key">SRC MAC:</span> <span class="l2-val val-client">00:11:22:33:44:55 (Your NIC)</span></div>
      <div class="l2-item"><span class="l2-key">DST MAC:</span> <span class="l2-val">AA:BB:CC:DD:EE:FF (Router LAN)</span></div>
      <div class="l2-item"><span class="l2-key">STATUS:</span> <span class="l2-badge badge-warning">Your MAC Visible ONLY on Local LAN</span></div>
    </div>
  </div>
  <div class="layer2-divider">
    <div class="divider-line"></div>
    <div class="divider-badge">ROUTER STRIPS ETHERNET FRAME</div>
    <div class="divider-line"></div>
  </div>
  <div class="layer2-card">
    <div class="l2-header">HOP 2: ROUTER ➔ REMOTE WEBSERVER</div>
    <div class="l2-body">
      <div class="l2-item"><span class="l2-key">SRC MAC:</span> <span class="l2-val">Router WAN Interface MAC</span></div>
      <div class="l2-item"><span class="l2-key">DST MAC:</span> <span class="l2-val">ISP Gateway Interface MAC</span></div>
      <div class="l2-item"><span class="l2-key">STATUS:</span> <span class="l2-badge badge-success">Your PC's MAC is 100% GONE</span></div>
    </div>
  </div>
</div>

* **Conclusion**: Remote servers, websites, and game hosts **cannot see your physical MAC address from an IP packet header**.

---

## 3. How Hardware Identifiers ARE Tracked & Leaked

If MAC addresses don't leave the local network in packet headers, how do adversaries and corporations use them to track you?

### 3.1 Local Wi-Fi Access Points & Captive Portals
* Public Wi-Fi (airports, hotels, cafes) logs your physical MAC address the instant you associate with the Access Point (AP).
* Even if you connect to a VPN immediately after authenticating, the network operator has already tied your device's physical hardware MAC, device hostname, and connection timestamps to your physical presence.

### 3.2 Client-Side Software & Telemetry (Layer 7 Exfiltration)
Websites running in standard web browsers cannot directly read your MAC address due to JavaScript sandbox restrictions. However:
* **Installed Applications (Steam, Discord, Game Anti-Cheats, EDRs, Malware)**: Run with native OS privileges.
* They call native APIs (e.g., Windows WinAPI `GetAdaptersAddresses()` or `GetAdaptersInfo()`) to read your real MAC address, disk serial numbers, BIOS UUID, and CPU IDs.
* They package these identifiers into encrypted HTTPS requests (Layer 7 payload) and send them to their servers, creating an unshakeable hardware profile (HWID).

### 3.3 ARP Sniffing on Shared Networks
On any unsegmented LAN (e.g., open Starbucks Wi-Fi or dorm networks):
* Any machine running Wireshark or `arp-scan` can discover every active host's MAC address and private IP.
* An attacker can execute **ARP Cache Poisoning (Man-in-the-Middle)** to redirect all your traffic through their machine before it reaches the router.

---

## 4. MAC Spoofing & Countermeasures

### 4.1 MAC Randomization
Modern mobile OSes (iOS, Android) and modern Windows/Linux desktop distributions feature built-in MAC randomization for Wi-Fi scanning and per-SSID connections.

### 4.2 Manual Spoofing
* **Linux**:
  ```bash
  sudo ip link set dev eth0 down
  sudo macchanger -r eth0
  sudo ip link set dev eth0 up
  ```
* **Windows**:
  * Device Manager -> Network Adapter -> Properties -> Advanced -> `Locally Administered Address` (or `Network Address`) -> Set to a custom 12-digit hex value.
  * Note: The second character must be `2`, `6`, `A`, or `E` to indicate a locally administered unicast address (e.g., `02:XX:XX:XX:XX:XX`).
