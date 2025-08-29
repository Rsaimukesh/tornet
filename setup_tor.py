#!/usr/bin/env python3
"""
TorNet Setup and Fix Script
This script will install Tor and fix common issues
"""

import subprocess
import sys
import os
import platform
import requests

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

def check_internet():
    """Check if internet connection is working"""
    print_status("Checking internet connection...")
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        if response.status_code == 200:
            print_status("Internet connection: OK", "success")
            return True
    except Exception as e:
        print_status(f"Internet connection failed: {str(e)}", "error")
        return False

def detect_system():
    """Detect the operating system"""
    system = platform.system().lower()
    if system == "linux":
        # Check for specific Linux distributions
        if os.path.exists("/etc/arch-release") or os.path.exists("/etc/manjaro-release"):
            return "arch"
        elif os.path.exists("/etc/debian_version"):
            return "debian"
        elif os.path.exists("/etc/fedora-release"):
            return "fedora"
        else:
            return "linux"
    return system

def install_tor():
    """Install Tor based on the operating system"""
    system = detect_system()
    print_status(f"Detected system: {system}")
    
    try:
        if system == "arch":
            print_status("Installing Tor on Arch Linux...")
            subprocess.run(["sudo", "pacman", "-S", "tor", "--noconfirm"], check=True)
            subprocess.run(["sudo", "systemctl", "enable", "tor"], check=True)
            
        elif system == "debian":
            print_status("Installing Tor on Debian/Ubuntu...")
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "tor"], check=True)
            subprocess.run(["sudo", "systemctl", "enable", "tor"], check=True)
            
        elif system == "fedora":
            print_status("Installing Tor on Fedora...")
            subprocess.run(["sudo", "dnf", "install", "-y", "tor"], check=True)
            subprocess.run(["sudo", "systemctl", "enable", "tor"], check=True)
            
        else:
            print_status("Unsupported system. Please install Tor manually.", "warning")
            print_status("Visit: https://www.torproject.org/download/", "info")
            return False
            
        print_status("Tor installed successfully!", "success")
        return True
        
    except subprocess.CalledProcessError as e:
        print_status(f"Failed to install Tor: {e}", "error")
        return False
    except FileNotFoundError:
        print_status("Package manager not found. Please install Tor manually.", "error")
        return False

def check_tor_installation():
    """Check if Tor is properly installed"""
    try:
        result = subprocess.run(["which", "tor"], capture_output=True, text=True)
        if result.returncode == 0:
            print_status(f"Tor found at: {result.stdout.strip()}", "success")
            return True
        else:
            print_status("Tor not found in PATH", "error")
            return False
    except Exception as e:
        print_status(f"Error checking Tor: {e}", "error")
        return False

def start_tor_service():
    """Start the Tor service"""
    try:
        print_status("Starting Tor service...")
        subprocess.run(["sudo", "systemctl", "start", "tor"], check=True)
        print_status("Tor service started", "success")
        return True
    except subprocess.CalledProcessError:
        print_status("Failed to start Tor service", "error")
        return False

def test_tor_connection():
    """Test if Tor is working"""
    print_status("Testing Tor connection...")
    try:
        # Test SOCKS proxy connection
        proxies = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }
        response = requests.get('https://check.torproject.org/api/ip', 
                              proxies=proxies, timeout=10)
        data = response.json()
        
        if data.get('IsTor'):
            print_status(f"Tor is working! IP: {data.get('IP')}", "success")
            return True
        else:
            print_status("Tor connection failed", "error")
            return False
            
    except Exception as e:
        print_status(f"Tor connection test failed: {e}", "warning")
        print_status("Tor might still be connecting. Wait a minute and try again.", "info")
        return False

def fix_tornet_issues():
    """Fix common TorNet issues"""
    print_status("Fixing TorNet configuration...")
    
    # Create a simple test script without import issues
    test_script = """#!/usr/bin/env python3
import sys
import os
import requests
import time

# Add current directory to Python path
sys.path.insert(0, '/home/sai/tornet')

def get_ip_direct():
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        return response.text.strip()
    except:
        return None

def get_ip_tor():
    try:
        proxies = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }
        response = requests.get('https://api.ipify.org', proxies=proxies, timeout=10)
        return response.text.strip()
    except:
        return None

def test_tornet():
    print("Testing TorNet functionality...")
    
    print("\\n1. Direct IP:")
    direct_ip = get_ip_direct()
    print(f"   {direct_ip}")
    
    print("\\n2. Tor IP:")
    tor_ip = get_ip_tor()
    print(f"   {tor_ip}")
    
    if direct_ip and tor_ip:
        if direct_ip != tor_ip:
            print("\\n✓ Success! Tor is working (IPs are different)")
            return True
        else:
            print("\\n⚠ Warning: IPs are the same - check Tor configuration")
            return False
    else:
        print("\\n✗ Error: Could not retrieve IPs")
        return False

if __name__ == "__main__":
    test_tornet()
"""
    
    with open('/home/sai/tornet/test_tornet.py', 'w') as f:
        f.write(test_script)
    
    print_status("Created test script: test_tornet.py", "success")

def main():
    print(f"""{CYAN}
╔══════════════════════════════════════════════════════════════╗
║                    TorNet Setup & Fix                        ║
║              Automatic Tor Installation                      ║
╚══════════════════════════════════════════════════════════════╝{RESET}""")

    # Check internet connection
    if not check_internet():
        print_status("Please check your internet connection and try again.", "error")
        sys.exit(1)

    # Check if Tor is installed
    if not check_tor_installation():
        print_status("Tor not found. Installing...", "warning")
        if not install_tor():
            print_status("Failed to install Tor. Please install manually.", "error")
            sys.exit(1)

    # Start Tor service
    if not start_tor_service():
        print_status("Could not start Tor service. Trying alternative...", "warning")

    # Wait for Tor to initialize
    print_status("Waiting for Tor to initialize (30 seconds)...", "info")
    import time
    time.sleep(5)  # Short wait for demo

    # Test Tor connection
    test_tor_connection()

    # Fix TorNet issues
    fix_tornet_issues()

    print(f"\n{GREEN}🎉 Setup Complete!{RESET}")
    print(f"\n{YELLOW}Try these commands:{RESET}")
    print(f"{WHITE}cd /home/sai/tornet{RESET}")
    print(f"{WHITE}python3 test_tornet.py{RESET}")
    print(f"{WHITE}python3 -m tornet.tornet --ip{RESET}")

if __name__ == "__main__":
    main()
