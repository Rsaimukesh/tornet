#!/usr/bin/env python3
"""
TorNet Dynamic IP Demo - Shows exactly how IP changing works
"""

import requests
import time
import subprocess
import os
import sys

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
WHITE = "\033[97m"
CYAN = "\033[96m"
RESET = "\033[0m"

def get_current_ip():
    """Get current public IP address"""
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        return response.text.strip()
    except:
        return "Unable to fetch"

def get_ip_info(ip):
    """Get detailed IP information"""
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'country': data.get('country', 'Unknown'),
                'city': data.get('city', 'Unknown'), 
                'isp': data.get('org', 'Unknown')
            }
    except:
        pass
    return {'country': 'Unknown', 'city': 'Unknown', 'isp': 'Unknown'}

def demo_ip_changing():
    print(f"""{CYAN}
╔══════════════════════════════════════════════════════╗
║              TorNet Dynamic IP Demo                  ║
║          Shows How IP Changing Really Works          ║
╚══════════════════════════════════════════════════════╝{RESET}""")

    print(f"\n{YELLOW}🔍 STEP 1: Check Your Current IP{RESET}")
    current_ip = get_current_ip()
    ip_info = get_ip_info(current_ip)
    
    print(f"{WHITE}Current IP: {GREEN}{current_ip}{RESET}")
    print(f"{WHITE}Location: {CYAN}{ip_info['city']}, {ip_info['country']}{RESET}")
    print(f"{WHITE}ISP: {CYAN}{ip_info['isp']}{RESET}")

    print(f"\n{YELLOW}🌐 HOW TORNET CHANGES YOUR IP DYNAMICALLY:{RESET}")
    print(f"""
{GREEN}1. AUTOMATIC IP ROTATION:{RESET}
   • TorNet connects to Tor network
   • Changes exit nodes at specified intervals
   • Each exit node = Different IP address
   • Shows you each new IP as it changes

{GREEN}2. TIMING CONTROL:{RESET}
   • --interval 30    → Change every 30 seconds
   • --interval 60    → Change every minute  
   • --interval 10-120 → Random intervals
   
{GREEN}3. SESSION CONTROL:{RESET}
   • --count 5  → Change IP exactly 5 times
   • --count 0  → Keep changing forever
   • --count 50 → Long session (50 changes)

{GREEN}4. GEOGRAPHIC CONTROL:{RESET}
   • --countries us     → US IPs only
   • --countries de,fr  → German/French IPs
   • No flag            → Random countries
""")

    print(f"\n{YELLOW}📋 READY-TO-RUN COMMANDS:{RESET}")
    
    commands = [
        ("Test Current IP", "python3 -m tornet.tornet --ip"),
        ("Quick Test (3 changes)", "python3 -m tornet.tornet --interval 30 --count 3"),
        ("Medium Session", "python3 -m tornet.tornet --interval 60 --count 10"),
        ("Infinite Mode", "python3 -m tornet.tornet --interval 120 --count 0"),
        ("US Only IPs", "python3 -m tornet.tornet --countries us --count 5"),
        ("Security Check", "python3 -m tornet.tornet --security-check"),
        ("Stop All Services", "python3 -m tornet.tornet --stop"),
    ]
    
    for desc, cmd in commands:
        print(f"\n{CYAN}• {desc}:{RESET}")
        print(f"  {YELLOW}{cmd}{RESET}")

    print(f"\n{YELLOW}🚀 WHAT HAPPENS WHEN YOU RUN IT:{RESET}")
    print(f"""
{WHITE}Example Session Output:{RESET}
{GREEN}[+] Tor service started. Please wait a minute for Tor to connect.
[+] Your IP has been changed to: 185.220.101.32 (Germany)
[+] Your IP has been changed to: 199.87.154.255 (USA) 
[+] Your IP has been changed to: 109.70.100.34 (Netherlands)
[+] Your IP has been changed to: 77.247.181.165 (Romania){RESET}

{CYAN}Each line shows:{RESET}
• New IP address
• Usually from different countries
• Changes automatically at your interval
• Continues for your specified count
""")

    print(f"\n{YELLOW}🔥 QUICK START - TRY THIS NOW:{RESET}")
    print(f"""
{GREEN}For a quick demo:{RESET}
{YELLOW}cd /home/sai/tornet{RESET}
{YELLOW}python3 -m tornet.tornet --interval 30 --count 3{RESET}

{WHITE}This will:{RESET}
• Change your IP 3 times
• Wait 30 seconds between changes  
• Show each new IP address
• Stop automatically after 3 changes

{RED}Note: Requires Tor to be installed and running{RESET}
{CYAN}Auto-install: python3 -m tornet.tornet --auto-fix{RESET}
""")

if __name__ == "__main__":
    demo_ip_changing()
