# DNS Leak Detection in TorNet

## What is a DNS Leak?

A DNS leak occurs when your DNS queries bypass the Tor network and go directly to your ISP's DNS servers, potentially revealing your real location and browsing activity even when using Tor.

## How TorNet Detects DNS Leaks

TorNet's DNS leak detection works by:

1. **Testing DNS Resolution Through Tor**: Makes DNS queries through the Tor SOCKS proxy (127.0.0.1:9050)
2. **Testing Direct DNS Resolution**: Makes the same queries without Tor for comparison  
3. **Comparing Results**: Analyzes if the DNS servers and geographic locations match
4. **Risk Assessment**: Identifies potential privacy vulnerabilities

## New Command-Line Options

### DNS Leak Testing
```bash
# Quick DNS leak test
tornet --dns-leak-test

# Comprehensive security check (includes DNS leak test)
tornet --security-check

# Get detailed IP information
tornet --ip-info
```

## How It Works

### 1. DNS Leak Detection (`--dns-leak-test`)
- Tests multiple DNS resolution services through Tor
- Compares with direct connection results
- Identifies if DNS queries are leaking outside Tor
- Provides security recommendations

### 2. IP Information (`--ip-info`)  
- Retrieves detailed IP geolocation data
- Shows country, city, ISP, and organization
- Works with or without Tor
- Uses multiple IP information services for reliability

### 3. Comprehensive Security Check (`--security-check`)
- Combines DNS leak test with IP information
- Checks Tor circuit status
- Provides overall security assessment
- Gives actionable security recommendations

## Security Recommendations

If DNS leaks are detected:

1. **Configure System DNS**: 
   - Use Tor's DNS resolver (127.0.0.1:9053)
   - Or configure your system to route DNS through Tor

2. **Use Tor Browser**:
   - Tor Browser handles DNS properly by default
   - Avoid using regular browsers even with Tor running

3. **Regular Testing**:
   - Run `tornet --dns-leak-test` periodically
   - Test after system updates or configuration changes

4. **Additional Tools**:
   - Use `tornet --security-check` for comprehensive testing
   - Monitor your IP changes with `tornet --ip-info`

## Technical Implementation

The DNS leak detection uses multiple techniques:

- **Multi-Service Testing**: Tests against Cloudflare, IPInfo, and other services
- **Proxy Comparison**: Compares Tor-routed vs direct connections
- **Geographic Analysis**: Checks for location consistency
- **ISP Detection**: Identifies if the same ISP is used for both connections

## Integration with Existing Features

The DNS leak detection integrates seamlessly with TorNet's existing features:

- Works with country-specific exit nodes (`--countries`)
- Compatible with IP change intervals (`--interval`)
- Enhances security during automated IP changes
- Provides feedback during long-running sessions

## Example Output

```
[*] Checking for DNS leaks...
[*] Testing DNS resolution through Tor...
[*] Testing DNS resolution without Tor...
[*] DNS Leak Test Results:
[+] Tor DNS Servers: ['Cloudflare-US', 'ISP-Germany']  
[+] Direct DNS Servers: ['Local-ISP-US']
[+] No obvious DNS leaks detected.

[+] Security Check Summary:
[+] DNS Leak Test: PASSED
[+] Tor Circuit: ACTIVE
```

This enhancement significantly improves TorNet's security capabilities by helping users identify and fix potential privacy vulnerabilities.
