#!/usr/bin/env python3
"""
Test script for DNS leak detection functionality
This script can be run to test the DNS leak detection features
"""

import sys
import os

# Add the parent directory to the path to import tornet modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tornet.tornet import check_dns_leaks, check_ip_info, comprehensive_security_check, is_tor_running

def test_dns_leak_detection():
    """Test the DNS leak detection functionality"""
    print("Testing DNS Leak Detection...")
    print("=" * 50)
    
    # Check if Tor is running
    if not is_tor_running():
        print("Warning: Tor is not running. Some tests may not work properly.")
        print("Please start Tor service and try again.")
        return False
    
    # Test DNS leak detection
    print("\n1. Testing DNS leak detection:")
    result = check_dns_leaks()
    
    # Test IP info
    print("\n2. Testing IP information retrieval:")
    check_ip_info()
    
    # Test comprehensive security check
    print("\n3. Testing comprehensive security check:")
    comprehensive_security_check()
    
    return True

if __name__ == "__main__":
    test_dns_leak_detection()
