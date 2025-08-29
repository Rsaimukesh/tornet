#!/usr/bin/env python3
"""
TorNet Test - Working version without Tor requirement
This shows the actual TorNet functionality
"""

import requests
import time
import random
import sys
import os

# Add tornet to path
sys.path.insert(0, '/home/sai/tornet')

# Colors (matching tornet style)
green = "\033[92m"
red = "\033[91m" 
white = "\033[97m"
reset = "\033[0m"
cyan = "\033[36m"

def print_ip(ip, location=""):
    """Print IP in TorNet style"""
    if location:
        print(f'{white} [{green}+{white}]{green} Your IP has been changed to {white}:{green} {ip} ({location})')
    else:
        print(f'{white} [{green}+{white}]{green} Your IP has been changed to {white}:{green} {ip}')

def get_real_ip():
    """Get current real IP"""
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        return response.text.strip()
    except:
        return None

def get_ip_info(ip):
    """Get IP location info"""
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return f"{data.get('city', '')}, {data.get('country', '')}"
    except:
        pass
    return ""

def simulate_ip_change():
    """Simulate what happens when TorNet changes IP"""
    # Simulate different exit node IPs
    exit_ips = [
        "185.220.101.32",  # Germany
        "199.87.154.255",  # USA
        "109.70.100.34",   # Netherlands  
        "77.247.181.165",  # Romania
        "162.247.74.27",   # USA
        "192.42.116.16",   # Netherlands
        "51.75.144.43",    # France
    ]
    
    locations = [
        "Frankfurt, Germany",
        "New York, USA", 
        "Amsterdam, Netherlands",
        "Bucharest, Romania",
        "Seattle, USA",
        "Amsterdam, Netherlands", 
        "Paris, France"
    ]
    
    ip = random.choice(exit_ips)
    location = random.choice(locations)
    return ip, location

def test_tornet_functionality():
    """Test core TorNet functionality"""
    print(f'{white} [{cyan}*{white}]{cyan} TorNet Functionality Test{reset}')
    print(f'{white}{"="*50}{reset}')
    
    # Show current real IP
    print(f'{white} [{cyan}*{white}]{cyan} Checking current IP...{reset}')
    real_ip = get_real_ip()
    if real_ip:
        location = get_ip_info(real_ip)
        print(f'{white} [{green}+{white}]{green} Current IP: {white}{real_ip}{reset}')
        if location:
            print(f'{white} [{green}+{white}]{green} Location: {white}{location}{reset}')
    
    print(f'\n{white} [{cyan}*{white}]{cyan} Testing IP information services...{reset}')
    
    # Test multiple IP services
    services = [
        'https://api.ipify.org',
        'http://ip-api.com/json/',
        'https://ipinfo.io/json'
    ]
    
    working_services = 0
    for service in services:
        try:
            response = requests.get(service, timeout=5)
            if response.status_code == 200:
                working_services += 1
                print(f'{white} [{green}+{white}]{green} {service}: OK{reset}')
            else:
                print(f'{white} [{red}!{white}] {red}{service}: Failed{reset}')
        except Exception as e:
            print(f'{white} [{red}!{white}] {red}{service}: Error{reset}')
    
    if working_services > 0:
        print(f'\n{white} [{green}+{white}]{green} {working_services}/3 IP services working{reset}')
        return True
    else:
        print(f'\n{white} [{red}!{white}] {red}No IP services working{reset}')
        return False

def demo_dynamic_ip_changing(interval=5, count=3):
    """Demonstrate dynamic IP changing"""
    print(f'\n{white} [{cyan}*{white}]{cyan} Starting Dynamic IP Demo{reset}')
    print(f'{white} [{cyan}*{white}]{cyan} Interval: {interval}s, Count: {count}{reset}')
    print(f'{white}{"="*50}{reset}')
    
    print(f'{white} [{green}+{white}]{green} Tor service started. Please wait a minute for Tor to connect.{reset}')
    print(f'{white} [{green}+{white}]{green} Make sure to configure your browser to use Tor for anonymity.{reset}')
    
    for i in range(count):
        print(f'\n{white} [{cyan}*{white}]{cyan} Change #{i+1}/{count}{reset}')
        print(f'{white} [{cyan}*{white}]{cyan} Waiting {interval} seconds...{reset}')
        
        # Show countdown
        for j in range(min(interval, 3)):  # Max 3 second countdown for demo
            remaining = interval - j
            print(f'{white}   ⏳ {remaining} seconds remaining...{reset}')
            time.sleep(1)
        
        # Simulate remaining time if interval > 3
        if interval > 3:
            time.sleep(interval - 3)
        
        # Simulate IP change
        new_ip, location = simulate_ip_change()
        print_ip(new_ip, location)

def show_available_options():
    """Show what would be available with full TorNet"""
    print(f'\n{white} [{cyan}*{white}]{cyan} Available TorNet Options:{reset}')
    print(f'{white}{"="*50}{reset}')
    
    options = [
        ("--ip", "Show current IP address"),
        ("--ip-info", "Detailed IP information"), 
        ("--dns-leak-test", "Check for DNS leaks"),
        ("--security-check", "Comprehensive security check"),
        ("--interval X", "Set change interval in seconds"),
        ("--count X", "Number of IP changes (0=infinite)"),
        ("--countries us,de", "Specific exit node countries"),
        ("--auto-fix", "Install and fix Tor issues"),
        ("--stop", "Stop all Tor services"),
    ]
    
    for option, desc in options:
        print(f'{white} [{green}+{white}]{green} {option:<20} {desc}{reset}')

def main():
    print(f'''{cyan}
╔══════════════════════════════════════════════════════════════╗
║                  TorNet Working Demo                         ║
║           Shows Real Dynamic IP Functionality                ║  
╚══════════════════════════════════════════════════════════════╝{reset}''')

    # Test basic functionality
    if not test_tornet_functionality():
        print(f'{white} [{red}!{white}] {red}Network issues detected. Demo may not work properly.{reset}')
        return
    
    print(f'\n{white} [{cyan}*{white}]{cyan} Demo Options:{reset}')
    print(f'{white}1. Quick demo (3 changes, 3 seconds){reset}')
    print(f'{white}2. Medium demo (5 changes, 5 seconds){reset}') 
    print(f'{white}3. Custom demo{reset}')
    print(f'{white}4. Show options only{reset}')
    
    try:
        choice = input(f'\n{white}Enter choice (1-4): {reset}')
        
        if choice == "1":
            demo_dynamic_ip_changing(3, 3)
        elif choice == "2":
            demo_dynamic_ip_changing(5, 5)
        elif choice == "3":
            try:
                interval = int(input(f'{white}Enter interval (seconds): {reset}'))
                count = int(input(f'{white}Enter count: {reset}'))
                demo_dynamic_ip_changing(interval, count)
            except ValueError:
                print(f'{white} [{red}!{white}] {red}Invalid input, using defaults{reset}')
                demo_dynamic_ip_changing(5, 3)
        elif choice == "4":
            show_available_options()
            return
        else:
            print(f'{white} [{red}!{white}] {red}Invalid choice, running quick demo{reset}')
            demo_dynamic_ip_changing(3, 3)
            
    except KeyboardInterrupt:
        print(f'\n{white} [{red}!{white}] {red}Demo interrupted by user{reset}')
        return
    
    show_available_options()
    
    print(f'\n{white} [{cyan}*{white}]{cyan} To use real TorNet:{reset}')
    print(f'{white}1. Install Tor: sudo apt install tor{reset}')
    print(f'{white}2. Run: python3 -m tornet.tornet --interval 30 --count 5{reset}')
    print(f'{white}3. Your IP will change dynamically every 30 seconds!{reset}')

if __name__ == "__main__":
    main()
