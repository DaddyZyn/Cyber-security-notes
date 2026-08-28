#!/usr/bin/env python3
"""
ARP Poisoning & MITM Sentinel
Author: DaddyZyn (DRAXO.dev)
Repo: https://github.com/DaddyZyn/Cyber-security-notes

Monitors the local operating system ARP cache in real-time
to detect duplicate MAC collisions and gateway poisoning attacks.
"""

import sys
import time
import subprocess
import platform
import re
import argparse

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
   _   ___ ___  __      ___ _____ ___ _  _ 
  /_\\ | _ \\ _ \\ \\ \\    / /_\\_   _/ __| || |
 / _ \\|   /  _/  \\ \\/\\/ / _ \\| || (__| __ |
/_/ \\_\\_|_\\_|     \\_/\\_/_/ \\_\\_| \\___|_||_|
  {Colors.RESET}{Colors.BOLD}Real-Time ARP Poisoning & MITM Sentinel // DaddyZyn (DRAXO.dev){Colors.RESET}
"""
    print(banner)

def get_arp_table():
    """Parses system ARP table across Windows, Linux, and macOS."""
    system = platform.system()
    table = {}
    
    try:
        if system == "Windows":
            out = subprocess.check_output("arp -a", text=True, errors="ignore")
            # Matches: 192.168.1.1   00-11-22-33-44-55   dynamic
            for line in out.split("\n"):
                match = re.search(r'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\s+([0-9a-fA-F\-]{17})\s+(\w+)', line)
                if match:
                    ip = match.group(1)
                    mac = match.group(2).replace("-", ":").lower()
                    entry_type = match.group(3)
                    # Ignore broadcast / multicast
                    if not ip.startswith("224.") and not ip.startswith("239.") and not ip.endswith(".255"):
                        table[ip] = mac
        else: # Linux / Darwin
            out = subprocess.check_output("arp -n", text=True, errors="ignore")
            for line in out.split("\n"):
                match = re.search(r'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\s+.*\s+([0-9a-fA-F:]{17})', line)
                if match:
                    ip = match.group(1)
                    mac = match.group(2).lower()
                    if mac != "<incomplete>":
                        table[ip] = mac
    except Exception as e:
        print(f"{Colors.RED}[-] Error reading ARP table: {e}{Colors.RESET}")
        
    return table

def analyze_arp_table(table, previous_table=None):
    """Detects MAC collisions and suspicious mutations."""
    mac_to_ips = {}
    for ip, mac in table.items():
        if mac not in mac_to_ips:
            mac_to_ips[mac] = []
        mac_to_ips[mac].append(ip)
    
    alerts = []
    
    # 1. Check for Duplicate MAC Collisions (Classic arpspoof signature)
    for mac, ips in mac_to_ips.items():
        if len(ips) > 1:
            alerts.append(
                f"{Colors.RED}[!] CRITICAL ALERT: MAC Collision Detected!{Colors.RESET}\n"
                f"    {Colors.YELLOW}MAC Address: {mac}{Colors.RESET}\n"
                f"    {Colors.YELLOW}Claiming IPs: {', '.join(ips)}{Colors.RESET}\n"
                f"    {Colors.RED}Threat: An attacker may be actively poisoning the local ARP cache.{Colors.RESET}"
            )
            
    # 2. Check for Gateway / Host MAC Mutation
    if previous_table:
        for ip, mac in table.items():
            if ip in previous_table and previous_table[ip] != mac:
                alerts.append(
                    f"{Colors.RED}[!] WARNING: IP Address MAC Changed!{Colors.RESET}\n"
                    f"    {Colors.CYAN}Target IP:   {ip}{Colors.RESET}\n"
                    f"    {Colors.YELLOW}Previous MAC: {previous_table[ip]}{Colors.RESET}\n"
                    f"    {Colors.RED}New MAC:      {mac}{Colors.RESET}"
                )
                
    return alerts

def main():
    parser = argparse.ArgumentParser(description="ARP Poisoning & MITM Sentinel")
    parser.add_argument("--watch", "-w", action="store_true", help="Run in continuous monitoring loop")
    parser.add_argument("--interval", "-i", type=int, default=3, help="Polling interval in seconds (default: 3)")
    args = parser.parse_args()
    
    print_banner()
    
    current_table = get_arp_table()
    print(f"{Colors.BOLD}[*] Initializing baseline ARP cache snapshot ({len(current_table)} hosts indexed)...{Colors.RESET}")
    for ip, mac in sorted(current_table.items()):
        print(f"  {Colors.CYAN}> {ip.ljust(16)}{Colors.RESET} -> {mac}")
        
    initial_alerts = analyze_arp_table(current_table)
    if initial_alerts:
        print(f"\n{Colors.RED}[!] ANOMALIES FOUND ON STARTUP:{Colors.RESET}")
        for alert in initial_alerts:
            print(alert)
    else:
        print(f"\n{Colors.GREEN}[+] Initial ARP table clean. No MAC collisions detected.{Colors.RESET}")
        
    if not args.watch:
        print(f"\n{Colors.BOLD}Tip: Run with '{Colors.CYAN}--watch{Colors.RESET}{Colors.BOLD}' for continuous real-time MITM monitoring.{Colors.RESET}\n")
        return
        
    print(f"\n{Colors.BOLD}[*] Starting real-time sentinel (Polling every {args.interval}s, Press Ctrl+C to stop)...{Colors.RESET}")
    previous_table = current_table
    
    try:
        while True:
            time.sleep(args.interval)
            new_table = get_arp_table()
            alerts = analyze_arp_table(new_table, previous_table)
            if alerts:
                timestamp = time.strftime("%H:%M:%S")
                print(f"\n{Colors.BOLD}[{timestamp}] {Colors.RED}!!! SUSPICIOUS ARP ACTIVITY !!!{Colors.RESET}")
                for alert in alerts:
                    print(alert)
            previous_table = new_table
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[*] Sentinel monitoring stopped by user.{Colors.RESET}\n")

if __name__ == "__main__":
    main()
