#!/usr/bin/env python3
"""
DNS Tunneling & Shannon Entropy Analyzer
Author: DaddyZyn (DRAXO.dev)
Repo: https://github.com/DaddyZyn/Cyber-security-notes

Calculates the Shannon Entropy of domain strings and subdomains
to detect covert DNS tunneling (dnscat2/iodine) and DGA botnets.
"""

import sys
import math
import argparse
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def print_banner():
    banner = f"""{Colors.BOLD}{Colors.CYAN}
  ___  _  _ ___   ___ _  _ _____ ___  ___ _____   __
 |   \\| \\| / __| | __| \\| |_   _| _ \\/ _ \\ _ \\ \\ / /
 | |) | .` \\__ \\ | _|| .` | | | |   / (_) |  _/\\ V / 
 |___/|_|\\_|___/ |___|_|\\_| |_| |_|_\\\\___/|_|   |_|  
  {Colors.RESET}{Colors.BOLD}Shannon Entropy & DNS Exfiltration Analyzer // DaddyZyn (DRAXO.dev){Colors.RESET}
"""
    print(banner)

def calculate_shannon_entropy(string):
    """Calculates Shannon Entropy: H(X) = -sum(P(x) * log2(P(x)))"""
    if not string:
        return 0.0
    length = len(string)
    counts = Counter(string)
    entropy = 0.0
    for count in counts.values():
        prob = count / length
        entropy -= prob * math.log2(prob)
    return entropy

def analyze_domain(domain):
    domain = domain.strip().lower()
    if not domain:
        return

    parts = domain.split(".")
    subdomain = ".".join(parts[:-2]) if len(parts) > 2 else parts[0]
    
    full_entropy = calculate_shannon_entropy(domain)
    sub_entropy = calculate_shannon_entropy(subdomain) if subdomain else full_entropy

    # Evaluation Thresholds
    is_suspicious = False
    reasons = []

    if len(domain) > 65:
        is_suspicious = True
        reasons.append(f"Abnormal FQDN Length ({len(domain)} chars > 65)")

    if len(subdomain) > 40:
        is_suspicious = True
        reasons.append(f"Excessive Subdomain Length ({len(subdomain)} chars > 40)")

    if sub_entropy > 4.2:
        is_suspicious = True
        reasons.append(f"High Subdomain Entropy ({sub_entropy:.2f} bits/char > 4.20)")
    elif sub_entropy > 3.7 and len(subdomain) > 25:
        is_suspicious = True
        reasons.append(f"Elevated Entropy with Long Payload ({sub_entropy:.2f} bits/char)")

    print(f"\n{Colors.BOLD}[*] Domain Analysis: {Colors.CYAN}{domain}{Colors.RESET}")
    print(f"  {Colors.BOLD}Subdomain Payload:{Colors.RESET}   {subdomain if subdomain else '(None)'}")
    print(f"  {Colors.BOLD}Total Length:{Colors.RESET}        {len(domain)} chars")
    print(f"  {Colors.BOLD}Subdomain Length:{Colors.RESET}    {len(subdomain)} chars")
    print(f"  {Colors.BOLD}Domain Entropy:{Colors.RESET}      {full_entropy:.3f} bits/char")
    print(f"  {Colors.BOLD}Subdomain Entropy:{Colors.RESET}   {sub_entropy:.3f} bits/char")

    if is_suspicious:
        print(f"  {Colors.BOLD}Verdict:{Colors.RESET}            {Colors.RED}[!] HIGH-RISK: Potential DNS Tunnel / DGA Exfil!{Colors.RESET}")
        for r in reasons:
            print(f"    {Colors.YELLOW}- {r}{Colors.RESET}")
    else:
        print(f"  {Colors.BOLD}Verdict:{Colors.RESET}            {Colors.GREEN}[+] BENIGN: Normal human-readable / CDN domain.{Colors.RESET}")

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="Shannon Entropy & DNS Tunneling Analyzer")
    parser.add_argument("domain", nargs="?", default="a7f93b8c2d1e04b8921a8f90c3e.tunnel.darknet-c2.net", help="Domain to analyze")
    args = parser.parse_args()
    
    analyze_domain(args.domain)
    
    # Also test a normal benign domain for contrast
    print(f"\n{Colors.BOLD}--- Comparative Baseline Example ---{Colors.RESET}")
    analyze_domain("api.github.com")
    print()

if __name__ == "__main__":
    main()
