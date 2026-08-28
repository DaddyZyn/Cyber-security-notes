#!/usr/bin/env python3
"""
OPSEC & Network Leak Auditor
Author: DaddyZyn (DRAXO.dev)
Repo: https://github.com/DaddyZyn/Cyber-security-notes

Audits the local system for network leaks, DNS configuration,
outbound SMB port exposure, and IPv6 dual-stack fallback risks.
"""

import sys
import os
import socket
import subprocess
import platform
import json
import urllib.request

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def print_banner():
    banner = f"""{Colors.BOLD}{Colors.CYAN}
   ___  ___  ___ ___ ___     _   _   _ ___ ___ _____ ___  ___ 
  / _ \\| _ \\/ __| __/ __|   /_\\ | | | |   \\_ _|_   _/ _ \\| _ \\
 | (_) |  _/\\__ \\ _| (__   / _ \\| |_| | |) | |  | || (_) |   /
  \\___/|_|  |___/___\\___| /_/ \\_\\\\___/|___/___| |_| \\___/|_|_\\
  {Colors.RESET}{Colors.BOLD}Local Endpoint & Network Leak Audit Tool // DaddyZyn (DRAXO.dev){Colors.RESET}
"""
    print(banner)

def check_public_ip():
    print(f"{Colors.BOLD}[*] Probing Outbound Network Identity & GeoIP...{Colors.RESET}")
    try:
        req = urllib.request.Request(
            "https://ipinfo.io/json",
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            ip = data.get("ip", "Unknown")
            org = data.get("org", "Unknown")
            city = data.get("city", "Unknown")
            country = data.get("country", "Unknown")
            
            print(f"  {Colors.CYAN}> Public IP:{Colors.RESET} {Colors.BOLD}{ip}{Colors.RESET}")
            print(f"  {Colors.CYAN}> ISP / ASN:{Colors.RESET} {org}")
            print(f"  {Colors.CYAN}> Location:{Colors.RESET}  {city}, {country}")
            
            org_lower = org.lower()
            if any(k in org_lower for k in ["mullvad", "datacenter", "hosting", "ovh", "digitalocean", "linode", "m247"]):
                print(f"  {Colors.GREEN}[+] Network appears to be routed through a VPN / Hosting Provider.{Colors.RESET}")
            else:
                print(f"  {Colors.YELLOW}[!] Warning: ISP looks like a residential/consumer broadband connection.{Colors.RESET}")
    except Exception as e:
        print(f"  {Colors.RED}[-] Could not reach external GeoIP lookup: {e}{Colors.RESET}")

def check_outbound_smb():
    print(f"\n{Colors.BOLD}[*] Testing Outbound SMB (Port 445) UNC Leak Vulnerability...{Colors.RESET}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2.0)
    result = sock.connect_ex(("1.1.1.1", 445))
    sock.close()
    
    if result == 0:
        print(f"  {Colors.RED}[!] CRITICAL: Outbound TCP Port 445 is OPEN!{Colors.RESET}")
        print(f"      {Colors.YELLOW}Your system is vulnerable to forced UNC path NetNTLMv2 hash theft.{Colors.RESET}")
        print(f"      {Colors.CYAN}Remediation: Block TCP Port 445 outbound on your router/firewall.{Colors.RESET}")
    else:
        print(f"  {Colors.GREEN}[+] SECURE: Outbound TCP Port 445 is BLOCKED or Filtered.{Colors.RESET}")

def check_ipv6_status():
    print(f"\n{Colors.BOLD}[*] Checking IPv6 Dual-Stack Leak Status...{Colors.RESET}")
    try:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        sock.settimeout(2.0)
        sock.connect(("2001:4860:4860::8888", 53))
        local_ipv6 = sock.getsockname()[0]
        sock.close()
        print(f"  {Colors.YELLOW}[!] IPv6 is ACTIVE: Local IPv6 address is {local_ipv6}{Colors.RESET}")
        print(f"      {Colors.YELLOW}If your VPN does not route IPv6, traffic may bypass the tunnel.{Colors.RESET}")
    except Exception:
        print(f"  {Colors.GREEN}[+] SECURE: IPv6 outbound route is inactive or disabled.{Colors.RESET}")

def check_dns_resolver():
    print(f"\n{Colors.BOLD}[*] Inspecting Active DNS Server Bindings...{Colors.RESET}")
    system = platform.system()
    try:
        if system == "Windows":
            out = subprocess.check_output("ipconfig /all", text=True, errors="ignore")
            dns_lines = [line.strip() for line in out.split("\n") if "DNS Servers" in line or "192.168" in line or "10." in line]
            for line in dns_lines[:4]:
                print(f"  {Colors.CYAN}> {line}{Colors.RESET}")
        elif system in ["Linux", "Darwin"]:
            with open("/etc/resolv.conf", "r") as f:
                for line in f:
                    if line.startswith("nameserver"):
                        print(f"  {Colors.CYAN}> {line.strip()}{Colors.RESET}")
    except Exception as e:
        print(f"  {Colors.RED}[-] Could not query DNS bindings: {e}{Colors.RESET}")

def main():
    print_banner()
    check_public_ip()
    check_outbound_smb()
    check_ipv6_status()
    check_dns_resolver()
    print(f"\n{Colors.BOLD}{Colors.GREEN}[+] OPSEC & Network Leak Audit Completed.{Colors.RESET}\n")

if __name__ == "__main__":
    main()
