# Module 03: IP Tracking, Geolocation Realities & House-Level Doxxing

One of the biggest myths in internet culture and script-kiddie lore is that "pulling someone's IP gives you their exact house address." In this module, we dissect how IPs are obtained, what IP geolocation actually does, and how adversaries *actually* find exact physical locations.

---

## 1. How Adversaries "Pull" Your IP Address

A remote party cannot grab your IP out of thin air; **you must establish a direct or indirect network connection with a service they control or monitor**.

### 1.1 Direct Peer-to-Peer (P2P) Connections
* **P2P Games & Voice Apps**: Older gaming lobbies (old Xbox 360/PS3 architecture, older GTA Online, P2P torrent swarms, legacy Skype/IRC) connect players directly to each other without dedicated relay servers.
* **Mechanism**: Running a packet capture tool like Wireshark or CommView during an active P2P session shows the direct UDP stream from your peer's IP address.
* *Modern fix*: Almost all modern platforms (Discord, modern game matchmaking) use centralized relay servers or proxy voice streams through their infrastructure, hiding user IPs behind platform server IPs.

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

<div class="geoip-inspector">
  <div class="geoip-header">
    <div class="geoip-pill">GEOIP INSPECTOR</div>
    <div class="geoip-status">ACCURACY LIMIT: REGIONAL CENTROID ONLY</div>
  </div>
  <div class="geoip-grid">
    <div class="geoip-stat"><span class="stat-name">TARGET IP:</span> <span class="stat-val">73.182.xx.xx</span></div>
    <div class="geoip-stat"><span class="stat-name">ISP / ASN:</span> <span class="stat-val">AS7922 (Comcast)</span></div>
    <div class="geoip-stat"><span class="stat-name">EST. REGION:</span> <span class="stat-val">Atlanta Metro Area</span></div>
    <div class="geoip-stat"><span class="stat-name">ROOFTOP ACCURACY:</span> <span class="stat-val stat-danger">0.0% (IMPOSSIBLE VIA IP)</span></div>
  </div>
  <div class="geoip-meters">
    <div class="meter-row">
      <span class="meter-lbl">Country Level</span>
      <div class="meter-bar"><div class="meter-fill" style="width: 99%;"></div></div>
      <span class="meter-pct">99%</span>
    </div>
    <div class="meter-row">
      <span class="meter-lbl">Region / State Level</span>
      <div class="meter-bar"><div class="meter-fill" style="width: 80%;"></div></div>
      <span class="meter-pct">80%</span>
    </div>
    <div class="meter-row">
      <span class="meter-lbl">City / Metro Level</span>
      <div class="meter-bar"><div class="meter-fill" style="width: 60%;"></div></div>
      <span class="meter-pct">60%</span>
    </div>
    <div class="meter-row">
      <span class="meter-lbl">Exact House / Street Address</span>
      <div class="meter-bar"><div class="meter-fill fill-zero" style="width: 0%;"></div></div>
      <span class="meter-pct">0% (ROOFTOP IMPOSSIBLE)</span>
    </div>
  </div>
</div>

### 2.1 How GeoIP Databases Work
1. **BGP and Routing Hubs**: ISPs announce IP blocks assigned to regional aggregation nodes (DSLAMs, CMTS, PoPs).
2. **Registry Data (RIRs)**: Regional registries (ARIN, RIPE, APNIC) record the corporate mailing address of the ISP organization leasing the block, not the residential subscriber.
3. **Accuracy Limits**:
   * Country-level accuracy: ~95–99%
   * Region/State accuracy: ~75–90%
   * City accuracy: ~50–75%
   * Street/House accuracy: **0%** (impossible via pure IP routing tables)

---

## 3. How Physical House Locations are ACTUALLY Found

If IP geolocation is inaccurate, how do skilled doxxers, threat actors, and investigators actually locate a specific home?

<div class="vector-grid">
  <div class="vector-card">
    <div class="vector-badge badge-critical">CRITICAL THREAT</div>
    <div class="vector-title">Wi-Fi BSSID Mapping</div>
    <div class="vector-desc">Adversaries query nearby router MACs against war-driving databases (WiGLE/Skyhook).</div>
    <div class="vector-stat">Accuracy: <strong>5 - 10 Meters</strong></div>
  </div>
  <div class="vector-card">
    <div class="vector-badge badge-high">HIGH THREAT</div>
    <div class="vector-title">Breaches & OSINT</div>
    <div class="vector-desc">Leaked databases from food delivery, e-commerce, and billing records tied to email/phone.</div>
    <div class="vector-stat">Accuracy: <strong>Exact Rooftop Address</strong></div>
  </div>
  <div class="vector-card">
    <div class="vector-badge badge-high">LEGAL / SUBPOENA</div>
    <div class="vector-title">ISP DHCP Logs</div>
    <div class="vector-desc">ISP maintains timestamps linking IP to the customer's physical fiber/cable installation.</div>
    <div class="vector-stat">Accuracy: <strong>Exact Legal Resident</strong></div>
  </div>
  <div class="vector-card">
    <div class="vector-badge badge-med">CLIENT SENSOR</div>
    <div class="vector-title">Browser Geolocation</div>
    <div class="vector-desc">Websites trigger HTML5 GPS prompts or query onboard device positioning APIs.</div>
    <div class="vector-stat">Accuracy: <strong>Sub-Meter GPS</strong></div>
  </div>
</div>

### 3.1 Wi-Fi BSSID Geolocation (War-driving Databases)
This is the most powerful remote physical location exploit:
1. **The Infrastructure**: Companies (Google, Apple, Skyhook) and war-driving projects (WiGLE.net) have mapped the exact physical GPS locations of billions of Wi-Fi routers worldwide.
2. **The Identifier**: Every Wi-Fi router broadcasts a unique BSSID (the MAC address of its wireless radio interface).
3. **The Exploit**:
   * If an application on your machine, mobile device, or a malicious script gains access to nearby Wi-Fi network BSSIDs and their signal strengths (RSSI):
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
