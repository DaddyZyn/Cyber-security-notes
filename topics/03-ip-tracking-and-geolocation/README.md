# 🛰️ Module 03: IP Tracking, Geolocation Realities & House-Level Doxxing

One of the biggest myths in internet culture and script-kiddie lore is that "pulling someone's IP gives you their exact house address." In this module, we dissect how IPs are obtained, what IP geolocation actually does, and how adversaries *actually* find exact physical locations.

---

## 📑 Table of Contents
- [1. How Adversaries "Pull" Your IP Address](#1-how-adversaries-pull-your-ip-address)
  - [1.1 Direct Peer-to-Peer (P2P) Connections](#11-direct-peer-to-peer-p2p-connections)
  - [1.2 Web Tracking Links & IP Loggers](#12-web-tracking-links--ip-loggers-grabify-canary-tokens)
  - [1.3 WebRTC STUN Leaks](#13-webrtc-leaks)
- [2. The IP Geolocation Myth: Why IPs Do NOT Point to Houses](#2-the-ip-geolocation-myth-why-ips-do-not-point-to-houses)
  - [2.1 How GeoIP Databases Work](#21-how-geoip-databases-work)
  - [2.2 Real-World Accuracy Limitations](#22-accuracy-limits)
- [3. How Physical House Locations are ACTUALLY Found](#3-how-physical-house-locations-are-actually-found)
  - [3.1 Wi-Fi BSSID Geolocation (War-driving Databases)](#31-wi-fi-bssid-geolocation-war-driving-databases)
  - [3.2 Correlating Data Breaches & OSINT](#32-correlating-data-breaches--osint)
  - [3.3 ISP DHCP Logs & Legal Subpoenas](#33-isp-dhcp-logs--legal-subpoenas)
  - [3.4 Browser Geolocation APIs](#34-browser-geolocation-api--malicious-permissions)

---

## 1. How Adversaries "Pull" Your IP Address

A remote party cannot grab your IP out of thin air; **you must establish a direct or indirect network connection with a service they control or monitor**.

### 1.1 Direct Peer-to-Peer (P2P) Connections
* **P2P Games & Voice Apps**: Older gaming lobbies (old Xbox 360/PS3 architecture, older GTA Online, P2P torrent swarms, legacy Skype/IRC) connect players directly to each other without dedicated relay servers.
* **Mechanism**: Running a packet capture tool like Wireshark or CommView during an active P2P session reveals the direct UDP stream from your peer's IP address.
* *Modern fix*: Almost all modern platforms (Discord, modern matchmaking) use centralized relay servers or proxy voice streams through their infrastructure, hiding user IPs behind platform server IPs.

### 1.2 Web Tracking Links & IP Loggers (Grabify, Canary Tokens)
* An attacker sends a link or embeds a hidden image element (`<img src="https://attacker-server.com/logger.png">`) in an HTML email or web page.
* When your client loads the asset, your browser performs a TCP handshake and HTTP GET request to the attacker's server.
* The server's access log records:
  * Your Public IP address
  * Timestamp
  * User-Agent (Browser version, OS architecture)
  * Referer header

### 1.3 WebRTC Leaks
* **WebRTC (Web Real-Time Communication)** allows browsers to make peer-to-peer voice/video calls.
* To punch through NAT, WebRTC queries STUN (Session Traversal Utilities for NAT) servers.
* JavaScript running on a webpage can trigger a WebRTC STUN request that exposes both your **local private IP** and your **real public IP**, even if you are using an HTTP proxy or a misconfigured VPN extension.

---

## 2. The IP Geolocation Myth: Why IPs Do NOT Point to Houses

When someone enters an IP address into an online lookup tool (e.g., MaxMind GeoIP, IPinfo, DB-IP), the result is **coarse, estimated geographic routing data**, NOT a GPS coordinate of a physical building.

```
+-------------------------------------------------------------+
|                     WHAT GEOIP SHOWS                        |
|                                                             |
|   [ Public IP: 73.182.xx.xx ]                               |
|   -> ISP: Comcast Cable Communications                      |
|   -> Autonomous System: AS7922                              |
|   -> City / Metro Area: Atlanta, GA (Confidence: ~60-80%)   |
|   -> Coordinates: 33.7490, -84.3880 (City Center Centroid)  |
|                                                             |
|   WARNING: The GPS coordinates provided by IP lookups are   |
|   just the arbitrary center point of the city or postal     |
|   code area. It is NOT a rooftop coordinate.                |
+-------------------------------------------------------------+
```

### 2.1 How GeoIP Databases Work
1. **BGP and Routing Hubs**: ISPs announce IP blocks assigned to regional aggregation nodes (DSLAMs, CMTS, PoPs).
2. **Registry Data (RIRs)**: Regional registries (ARIN, RIPE, APNIC) record the corporate mailing address of the ISP organization leasing the block, not the residential subscriber.

### 2.2 Accuracy Limits
* **Country-level accuracy**: ~95–99%
* **Region/State accuracy**: ~75–90%
* **City accuracy**: ~50–75%
* **Street/House accuracy**: **0% (Impossible via pure IP routing tables)**

---

## 3. How Physical House Locations are ACTUALLY Found

If IP geolocation is inaccurate, how do skilled doxxers, threat actors, and investigators actually locate a specific home?

### 3.1 Wi-Fi BSSID Geolocation (War-driving Databases)
This is the most powerful remote physical location exploit:
1. **The Infrastructure**: Companies (Google, Apple, Skyhook) and war-driving projects (WiGLE.net) have mapped the exact physical GPS locations of billions of Wi-Fi routers worldwide.
2. **The Identifier**: Every Wi-Fi router broadcasts a unique BSSID (the MAC address of its wireless radio interface).
3. **The Exploit**:
   * If an application on your machine, mobile device, or a script gains access to nearby Wi-Fi network BSSIDs and their signal strengths (RSSI):
   * The attacker queries the BSSID against WiGLE / Google Geolocation API.
   * By trilaterating signal strengths from 2–3 nearby routers, they determine your physical rooftop location within **5 to 10 meters**.

### 3.2 Correlating Data Breaches & OSINT
Adversaries almost never rely solely on network packets. They chain digital footprints:
1. They obtain your username, email, or phone number from online activity.
2. They search aggregated data breach indexes (e.g., leaked databases from food delivery apps, clothing stores, credit bureaus, vehicle registrations).
3. Breaches contain full names tied to physical residential billing/shipping addresses, credit card records, and phone numbers.

### 3.3 ISP DHCP Logs & Legal Subpoenas
* Your ISP maintains strict **DHCP reservation logs** recording which customer account held which public IP address at any specific millisecond.
* Law enforcement with a subpoena (or corrupt ISP employees/SIM swappers with internal access) look up the IP + timestamp in the ISP's billing database to get the exact residential subscriber name, physical line installation address, and payment records.

### 3.4 Browser Geolocation API / Malicious Permissions
* Websites request high-precision device location via `navigator.geolocation.getCurrentPosition()`.
* If granted, the device uses onboard GPS, cell tower IDs, and Wi-Fi scanning to feed exact lat/long coordinates back to the remote web server.

---

<div align="center">
  <sub>Published and maintained by <a href="https://draxo.dev"><b>draxo.dev</b></a></sub>
</div>
