#!/usr/bin/env python3
"""
TorNet - Quick Start Guide and Demo
This shows you exactly how to run TorNet for dynamic IP changing
"""

import subprocess
import time
import sys
import os

# Color codes for better output
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
WHITE = "\033[97m"
CYAN = "\033[96m"
RESET = "\033[0m"

def print_banner():
    print(f"""
{CYAN}╔══════════════════════════════════════════════════════════════╗
║                     {WHITE}TorNet Quick Start Guide{CYAN}                     ║
║              {YELLOW}Dynamic IP Changing with Tor Network{CYAN}              ║
╚══════════════════════════════════════════════════════════════╝{RESET}
""")

def print_section(title):
    print(f"\n{BLUE}{'='*60}")
    print(f"{WHITE}{title}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

def run_command_demo(cmd, description):
    print(f"\n{CYAN}[DEMO]{RESET} {description}")
    print(f"{YELLOW}Command:{RESET} {cmd}")
    print(f"{GREEN}➤{RESET} This will: {description}")
    print(f"{WHITE}{'─'*50}{RESET}")

def main():
    print_banner()
    
    print_section("🚀 HOW TO RUN TORNET FOR DYNAMIC IP CHANGING")
    
    print(f"""
{GREEN}TorNet automatically changes your IP address through the Tor network.{RESET}
{WHITE}Yes, it changes IP dynamically at specified intervals!{RESET}

{CYAN}Prerequisites:{RESET}
1. Install Tor: sudo apt install tor (Ubuntu/Debian) or sudo pacman -S tor (Arch)
2. Install TorNet: pip install python-tornet==2.2.0
3. Or run from source: python3 -m tornet.tornet [options]
""")

    print_section("📋 BASIC USAGE EXAMPLES")
    
    examples = [
        ("python3 -m tornet.tornet", "Default: Change IP 10 times, every 60 seconds"),
        ("python3 -m tornet.tornet --interval 30 --count 5", "Change IP 5 times, every 30 seconds"),
        ("python3 -m tornet.tornet --interval 120 --count 0", "Change IP every 2 minutes INFINITELY"),
        ("python3 -m tornet.tornet --interval 10-60 --count 20", "Random interval 10-60 seconds, 20 changes"),
        ("python3 -m tornet.tornet --countries us,de,fr", "Use only US, German, French exit nodes"),
    ]
    
    for cmd, desc in examples:
        run_command_demo(cmd, desc)
    
    print_section("🔧 SECURITY & MONITORING COMMANDS")
    
    security_examples = [
        ("python3 -m tornet.tornet --ip", "Check current IP address"),
        ("python3 -m tornet.tornet --ip-info", "Detailed IP location & ISP info"),
        ("python3 -m tornet.tornet --dns-leak-test", "Test for DNS leaks (security check)"),
        ("python3 -m tornet.tornet --security-check", "Complete security analysis"),
        ("python3 -m tornet.tornet --stop", "Stop all Tor services"),
    ]
    
    for cmd, desc in security_examples:
        run_command_demo(cmd, desc)
    
    print_section("⚡ QUICK START - TRY NOW!")
    
    print(f"""
{GREEN}1. BASIC TEST:{RESET}
   {YELLOW}python3 -m tornet.tornet --ip{RESET}
   Shows your current IP address
   
{GREEN}2. CHANGE IP 3 TIMES (30 second intervals):{RESET}
   {YELLOW}python3 -m tornet.tornet --interval 30 --count 3{RESET}
   Perfect for testing!
   
{GREEN}3. INFINITE IP CHANGING:{RESET}
   {YELLOW}python3 -m tornet.tornet --interval 60 --count 0{RESET}
   Changes IP every minute forever (Ctrl+C to stop)
   
{GREEN}4. SECURITY CHECK:{RESET}
   {YELLOW}python3 -m tornet.tornet --security-check{RESET}
   Comprehensive security analysis
""")

    print_section("🌍 ADVANCED FEATURES")
    
    print(f"""
{CYAN}Country-Specific Exit Nodes:{RESET}
• --countries us          → Only US exit nodes
• --countries us,de,fr    → US, German, French nodes
• --countries jp,kr       → Asian nodes (Japan, Korea)

{CYAN}Flexible Intervals:{RESET}
• --interval 60           → Fixed 60 seconds
• --interval 30-120       → Random between 30-120 seconds
• --interval 10           → Fast 10-second changes

{CYAN}Count Options:{RESET}
• --count 5               → Change IP exactly 5 times
• --count 0               → Change IP infinitely
• --count 100             → Long session (100 changes)
""")

    print_section("📊 WHAT HAPPENS WHEN YOU RUN IT")
    
    print(f"""
{GREEN}When you run TorNet, it will:{RESET}

1. {CYAN}Check & Install Dependencies{RESET} - Tor, Python packages
2. {CYAN}Start Tor Service{RESET} - Connects to Tor network
3. {CYAN}Display Current IP{RESET} - Shows your new anonymous IP
4. {CYAN}Begin IP Rotation{RESET} - Changes IP at your specified intervals
5. {CYAN}Show Each Change{RESET} - Displays new IP each time it changes

{YELLOW}Example Output:{RESET}
{WHITE}[+] Tor service started. Please wait a minute for Tor to connect.
[+] Your IP has been changed to: 185.220.101.32
[+] Your IP has been changed to: 199.87.154.255
[+] Your IP has been changed to: 109.70.100.34{RESET}
""")

    print_section("🛡️ SECURITY TIPS")
    
    print(f"""
{RED}IMPORTANT SECURITY NOTES:{RESET}

• {CYAN}Always test for DNS leaks:{RESET} python3 -m tornet.tornet --dns-leak-test
• {CYAN}Use Tor Browser for browsing{RESET} - Don't use regular browsers
• {CYAN}Configure system DNS{RESET} - Point to 127.0.0.1:9053 (Tor DNS)
• {CYAN}Regular security checks{RESET} - Run --security-check periodically

{GREEN}Pro Tips:{RESET}
• Start with short sessions to test: --count 3
• Use random intervals for better anonymity: --interval 30-300
• Different countries for different purposes: --countries us,de
""")

    print_section("🚨 TROUBLESHOOTING")
    
    print(f"""
{YELLOW}If TorNet doesn't work:{RESET}

1. {CYAN}Auto-fix issues:{RESET} python3 -m tornet.tornet --auto-fix
2. {CYAN}Check Tor installation:{RESET} which tor
3. {CYAN}Check Tor status:{RESET} sudo systemctl status tor
4. {CYAN}Restart Tor:{RESET} sudo systemctl restart tor
5. {CYAN}Check permissions:{RESET} Make sure you can write to /etc/tor/torrc

{GREEN}Quick Fix Command:{RESET}
{YELLOW}python3 -m tornet.tornet --auto-fix{RESET}
""")

    print(f"\n{GREEN}🎉 Ready to start? Try this command:{RESET}")
    print(f"{YELLOW}python3 -m tornet.tornet --interval 30 --count 3{RESET}")
    print(f"{WHITE}This will change your IP 3 times, every 30 seconds!{RESET}\n")

if __name__ == "__main__":
    main()
