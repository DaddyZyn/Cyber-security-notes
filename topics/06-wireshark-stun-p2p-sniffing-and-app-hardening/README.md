# 🦈 Module 06: Wireshark STUN / P2P IP Sniffing & App Hardening

One of the most widely used methods by gamers, trolls, and script kiddies to pull IP addresses is sniffing **Peer-to-Peer (P2P)** media streams during voice and video calls using network packet analyzers like **Wireshark**. In this module, we break down the exact packet mechanics of STUN (Session Traversal Utilities for NAT), explain how IP addresses are extracted from packet captures, and configure app-by-app hardening settings.

---

## 📑 Table of Contents
- [1. How P2P Voice & Video Calls Leak IPs](#1-how-p2p-voice--video-calls-leak-ips)
  - [1.1 P2P Direct Media vs. Server Relayed](#11-p2p-direct-media-vs-server-relayed)
  - [1.2 The STUN Protocol Mechanics](#12-the-stun-protocol-mechanics)
- [2. The Wireshark STUN Sniffing Mechanics](#2-the-wireshark-stun-sniffing-mechanics)
  - [2.1 The Exact Wireshark Filters](#21-the-exact-wireshark-filters)
  - [2.2 XOR-MAPPED-ADDRESS Inspection](#22-xor-mapped-address-inspection)
- [3. Complete App-by-App Hardening Guide](#3-complete-app-by-app-hardening-guide)
  - [3.1 WhatsApp: Protect IP Address in Calls](#31-whatsapp-hardening)
  - [3.2 Telegram: Disabling P2P Calls](#32-telegram-hardening)
  - [3.3 Signal: Always Relay Calls](#33-signal-hardening)
  - [3.4 Discord: Voice Architecture & Link Leak Vectors](#34-discord-architecture--link-leaks)
  - [3.5 Steam & Gaming: Steam Datagram Relay (SDR)](#35-steam--gaming-lobbies)

---

## 1. How P2P Voice & Video Calls Leak IPs

### 1.1 P2P Direct Media vs. Server Relayed
When two users initiate a voice or video call on a messaging app, the platform chooses one of two connection architectures:

```mermaid
flowchart TD
    P1["Caller Client"] <-->|Direct UDP Stream<br/>(Public IP Exposed)| P2["Recipient Client"]
    R1["Hardened Caller"] <-->|Encrypted Relay| Srv["Server Relay Gateway<br/>(Meta / Telegram)"]
    Srv <-->|Encrypted Relay| R2["Hardened Recipient<br/>(IP Protected)"]
```

* **Direct P2P (Low Latency / High Risk)**: Audio/video packets travel directly between Caller IP and Recipient IP over UDP. Anyone running Wireshark on either machine can read the other party's public IP address in real time.
* **Server-Relayed (High Privacy)**: Both users send encrypted media packets to the platform's central media gateway. Neither user ever sees the other party's IP address.

### 1.2 The STUN Protocol Mechanics
Because most consumer devices sit behind NAT routers with private IPs (`192.168.x.x`), WebRTC and VoIP applications use **STUN (Session Traversal Utilities for NAT - RFC 5389 / RFC 8489)**:
1. Device sends a **STUN Binding Request** (`0x0001`) to a public STUN server.
2. The STUN server observes the public source IP and port assigned by the router's NAT.
3. The server sends back a **STUN Binding Response** (`0x0101`) containing the device's public IP inside the `XOR-MAPPED-ADDRESS` attribute.
4. The messaging app exchanges this candidate address with the peer to establish direct UDP media flow.

---

## 2. The Wireshark STUN Sniffing Mechanics

Adversaries use Wireshark to capture network interface traffic while triggering a direct call or gaming session.

### 2.1 The Exact Wireshark Filters

| Wireshark Filter | What It Captures | Purpose |
| :--- | :--- | :--- |
| `stun` | All STUN packets | Catches all NAT traversal signaling |
| `stun.type == 0x0001` | STUN Binding Requests | Outgoing requests to discover mapped public endpoints |
| `stun.type == 0x0101` | STUN Binding Success Responses | Server responses containing mapped public addresses |
| `stun.att.type == 0x0020` | `XOR-MAPPED-ADDRESS` Attribute | Inspects the decoded public IP attribute |
| `classicstun` | Legacy RFC 3489 STUN packets | Catches older legacy gaming lobbies |
| `udp and not dns and not dhcp` | High-volume UDP audio streams | Identifies direct RTP/SRTP voice streams between hosts |

### 2.2 XOR-MAPPED-ADDRESS Inspection
Inside Wireshark's Packet Details pane:
```
Session Traversal Utilities for NAT
    Message Header
        Message Type: Binding Success Response (0x0101)
        Message Length: 32
        Message Cookie: 2112a442
        Message Transaction ID: 894a3c21...
    Attributes
        XOR-MAPPED-ADDRESS
            Reserved: 00
            Protocol Family: IPv4 (0x01)
            Port (XOR-d): 52140
            IP (XOR-d): 203.0.113.42  <--- [ TARGET'S REAL PUBLIC IP EXTRACTED ]
```

---

## 3. Complete App-by-App Hardening Guide

Protect yourself from Wireshark sniffing by enforcing **Server Relaying** across all communication apps.

---

### 3.1 WhatsApp Hardening

By default, WhatsApp 1-on-1 voice and video calls establish direct P2P connections to minimize latency, exposing your public IP to the caller.

> [!IMPORTANT]
> **To Block IP Pulling on WhatsApp**:
> 1. Open WhatsApp -> **Settings** -> **Privacy**.
> 2. Scroll to the bottom and tap **Advanced**.
> 3. Toggle **"Protect IP Address in Calls"** to **ON**.

```
[ WhatsApp Settings ] ➔ [ Privacy ] ➔ [ Advanced ] ➔ [ Protect IP Address in Calls: ENABLED ]
```
* **Result**: All calls are securely relayed through WhatsApp / Meta servers. The caller's packet capture will only show Meta's server IP.

---

### 3.2 Telegram Hardening

By default, Telegram allows peer-to-peer calls between contacts.

> [!IMPORTANT]
> **To Block IP Pulling on Telegram**:
> 1. Open Telegram -> **Settings** -> **Privacy and Security**.
> 2. Tap **Calls**.
> 3. Under **Peer-to-Peer**, select **"Nobody"** (or "My Contacts" only).
> 4. Go back to Privacy -> Tap **Phone Number** -> Set to **"Nobody"** -> Set *"Who can find me by my number"* to **"My Contacts"**.

```
[ Telegram Settings ] ➔ [ Privacy and Security ] ➔ [ Calls ] ➔ [ Peer-to-Peer: NOBODY ]
```
* **Result**: All Telegram calls are forced through Telegram's encrypted relay infrastructure.

---

### 3.3 Signal Hardening

Signal provides an explicit option to prevent IP exposure to callers.

> [!IMPORTANT]
> **To Block IP Pulling on Signal**:
> 1. Open Signal -> **Settings** -> **Privacy**.
> 2. Tap **Advanced**.
> 3. Toggle **"Always Relay Calls"** to **ON**.

* **Result**: Audio and video streams are always proxied through Signal servers.

---

### 3.4 Discord: Architecture & Link Leaks

#### Does Discord Leak IPs on Voice Calls?
* **Voice Channels & Direct Call DMs**: **NO.** Discord routes all voice and video calls through centralized Discord Voice Gateways (WebSockets & WebRTC to Discord IP blocks `66.22.x.x` / `162.159.x.x`). Running Wireshark during a Discord call will only show Discord's gateway server IP.

#### Where Discord CAN Leak Your IP:
1. **Uncached External Links / Custom Rich Presence**: Clicking direct external links in DMs or loading assets from unverified custom bot bots.
2. **Third-Party Modified Clients (Vencord, BetterDiscord)**: Untrusted plugins that fetch external assets outside of Discord's image proxy (`media.discordapp.net`).

---

### 3.5 Steam & Gaming Lobbies (Steam Datagram Relay)

Older games connected players directly via P2P UDP lobbies. Modern Source 2 and Steamworks games utilize **Steam Datagram Relay (SDR)**.

> [!TIP]
> **To Enforce Relay Routing in Steam**:
> 1. Open Steam -> **Settings** -> **In-Game**.
> 2. Look for **Steam Networking** / **Client Relay**.
> 3. Set to **"Always Relay"** or **"Default"**.

---

## 🔒 Summary Hardening Matrix

| Application | Vulnerable Default? | Required Privacy Setting | Resulting Protection |
| :--- | :---: | :--- | :--- |
| **WhatsApp** | ⚠️ Yes (P2P on 1-on-1) | Settings ➔ Privacy ➔ Advanced ➔ **Protect IP Address in Calls** | 🛡️ Relayed via Meta Servers |
| **Telegram** | ⚠️ Yes (P2P enabled) | Settings ➔ Privacy ➔ Calls ➔ **Peer-to-Peer: NOBODY** | 🛡️ Relayed via Telegram Servers |
| **Signal** | ⚠️ Yes (Direct P2P) | Settings ➔ Privacy ➔ Advanced ➔ **Always Relay Calls** | 🛡️ Relayed via Signal Servers |
| **Discord** | 🛡️ Safe on Voice | Keep official client & avoid untrusted external links | 🛡️ Centralized Gateway Default |
| **Steam Games** | ⚠️ Depends on Game | Steam Settings ➔ In-Game ➔ **Steam Networking: Always Relay** | 🛡️ SDR Datagram Relay |

---

<div align="center">
  <sub>Published and maintained by <a href="https://github.com/DaddyZyn"><b>DaddyZyn (DRAXO.dev)</b></a></sub>
</div>
