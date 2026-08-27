# Module 04: VPN Mechanics, OPSEC Realities & Provider Analysis

A Virtual Private Network (VPN) is one of the most misunderstood privacy tools in cybersecurity. Commercial marketing has convinced millions of users that clicking "Connect" makes them an untouchable ghost on the internet. In this module, we break down how VPNs actually work, where they fail, and conduct a threat-model breakdown of providers like ProtonVPN vs. Mullvad.

---

## 1. How a VPN Operates Under the Hood

### 1.1 The Virtual Adapter & Routing Table
When a VPN client starts on your machine:
1. It creates a **virtual network interface (TUN/TAP adapter)**.
2. It modifies your operating system's **kernel routing table**, setting the default route (`0.0.0.0/0`) to point through the virtual adapter instead of your physical LAN gateway.
3. It establishes an encrypted tunnel (using protocols like **WireGuard** or **OpenVPN**) over UDP/TCP to a remote VPN server.

<div class="vpn-tunnel-comparison">
  <div class="tunnel-card tunnel-unprotected">
    <div class="tunnel-header">STANDARD CONNECTION (NO VPN)</div>
    <div class="tunnel-flow">
      <div class="t-node">Your App</div>
      <div class="t-arrow-red">➔ Plaintext Headers ➔</div>
      <div class="t-node">ISP Router (Logs Everything)</div>
      <div class="t-arrow-red">➔ Public IP Visible ➔</div>
      <div class="t-node">Target Website</div>
    </div>
  </div>
  <div class="tunnel-card tunnel-protected">
    <div class="tunnel-header">VPN PROTECTED TUNNEL</div>
    <div class="tunnel-flow">
      <div class="t-node">Your App</div>
      <div class="t-arrow-green">➔ Encrypted TUN Adapter ➔</div>
      <div class="t-node">ISP (Sees only UDP Stream)</div>
      <div class="t-arrow-green">➔ Decrypted at VPN Node ➔</div>
      <div class="t-node">Target Website (Sees VPN IP)</div>
    </div>
  </div>
</div>

### 1.2 The Trust Shift Rule
**A VPN does NOT encrypt your data across the entire internet.**
* The tunnel exists **only between your device and the VPN server**.
* From the VPN server to the target website, the traffic exits in whatever protocol you are using (HTTPS encrypts the payload, but the target server sees the VPN server's IP).
* **Core Rule**: A VPN does not eliminate trust; **it shifts trust from your ISP to the VPN provider**.

---

## 2. Common VPN Leak Vectors & Failure Modes

Even with an active VPN, your real identity can leak through several structural flaws:

| Leak Vector | Mechanism | Threat Outcome |
| :--- | :--- | :--- |
| **DNS Leak** | OS sends DNS requests to local ISP resolver outside the VPN tunnel. | ISP still sees all domains visited. |
| **IPv6 Leak** | VPN only tunnels IPv4; outbound IPv6 requests bypass tunnel directly to ISP. | Exposes real ISP-assigned global IPv6 address. |
| **WebRTC STUN Leak** | Browser executes STUN request punching through NAT. | Remote website reads your real public and private IPs. |
| **Kill Switch Failure** | VPN connection drops momentarily; OS fails back to physical network before renegotiating. | Unencrypted packets leak real IP during reconnect. |
| **Traffic Timing Correlation** | An adversary monitoring your ISP line and the target server correlates packet burst sizes and timestamps. | Confirms you are the sender despite encryption. |

---

## 3. Threat Modeling Providers: Commercial Traps vs. True OPSEC

Not all VPN providers are architected equally. When choosing an infrastructure provider, look past marketing slogans and examine the legal jurisdiction, account creation mechanics, and data retention architecture.

<div class="comparison-grid">
  <!-- Commercial / Proton Card -->
  <div class="comp-card comp-commercial">
    <div class="comp-header">
      <div class="comp-badge badge-warning">COMMERCIAL / PROTON</div>
      <div class="comp-score-box">
        <div class="score-label">OPSEC PRIVACY SCORE</div>
        <div class="score-bar-bg"><div class="score-bar-fill fill-low" style="width: 35%;"></div></div>
        <div class="score-val">35% RATED ANONYMITY</div>
      </div>
    </div>
    <div class="comp-body">
      <div class="comp-row">
        <div class="comp-key">Account Identifier</div>
        <div class="comp-val val-negative">✕ Email / Username / Password required</div>
      </div>
      <div class="comp-row">
        <div class="comp-key">KYC / Identity Trail</div>
        <div class="comp-val val-negative">✕ Tied to payment records & recovery inboxes</div>
      </div>
      <div class="comp-row">
        <div class="comp-key">Anonymous Payment</div>
        <div class="comp-val val-neutral">△ Limited (Requires 3rd-party KYC gateways)</div>
      </div>
      <div class="comp-row">
        <div class="comp-key">Logging Architecture</div>
        <div class="comp-val val-negative">✕ Subject to Swiss criminal court logging orders</div>
      </div>
      <div class="comp-row">
        <div class="comp-key">Real-World Audit</div>
        <div class="comp-val val-negative">✕ Documented IP logging compliance cases</div>
      </div>
    </div>
  </div>

  <!-- Mullvad Card -->
  <div class="comp-card comp-mullvad">
    <div class="comp-header">
      <div class="comp-badge badge-success">MULLVAD VPN</div>
      <div class="comp-score-box">
        <div class="score-label">OPSEC PRIVACY SCORE</div>
        <div class="score-bar-bg"><div class="score-bar-fill fill-high" style="width: 98%;"></div></div>
        <div class="score-val">98% RATED ANONYMITY</div>
      </div>
    </div>
    <div class="comp-body">
      <div class="comp-row">
        <div class="comp-key">Account Identifier</div>
        <div class="comp-val val-positive">✓ Random 16-Digit Token (Zero KYC)</div>
      </div>
      <div class="comp-row">
        <div class="comp-key">KYC / Identity Trail</div>
        <div class="comp-val val-positive">✓ ZERO personal data collected or stored</div>
      </div>
      <div class="comp-row">
        <div class="comp-key">Anonymous Payment</div>
        <div class="comp-val val-positive">✓ Physical Cash in Mail / Monero (XMR)</div>
      </div>
      <div class="comp-row">
        <div class="comp-key">Logging Architecture</div>
        <div class="comp-val val-positive">✓ Diskless RAM-only infrastructure</div>
      </div>
      <div class="comp-row">
        <div class="comp-key">Real-World Audit</div>
        <div class="comp-val val-positive">✓ Swedish Police raid yielded 0 logs</div>
      </div>
    </div>
  </div>
</div>

### 3.1 The Reality of Commercial VPNs & Proton
* **Account Linkage**: Providers like Proton, Nord, and Surfshark require an email address, username, and password upon registration. This immediately links your payment records, recovery accounts, and communication logs to a central identity.
* **Jurisdiction & Legal Compliance**:
  * While Switzerland (where Proton is based) has strict privacy laws, Swiss courts **can and do compel Swiss companies to log specific targets** under Swiss criminal code orders (as seen in the documented 2021 French activist case where Proton was legally forced to log IP and browser fingerprints of a target).
  * No commercial provider operating a business entity is above the court orders of its sovereign jurisdiction.
* **Heavy Marketing & Affiliate Schemes**: Most "top 10 VPN" review sites are owned by the VPN companies themselves or run on massive recurring affiliate payouts, skewing technical recommendations.

### 3.2 Why Mullvad Sets the Benchmark for Privacy
Mullvad is widely regarded by systems engineers and security researchers as the gold standard for network proxying due to its strict zero-knowledge architecture:

1. **No Account Information**:
   * Mullvad generates a **random 16-digit account number**.
   * It never asks for an email, phone number, name, or password.
2. **Anonymous Payment Methods**:
   * Accepts **cash mailed in a physical envelope** with only the account token written inside.
   * Accepts **Monero (XMR)** for untraceable on-chain settlement.
3. **RAM-Only Diskless Servers**:
   * Servers run on ephemeral operating system images in memory with no hard drive logging.
4. **Real-World Stress Test (2023 Police Raid)**:
   * In April 2023, the Swedish National Police visited Mullvad's Gothenburg offices with a search warrant to seize user data.
   * Because of Mullvad's system architecture, no user data or logs existed to seize, and the authorities left empty-handed.
5. **No Port Forwarding**:
   * Mullvad eliminated port forwarding to prevent users from being uniquely fingerprinted or abuse actors from compromising the network integrity.

---

## 4. Advanced Tracking Beyond the VPN: Browser Fingerprinting

Using Mullvad or any VPN **only conceals your IP address**. Advanced adversaries and tracking networks do not rely on IPs alone.

### 4.1 What a VPN CANNOT Protect You From:
* **Browser Fingerprinting**: Websites probe your browser engine using Canvas rendering, WebGL attributes, installed fonts, audio context hardware hashing, and screen geometry. This creates a hash unique to your exact device that persists across IP changes.
* **Persistent State & Cookies**: LocalStorage, IndexedDB, Session Cookies, and Service Workers keep you authenticated and tracked regardless of what VPN node you switch to.
* **Application-Level Telemetry**: Logging into personal accounts (Google, Discord, Steam, Twitter) while connected to a VPN immediately ties that VPN exit IP to your permanent identity.

### 4.2 The Layered OPSEC Defense Stack

<div class="defense-stack-container">
  <div class="stack-layer layer-5">
    <div class="layer-pill">LAYER 5</div>
    <div class="layer-title">Human Discipline & Zero Cross-Contamination</div>
    <div class="layer-desc">Never link personal accounts, phone numbers, or credit cards to burner sessions.</div>
  </div>
  <div class="stack-layer layer-4">
    <div class="layer-pill">LAYER 4</div>
    <div class="layer-title">Ephemeral Operating Systems</div>
    <div class="layer-desc">Tails OS / Qubes OS / Whonix inside isolated hardware hypervisors.</div>
  </div>
  <div class="stack-layer layer-3">
    <div class="layer-pill">LAYER 3</div>
    <div class="layer-title">Anti-Fingerprinting Browser Engine</div>
    <div class="layer-desc">Mullvad Browser / Tor Browser (Canvas & WebGL spoofing + uniform user-agents).</div>
  </div>
  <div class="stack-layer layer-2">
    <div class="layer-pill">LAYER 2</div>
    <div class="layer-title">Protocol & DNS Hardening</div>
    <div class="layer-desc">Encrypted DNS (DoH/DoT), WebRTC disabled, IPv6 dual-stack disabled.</div>
  </div>
  <div class="stack-layer layer-1">
    <div class="layer-pill">LAYER 1</div>
    <div class="layer-title">Network Proxy Layer</div>
    <div class="layer-desc">Mullvad WireGuard / Multi-hop Tor routing.</div>
  </div>
</div>

* **Golden Rule**: Anonymity is not a software you download; it is an unbroken chain of operational discipline.
