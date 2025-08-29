#!/usr/bin/env python3
"""
TorNet Demo - Simulates dynamic IP changing without requiring Tor
This shows exactly how TorNet would work in a real environment
"""

import requests
import time
import random

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
WHITE = "\033[97m"
CYAN = "\033[96m"
RESET = "\033[0m"

def print_status(message, status="info"):
    if status == "success":
        print(f"{WHITE}[{GREEN}+{WHITE}]{GREEN} {message}{RESET}")
    elif status == "error":
        print(f"{WHITE}[{RED}!{WHITE}]{RED} {message}{RESET}")
    elif status == "warning":
        print(f"{WHITE}[{YELLOW}*{WHITE}]{YELLOW} {message}{RESET}")
    else:
        print(f"{WHITE}[{CYAN}*{WHITE}]{CYAN} {message}{RESET}")

def get_current_ip():
    """Get current real IP address"""
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        return response.text.strip()
    except:
        return "Unable to fetch"

def get_random_tor_ip():
    """Simulate getting a random Tor exit node IP"""
    # These are example IPs from different countries that Tor might use
    tor_ips = [
        ("185.220.101.32", "Germany", "AS16276 OVH SAS"),
        ("199.87.154.255", "United States", "AS396356 Riseup Networks"), 
        ("109.70.100.34", "Netherlands", "AS60781 LeaseWeb Netherlands"),
        ("77.247.181.165", "Romania", "AS9050 RTD Romania"),
        ("162.247.74.27", "United States", "AS396356 Riseup Networks"),
        ("192.42.116.16", "Netherlands", "AS60781 LeaseWeb Netherlands"),
        ("51.75.144.43", "France", "AS16276 OVH SAS"),
        ("185.241.208.234", "Germany", "AS202425 IP Volume inc"),
        ("199.249.230.164", "United States", "AS396356 Riseup Networks"),
        ("45.141.215.103", "Romania", "AS200651 Flokinet Ltd")
    ]
    return random.choice(tor_ips)

def simulate_tornet_session(interval=30, count=3, countries=None):
    """Simulate a TorNet IP changing session"""
    
    print(f"""{CYAN}
╔══════════════════════════════════════════════════════════════╗
║                 TorNet Dynamic IP Demo                       ║
║              Simulating Real Tor Behavior                    ║
╚══════════════════════════════════════════════════════════════╝{RESET}""")
    
    print_status("Starting TorNet simulation...", "info")
    print_status(f"Settings: Change IP {count} times every {interval} seconds", "info")
    
    # Show current real IP
    current_ip = get_current_ip()
    print(f"\n{YELLOW}Your Current Real IP:{RESET}")
    print_status(f"Real IP: {current_ip}", "warning")
    
    print(f"\n{GREEN}🔄 Starting Dynamic IP Changes (simulated Tor):${RESET}")
    print(f"{WHITE}{'='*60}{RESET}")
    
    # Simulate Tor startup
    print_status("Tor service started. Please wait a minute for Tor to connect.", "success")
    print_status("Make sure to configure your browser to use Tor for anonymity.", "success")
    
    # Simulate IP changes
    for i in range(count):
        print(f"\n{CYAN}Change #{i+1}:{RESET}")
        print_status(f"Waiting {interval} seconds before next IP change...", "info")
        
        # Simulate waiting (shortened for demo)
        for j in range(3):  # Show countdown
            print(f"  {WHITE}⏳ {3-j} seconds remaining...{RESET}")
            time.sleep(1)
        
        # Get simulated new IP
        new_ip, country, isp = get_random_tor_ip()
        print_status(f"Your IP has been changed to: {new_ip}", "success")
        print(f"    {CYAN}📍 Location: {country}{RESET}")
        print(f"    {CYAN}🏢 ISP: {isp}{RESET}")
        
        if i < count - 1:  # Don't wait after last change
            print()

    print(f"\n{GREEN}✅ Session Complete!{RESET}")
    print_status(f"Successfully changed IP {count} times", "success")

def show_tornet_commands():
    """Show real TorNet commands that would work with Tor installed"""
    
    print(f"\n{YELLOW}🚀 Real TorNet Commands (when Tor is installed):{RESET}")
    print(f"{WHITE}{'='*60}{RESET}")
    
    commands = [
        ("python3 -m tornet.tornet --ip", "Check current IP"),
        ("python3 -m tornet.tornet --interval 30 --count 3", "Change IP 3 times, 30s apart"),
        ("python3 -m tornet.tornet --interval 60 --count 0", "Change IP every minute forever"),
        ("python3 -m tornet.tornet --countries us,de", "Use US/German exit nodes only"),
        ("python3 -m tornet.tornet --dns-leak-test", "Test for DNS leaks"),
        ("python3 -m tornet.tornet --security-check", "Full security analysis"),
        ("python3 -m tornet.tornet --auto-fix", "Install/fix Tor automatically"),
    ]
    
    for cmd, desc in commands:
        print(f"{GREEN}• {desc}:{RESET}")
        print(f"  {YELLOW}{cmd}{RESET}\n")

def main():
    print_status("TorNet Demo - Showing Dynamic IP Changing", "info")
    print_status("(This simulates real Tor behavior)", "warning")
    
    # Get user choice
    print(f"\n{CYAN}Choose demo type:{RESET}")
    print(f"{WHITE}1. Quick demo (3 changes, 3 seconds apart){RESET}")
    print(f"{WHITE}2. Medium demo (5 changes, 5 seconds apart){RESET}")
    print(f"{WHITE}3. Show real commands only{RESET}")
    
    try:
        choice = input(f"\n{YELLOW}Enter choice (1-3): {RESET}")
        
        if choice == "1":
            simulate_tornet_session(interval=3, count=3)
        elif choice == "2":
            simulate_tornet_session(interval=5, count=5)
        elif choice == "3":
            show_tornet_commands()
            return
        else:
            print_status("Invalid choice, running quick demo...", "warning")
            simulate_tornet_session(interval=3, count=3)
            
    except KeyboardInterrupt:
        print(f"\n{RED}Demo interrupted by user{RESET}")
        return
    
    # Show real commands
    show_tornet_commands()
    
    print(f"\n{CYAN}💡 To use TorNet for real:{RESET}")
    print(f"{WHITE}1. Install Tor: sudo apt install tor{RESET}")
    print(f"{WHITE}2. Start Tor service: sudo systemctl start tor{RESET}")  
    print(f"{WHITE}3. Run: python3 -m tornet.tornet --interval 30 --count 3{RESET}")
    print(f"{WHITE}4. Your IP will change dynamically through Tor network!{RESET}")

if __name__ == "__main__":
    main()
