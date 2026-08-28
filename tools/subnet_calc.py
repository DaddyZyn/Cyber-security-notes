#!/usr/bin/env python3
"""
CIDR & Subnet Mask Bitwise Calculator
Author: DaddyZyn (DRAXO.dev)
Repo: https://github.com/DaddyZyn/Cyber-security-notes

Calculates binary masks, network IDs, broadcast addresses,
and usable host ranges from CIDR prefix notations.
"""

import sys
import ipaddress
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
  ___ _   _ ___ _  _ ___ _____   ___   _   _    ___ 
 / __| | | | _ ) \\| | __|_   _| / __| /_\\ | |  / __|
 \\__ \\ |_| | _ \\ .` | _|  | |  | (__ / _ \\| |__| (__ 
 |___/\\___/|___/_|\\_|___| |_|   \\___/_/ \\_\\____|\\___|
  {Colors.RESET}{Colors.BOLD}CIDR & Subnet Bitwise Calculator // DaddyZyn (DRAXO.dev){Colors.RESET}
"""
    print(banner)

def to_binary_dotted(ip_int):
    binary_str = f"{ip_int:032b}"
    return ".".join([binary_str[i:i+8] for i in range(0, 32, 8)])

def calculate_subnet(cidr_str):
    try:
        net = ipaddress.ip_network(cidr_str, strict=False)
    except ValueError as e:
        print(f"{Colors.RED}[-] Invalid CIDR format: {e}{Colors.RESET}")
        return

    netmask_int = int(net.netmask)
    wildcard_int = int(net.hostmask)
    net_addr_int = int(net.network_address)
    broadcast_int = int(net.broadcast_address)

    # Classification
    if net.is_private:
        scope = f"{Colors.GREEN}RFC 1918 Private Subnet (LAN Only){Colors.RESET}"
    elif net.is_loopback:
        scope = f"{Colors.YELLOW}Loopback Range (127.0.0.0/8){Colors.RESET}"
    elif net.is_link_local:
        scope = f"{Colors.YELLOW}Link-Local / APIPA (169.254.0.0/16){Colors.RESET}"
    else:
        scope = f"{Colors.CYAN}Public Routable Internet Space{Colors.RESET}"

    total_hosts = net.num_addresses
    usable_hosts = total_hosts - 2 if total_hosts > 2 else total_hosts

    first_host = net.network_address + 1 if total_hosts > 2 else net.network_address
    last_host = net.broadcast_address - 1 if total_hosts > 2 else net.broadcast_address

    print(f"\n{Colors.BOLD}[*] Subnet Breakdown for {Colors.CYAN}{cidr_str}{Colors.RESET}:")
    print(f"  {Colors.BOLD}Scope:{Colors.RESET}             {scope}")
    print(f"  {Colors.BOLD}CIDR Prefix:{Colors.RESET}       /{net.prefixlen}")
    print(f"  {Colors.BOLD}Network ID:{Colors.RESET}        {Colors.CYAN}{net.network_address}{Colors.RESET}")
    print(f"  {Colors.BOLD}Subnet Mask:{Colors.RESET}       {net.netmask}")
    print(f"  {Colors.BOLD}Wildcard Mask:{Colors.RESET}     {net.hostmask}")
    print(f"  {Colors.BOLD}Broadcast IP:{Colors.RESET}      {net.broadcast_address}")
    print(f"  {Colors.BOLD}Usable Host Range:{Colors.RESET} {Colors.GREEN}{first_host}{Colors.RESET} - {Colors.GREEN}{last_host}{Colors.RESET}")
    print(f"  {Colors.BOLD}Total Addresses:{Colors.RESET}   {total_hosts:,}")
    print(f"  {Colors.BOLD}Usable Hosts:{Colors.RESET}      {Colors.GREEN}{usable_hosts:,}{Colors.RESET}")
    
    print(f"\n{Colors.BOLD}[*] Binary Bitmask Architecture:{Colors.RESET}")
    print(f"  {Colors.CYAN}Network Address:{Colors.RESET}  {to_binary_dotted(net_addr_int)}")
    print(f"  {Colors.CYAN}Subnet Mask:{Colors.RESET}      {to_binary_dotted(netmask_int)}")
    print(f"  {Colors.CYAN}Wildcard Mask:{Colors.RESET}    {to_binary_dotted(wildcard_int)}")
    print(f"  {Colors.CYAN}Broadcast Address:{Colors.RESET}{to_binary_dotted(broadcast_int)}\n")

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="Subnet & CIDR Bitwise Calculator")
    parser.add_argument("cidr", nargs="?", default="192.168.1.0/24", help="CIDR string (e.g. 10.0.0.0/8, 192.168.1.50/24)")
    args = parser.parse_args()
    calculate_subnet(args.cidr)

if __name__ == "__main__":
    main()
