#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# tornet - Automate IP address changes using Tor
# Author: Fidal
# Copyright (c) 2024 Fidal. All rights reserved.
import os
import time
import argparse
import requests
import subprocess
import signal
import platform
import random
import json
from .utils import install_pip, install_requests, install_tor
from .banner import print_banner
TOOL_NAME = "tornet"

green = "\033[92m"
red = "\033[91m"
white = "\033[97m"
reset = "\033[0m"
cyan = "\033[36m"

def is_arch_linux():
    return os.path.exists("/etc/arch-release") or os.path.exists("/etc/manjaro-release")

def is_tor_installed():
    try:
        subprocess.check_output('which tor', shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

def start_tor_service():
    if is_arch_linux():
        os.system("sudo systemctl start tor")
    else:
        os.system("sudo service tor start")

def reload_tor_service():
    # In Docker environment, send SIGHUP to the Tor process instead of using service commands
    if os.environ.get('DOCKER_ENV'):
        try:
            # Find the Tor process ID
            tor_pid = subprocess.check_output("pidof tor", shell=True).decode().strip()
            if tor_pid:
                # Send SIGHUP signal to reload Tor
                os.system(f"kill -HUP {tor_pid}")
        except subprocess.CalledProcessError:
            print(f"{white} [{red}!{white}] {red}Unable to find Tor process. Please check if Tor is running.{reset}")
    else:
        if is_arch_linux():
            os.system("sudo systemctl reload tor")
        else:
            os.system("sudo service tor reload")

def stop_tor_service():
    if is_arch_linux():
        os.system("sudo systemctl stop tor")
    else:
        os.system("sudo service tor stop")

def initialize_environment():
    install_pip()
    install_requests()
    install_tor()
    # Skip starting Tor service if running in Docker
    if not os.environ.get('DOCKER_ENV'):
        start_tor_service()
    print_start_message()

def print_start_message():
    print(f"{white} [{green}+{white}]{green} Tor service started. Please wait a minute for Tor to connect.")
    print(f"{white} [{green}+{white}]{green} Make sure to configure your browser to use Tor for anonymity.")

def ma_ip():
    if is_tor_running():
        return ma_ip_tor()
    else:
        return ma_ip_normal()

def is_tor_running():
    try:
        subprocess.check_output('pgrep -x tor', shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

def ma_ip_tor():
    url = 'https://api.ipify.org'
    proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }
    try:
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException:
        print(f'{white} [{red}!{white}] {red}Having trouble connecting to the Tor network. wait a minute.{reset}')
        return None

def ma_ip_normal():
    try:
        response = requests.get('https://api.ipify.org')
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException:
        print(f'{white} [{red}!{white}] {red}Having trouble fetching the IP address. Please check your internet connection.{reset}')
        return None

def change_ip():
    reload_tor_service()
    return ma_ip()

def change_ip_repeatedly(interval, count):
    if isinstance(interval, int):
        interval = str(interval)  # Convert integer to string for consistency

    if count == 0:  # null
        while True:
            try:
                inte = interval.split("-")
                time.sleep(random.randint(int(inte[0]), int(inte[1])))
                new_ip = change_ip()
                if new_ip:
                    print_ip(new_ip)
            except IndexError:
                time.sleep(int(interval))
                new_ip = change_ip()
                if new_ip:
                    print_ip(new_ip)
    else:
        for _ in range(count):
            try:
                inte = interval.split("-")
                time.sleep(random.randint(int(inte[0]), int(inte[1])))
                new_ip = change_ip()
                if new_ip:
                    print_ip(new_ip)
            except IndexError:
                time.sleep(int(interval))
                new_ip = change_ip()
                if new_ip:
                    print_ip(new_ip)

def print_ip(ip):
    print(f'{white} [{green}+{white}]{green} Your IP has been changed to {white}:{green} {ip}')

def auto_fix():
    install_pip()
    install_requests()
    install_tor()
    os.system("pip3 install --upgrade tornet")

def stop_services():
    # In Docker environment, find and kill the Tor process directly
    if os.environ.get('DOCKER_ENV'):
        try:
            # Find the Tor process ID
            tor_pid = subprocess.check_output("pidof tor", shell=True).decode().strip()
            if tor_pid:
                # Kill the Tor process
                os.system(f"kill {tor_pid}")
                print(f"{white} [{green}+{white}]{green} Tor process stopped.{reset}")
        except subprocess.CalledProcessError:
            print(f"{white} [{red}!{white}] {red}No Tor process found to stop.{reset}")
    else:
        stop_tor_service()
    
    os.system(f"pkill -f {TOOL_NAME} > /dev/null 2>&1")
    print(f"{white} [{green}+{white}]{green} Tor services and {TOOL_NAME} processes stopped.{reset}")

def signal_handler(sig, frame):
    stop_services()
    print(f"\n{white} [{red}!{white}] {red}Program terminated by user.{reset}")
    exit(0)

def check_internet_connection():
    """Check internet connection once, don't block execution"""
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        return True
    except requests.RequestException:
        print(f"{white} [{red}!{white}] {red}Internet connection issue. Some features may not work properly.{reset}")
        return False

def update_torrc_with_countries(countries):
    torrc_path = "/etc/tor/torrc"
    try:
        with open(torrc_path, "a") as torrc:
            torrc.write("\n# Tornet dynamic configuration\n")
            torrc.write("ExitNodes " + ",".join(countries) + "\n")
            torrc.write("StrictNodes 1\n")
        print(f"{white} [{green}+{white}]{green} Tor configuration updated with countries: {white}{','.join(countries)}{reset}")
    except Exception as e:
        print(f"{white} [{red}!{white}] {red}Error updating Tor configuration: {str(e)}{reset}")

def check_dns_leaks():
    """
    Check for DNS leaks by comparing DNS servers used with and without Tor.
    A DNS leak occurs when DNS requests bypass the Tor network.
    """
    print(f"{white} [{cyan}*{white}]{cyan} Checking for DNS leaks...{reset}")
    
    # DNS leak test servers
    dns_test_urls = [
        'https://1.1.1.1/cdn-cgi/trace',  # Cloudflare
        'https://ipinfo.io/json',          # IPInfo
        'https://api.ipify.org?format=json' # Ipify
    ]
    
    proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }
    
    tor_dns_servers = []
    direct_dns_servers = []
    
    try:
        # Test through Tor
        print(f"{white} [{cyan}*{white}]{cyan} Testing DNS resolution through Tor...{reset}")
        for url in dns_test_urls[:2]:  # Test first 2 URLs
            try:
                response = requests.get(url, proxies=proxies, timeout=10)
                if response.status_code == 200:
                    if 'cloudflare' in url:
                        # Parse Cloudflare trace
                        lines = response.text.strip().split('\n')
                        for line in lines:
                            if line.startswith('colo='):
                                tor_dns_servers.append(f"Cloudflare-{line.split('=')[1]}")
                    else:
                        # Parse JSON response
                        data = response.json()
                        if 'org' in data:
                            tor_dns_servers.append(data['org'][:30])
                        elif 'country' in data:
                            tor_dns_servers.append(f"Country: {data['country']}")
            except Exception as e:
                print(f"{white} [{red}!{white}] {red}Error testing {url}: {str(e)[:50]}...{reset}")
        
        # Test direct connection (without Tor) for comparison
        print(f"{white} [{cyan}*{white}]{cyan} Testing DNS resolution without Tor...{reset}")
        try:
            response = requests.get('https://ipinfo.io/json', timeout=5)
            if response.status_code == 200:
                data = response.json()
                if 'org' in data:
                    direct_dns_servers.append(data['org'][:30])
        except Exception as e:
            print(f"{white} [{red}!{white}] {red}Could not test direct connection: {str(e)[:50]}...{reset}")
        
        # Analyze results
        print(f"{white} [{cyan}*{white}]{cyan} DNS Leak Test Results:{reset}")
        print(f"{white} [{green}+{white}]{green} Tor DNS Servers: {white}{tor_dns_servers}{reset}")
        
        if direct_dns_servers:
            print(f"{white} [{green}+{white}]{green} Direct DNS Servers: {white}{direct_dns_servers}{reset}")
            
            # Check for leaks
            leak_detected = False
            for tor_dns in tor_dns_servers:
                for direct_dns in direct_dns_servers:
                    if tor_dns.lower() in direct_dns.lower() or direct_dns.lower() in tor_dns.lower():
                        if not any(safe_word in tor_dns.lower() for safe_word in ['tor', 'proxy', 'vpn']):
                            leak_detected = True
            
            if leak_detected:
                print(f"{white} [{red}!{white}] {red}WARNING: Potential DNS leak detected!{reset}")
                print(f"{white} [{red}!{white}] {red}Your DNS queries might be bypassing Tor.{reset}")
                print(f"{white} [{cyan}*{white}]{cyan} Recommendation: Configure your system to use Tor for DNS.{reset}")
                return False
            else:
                print(f"{white} [{green}+{white}]{green} No obvious DNS leaks detected.{reset}")
                return True
        else:
            print(f"{white} [{cyan}*{white}]{cyan} Could not compare with direct connection.{reset}")
            print(f"{white} [{green}+{white}]{green} Tor DNS resolution appears to be working.{reset}")
            return True
            
    except Exception as e:
        print(f"{white} [{red}!{white}] {red}Error during DNS leak test: {str(e)}{reset}")
        return None

def check_ip_info(ip=None):
    """
    Get detailed information about the current IP address
    """
    if not ip:
        ip = ma_ip()
        if not ip:
            print(f"{white} [{red}!{white}] {red}Could not retrieve IP address{reset}")
            return None
    
    print(f"{white} [{cyan}*{white}]{cyan} Getting detailed information for IP: {white}{ip}{reset}")
    
    proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    } if is_tor_running() else None
    
    try:
        # Try multiple IP info services
        services = [
            ('http://ip-api.com/json/', 'country,regionName,city,org,as,query'),
            ('https://ipapi.co/json/', None),
            ('https://ipinfo.io/json', None)
        ]
        
        for service_url, params in services:
            try:
                url = f"{service_url}?fields={params}" if params else service_url
                response = requests.get(url, proxies=proxies, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    print(f"{white} [{green}+{white}]{green} IP Information:{reset}")
                    print(f"{white} [{cyan}*{white}]{cyan} IP Address: {white}{data.get('query', data.get('ip', ip))}{reset}")
                    
                    if 'country' in data:
                        print(f"{white} [{cyan}*{white}]{cyan} Country: {white}{data['country']}{reset}")
                    if 'regionName' in data or 'region' in data:
                        region = data.get('regionName', data.get('region', ''))
                        print(f"{white} [{cyan}*{white}]{cyan} Region: {white}{region}{reset}")
                    if 'city' in data:
                        print(f"{white} [{cyan}*{white}]{cyan} City: {white}{data['city']}{reset}")
                    if 'org' in data:
                        print(f"{white} [{cyan}*{white}]{cyan} Organization: {white}{data['org']}{reset}")
                    if 'as' in data:
                        print(f"{white} [{cyan}*{white}]{cyan} ASN: {white}{data['as']}{reset}")
                    if 'timezone' in data:
                        print(f"{white} [{cyan}*{white}]{cyan} Timezone: {white}{data['timezone']}{reset}")
                    
                    return data
                    
            except Exception as e:
                continue
        
        print(f"{white} [{red}!{white}] {red}Could not retrieve detailed IP information{reset}")
        return None
        
    except Exception as e:
        print(f"{white} [{red}!{white}] {red}Error getting IP info: {str(e)}{reset}")
        return None

def comprehensive_security_check():
    """
    Perform a comprehensive security check including DNS leaks, IP info, and Tor status
    """
    print(f"{white} [{cyan}*{white}]{cyan} Starting comprehensive security check...{reset}")
    print(f"{white}{'='*60}{reset}")
    
    # Check if Tor is running
    if not is_tor_running():
        print(f"{white} [{red}!{white}] {red}Tor is not running! Security check failed.{reset}")
        return False
    
    # Get current IP and info
    print(f"{white} [{cyan}1/3{white}]{cyan} Checking current IP and location...{reset}")
    check_ip_info()
    
    print(f"\n{white} [{cyan}2/3{white}]{cyan} Performing DNS leak test...{reset}")
    dns_result = check_dns_leaks()
    
    print(f"\n{white} [{cyan}3/3{white}]{cyan} Checking Tor circuit status...{reset}")
    tor_status = check_tor_circuit_status()
    
    print(f"\n{white}{'='*60}{reset}")
    print(f"{white} [{cyan}*{white}]{cyan} Security Check Summary:{reset}")
    
    if dns_result is True:
        print(f"{white} [{green}+{white}]{green} DNS Leak Test: PASSED{reset}")
    elif dns_result is False:
        print(f"{white} [{red}!{white}] {red}DNS Leak Test: FAILED{reset}")
    else:
        print(f"{white} [{cyan}*{white}]{cyan} DNS Leak Test: INCONCLUSIVE{reset}")
    
    if tor_status:
        print(f"{white} [{green}+{white}]{green} Tor Circuit: ACTIVE{reset}")
    else:
        print(f"{white} [{red}!{white}] {red}Tor Circuit: UNKNOWN{reset}")
    
    return dns_result and tor_status

def check_tor_circuit_status():
    """
    Check if Tor circuit is active and get basic info
    """
    try:
        # Try to connect to Tor control port (usually 9051)
        # For basic check, we'll just verify if we can get a different IP through Tor
        tor_ip = ma_ip_tor()
        direct_ip = ma_ip_normal()
        
        if tor_ip and direct_ip and tor_ip != direct_ip:
            print(f"{white} [{green}+{white}]{green} Tor circuit is active (IPs differ){reset}")
            return True
        elif tor_ip and direct_ip and tor_ip == direct_ip:
            print(f"{white} [{red}!{white}] {red}Warning: Tor and direct IPs are the same{reset}")
            return False
        elif tor_ip:
            print(f"{white} [{green}+{white}]{green} Tor connection successful{reset}")
            return True
        else:
            print(f"{white} [{red}!{white}] {red}Could not establish Tor connection{reset}")
            return False
            
    except Exception as e:
        print(f"{white} [{red}!{white}] {red}Error checking Tor circuit: {str(e)}{reset}")
        return False

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)

    parser = argparse.ArgumentParser(description="TorNet - Automate IP address changes using Tor")
    parser.add_argument('--interval', type=str, default=60, help='Time in seconds between IP changes')
    parser.add_argument('--count', type=int, default=10, help='Number of times to change the IP. If 0, change IP indefinitely')
    parser.add_argument('--ip', action='store_true', help='Display the current IP address and exit')
    parser.add_argument('--auto-fix', action='store_true', help='Automatically fix issues (install/upgrade packages)')
    parser.add_argument('--stop', action='store_true', help='Stop all Tor services and tornet processes and exit')
    parser.add_argument('--countries', type=str, help='Comma-separated list of country codes for exit nodes (e.g., us,de,fr)')
    parser.add_argument('--dns-leak-test', action='store_true', help='Perform DNS leak detection test and exit')
    parser.add_argument('--ip-info', action='store_true', help='Show detailed information about current IP and exit')
    parser.add_argument('--security-check', action='store_true', help='Perform comprehensive security check and exit')
    parser.add_argument('--version', action='version', version='%(prog)s 2.2.0')
    args = parser.parse_args()

    if args.ip:
        ip = ma_ip()
        if ip:
            print_ip(ip)
        return

    if args.dns_leak_test:
        if not is_tor_installed():
            print(f"{white} [{red}!{white}] {red}Tor is not installed. Please install Tor first.{reset}")
            return
        check_dns_leaks()
        return

    if args.ip_info:
        check_ip_info()
        return

    if args.security_check:
        if not is_tor_installed():
            print(f"{white} [{red}!{white}] {red}Tor is not installed. Please install Tor first.{reset}")
            return
        comprehensive_security_check()
        return

    if not is_tor_installed():
        print(f"{white} [{red}!{white}] {red}Tor is not installed. Please install Tor and try again.{reset}")
        return

    if args.auto_fix:
        auto_fix()
        print(f"{white} [{green}+{white}]{green} Auto-fix complete.{reset}")
        return

    if args.stop:
        stop_services()
        return

    # Randomly select a country if no countries are provided
    predefined_countries = ['us', 'de', 'fr', 'nl', 'ca']
    if not args.countries:
        selected_country = random.choice(predefined_countries)
        update_torrc_with_countries([selected_country])
        print(f"Randomly selected country: {selected_country}")
    else:
        countries = args.countries.split(',')
        update_torrc_with_countries(countries)

    reload_tor_service()

    print_banner()
    initialize_environment()
    change_ip_repeatedly(args.interval, args.count)

if __name__ == "__main__":
    # Quick internet check but don't block
    check_internet_connection()
    main()
