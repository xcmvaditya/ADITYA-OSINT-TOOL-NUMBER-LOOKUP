#!/usr/bin/env python3
"""
Aditya OSINT Framework - Cybersecurity Intelligence Tool
Author: Security Research Purpose Only
Disclaimer: Only use on systems/networks you own or have written authorization
"""

import os
import sys
import json
import time
import requests
import subprocess
from datetime import datetime
from colorama import init, Fore, Style
import pyfiglet

# Initialize colorama for cross-platform colors
init(autoreset=True)

class AdityaOSINT:
    def __init__(self):
        self.results = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Aditya-OSINT-Framework/1.0'
        })
        # API key for mobile lookup (provided by user)
        self.tabbo_api_key = "tabboJ8K"  # Tabbo API key

    def banner(self):
        """Display stylish banner"""
        os.system('clear' if os.name == 'posix' else 'cls')
        banner_text = pyfiglet.figlet_format("ADITYA OSINT", font="slant")
        print(Fore.CYAN + banner_text)
        print(Fore.YELLOW + "=" * 60)
        print(Fore.GREEN + "    Cybersecurity Intelligence Framework")
        print(Fore.RED + "    [!] Legal Use Only - Authorized Testing")
        print(Fore.YELLOW + "=" * 60 + "\n")

    def show_menu(self):
        """Display main menu"""
        print(Fore.CYAN + "\n[ MAIN MENU ]")
        print(Fore.WHITE + "1. " + Fore.GREEN + "IP Intelligence")
        print(Fore.WHITE + "2. " + Fore.GREEN + "Domain Reconnaissance")
        print(Fore.WHITE + "3. " + Fore.GREEN + "SSL/TLS Analysis")
        print(Fore.WHITE + "4. " + Fore.GREEN + "Subdomain Discovery")
        print(Fore.WHITE + "5. " + Fore.GREEN + "DNS Enumeration")
        print(Fore.WHITE + "6. " + Fore.GREEN + "HTTP Header Analysis")
        print(Fore.WHITE + "7. " + Fore.GREEN + "WHOIS Lookup")
        print(Fore.WHITE + "8. " + Fore.GREEN + "Email Reputation Check")
        print(Fore.WHITE + "9. " + Fore.GREEN + "Save Results")
        print(Fore.WHITE + "10. " + Fore.GREEN + "Exit")
        print(Fore.WHITE + "11. " + Fore.GREEN + "Mobile Number Intelligence (Tabbo API)")
        print(Fore.YELLOW + "-" * 40)

    def ip_intelligence(self, ip):
        """Get public IP information"""
        try:
            print(Fore.BLUE + f"\n[*] Gathering IP intelligence for {ip}...")
            
            # Multiple public API sources
            sources = {
                'ipapi': f'http://ip-api.com/json/{ip}',
                'ipinfo': f'https://ipinfo.io/{ip}/json',
                'abuseipdb': f'https://api.abuseipdb.com/api/v2/check'
            }
            
            results = {}
            for source, url in sources.items():
                try:
                    if source == 'abuseipdb':
                        # AbuseIPDB requires API key (free registration)
                        # headers = {'Key': 'YOUR_API_KEY'}
                        # response = self.session.get(url, headers=headers)
                        pass
                    else:
                        response = self.session.get(url, timeout=10)
                        if response.status_code == 200:
                            results[source] = response.json()
                except:
                    results[source] = {"error": "Failed to fetch"}
                    
            return results
            
        except Exception as e:
            return {"error": str(e)}

    def domain_recon(self, domain):
        """Gather domain intelligence"""
        try:
            print(Fore.BLUE + f"\n[*] Running domain recon for {domain}...")
            
            # Check if domain resolves
            import socket
            ip = socket.gethostbyname(domain)
            
            results = {
                'ip': ip,
                'ssl': self.check_ssl(domain),
                'headers': self.check_headers(domain),
                'dns': self.dns_enumeration(domain)
            }
            
            return results
            
        except Exception as e:
            return {"error": str(e)}

    def check_ssl(self, domain):
        """Check SSL/TLS certificate"""
        try:
            import ssl
            import socket
            
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    return {
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'subject': dict(x[0] for x in cert['subject']),
                        'expiry': cert['notAfter']
                    }
        except:
            return {"error": "SSL check failed"}

    def check_headers(self, domain):
        """Analyze HTTP security headers"""
        try:
            response = self.session.get(f'https://{domain}', timeout=10, verify=False)
            headers = response.headers
            
            security_headers = {
                'Strict-Transport-Security': headers.get('Strict-Transport-Security', 'Missing'),
                'Content-Security-Policy': headers.get('Content-Security-Policy', 'Missing'),
                'X-Frame-Options': headers.get('X-Frame-Options', 'Missing'),
                'X-Content-Type-Options': headers.get('X-Content-Type-Options', 'Missing'),
                'Referrer-Policy': headers.get('Referrer-Policy', 'Missing')
            }
            
            return security_headers
            
        except:
            return {"error": "Header analysis failed"}

    def dns_enumeration(self, domain):
        """Perform DNS enumeration"""
        try:
            import dns.resolver
            
            record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']
            records = {}
            
            for record in record_types:
                try:
                    answers = dns.resolver.resolve(domain, record)
                    records[record] = [str(r) for r in answers]
                except:
                    records[record] = []
                    
            return records
            
        except Exception as e:
            return {"error": str(e)}

    def subdomain_discovery(self, domain):
        """Discover subdomains (using common wordlist)"""
        try:
            print(Fore.BLUE + f"\n[*] Discovering subdomains for {domain}...")
            
            common_subs = ['www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk', 'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'm', 'imap', 'test', 'ns', 'blog', 'pop3', 'dev', 'www2', 'admin', 'forum', 'news', 'vpn', 'ns3', 'mail2', 'new', 'mysql', 'old', 'lists', 'support', 'mobile', 'mx', 'static', 'docs', 'beta', 'shop', 'sql', 'secure', 'demo', 'cp', 'calendar', 'wiki', 'web', 'media', 'email', 'images', 'img', 'download', 'api']
            
            found_subs = []
            for sub in common_subs:
                try:
                    subdomain = f"{sub}.{domain}"
                    ip = socket.gethostbyname(subdomain)
                    found_subs.append({'subdomain': subdomain, 'ip': ip})
                except:
                    pass
                    
            return found_subs
            
        except:
            return {"error": "Subdomain discovery failed"}

    def whois_lookup(self, domain):
        """Perform WHOIS lookup"""
        try:
            import whois
            
            w = whois.whois(domain)
            return {
                'registrar': w.registrar,
                'creation_date': str(w.creation_date),
                'expiration_date': str(w.expiration_date),
                'name_servers': w.name_servers
            }
            
        except:
            return {"error": "WHOIS lookup failed"}

    def email_reputation(self, email):
        """Check email reputation (using public APIs)"""
        try:
            # Using Hunter.io API demo (you need API key for production)
            # This is just a placeholder for educational purposes
            print(Fore.YELLOW + "\n[!] Email reputation checks require API keys")
            return {"info": "Use services like Hunter.io, HaveIBeenPwned for email analysis"}
            
        except:
            return {"error": "Check failed"}

    def mobile_lookup(self, mobile):
        """Lookup mobile number using Tabbo API"""
        try:
            print(Fore.BLUE + f"\n[*] Querying Tabbo API for mobile: {mobile}...")
            url = f"https://tabbo-api.vercel.app/api/lookup?key={self.tabbo_api_key}&mobile={mobile}"
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"API returned HTTP {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": str(e)}

    def save_results(self, filename):
        """Save all results to file"""
        if self.results:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename}_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2, default=str)
            
            print(Fore.GREEN + f"\n[✓] Results saved to {filename}")
        else:
            print(Fore.RED + "\n[!] No results to save")

    def run(self):
        """Main execution loop"""
        self.banner()
        
        while True:
            self.show_menu()
            choice = input(Fore.CYAN + "\n[+] Select option: " + Fore.WHITE)
            
            if choice == '1':
                ip = input(Fore.YELLOW + "[?] Enter IP address: " + Fore.WHITE)
                self.results['ip_intel'] = self.ip_intelligence(ip)
                print(Fore.GREEN + "\n[+] Results:")
                print(json.dumps(self.results['ip_intel'], indent=2))
                
            elif choice == '2':
                domain = input(Fore.YELLOW + "[?] Enter domain: " + Fore.WHITE)
                self.results['domain_recon'] = self.domain_recon(domain)
                print(Fore.GREEN + "\n[+] Results:")
                print(json.dumps(self.results['domain_recon'], indent=2))
                
            elif choice == '3':
                domain = input(Fore.YELLOW + "[?] Enter domain: " + Fore.WHITE)
                self.results['ssl_analysis'] = self.check_ssl(domain)
                print(Fore.GREEN + "\n[+] Results:")
                print(json.dumps(self.results['ssl_analysis'], indent=2))
                
            elif choice == '4':
                domain = input(Fore.YELLOW + "[?] Enter domain: " + Fore.WHITE)
                self.results['subdomains'] = self.subdomain_discovery(domain)
                print(Fore.GREEN + "\n[+] Found subdomains:")
                for sub in self.results['subdomains']:
                    print(f"  - {sub['subdomain']} -> {sub['ip']}")
                    
            elif choice == '5':
                domain = input(Fore.YELLOW + "[?] Enter domain: " + Fore.WHITE)
                self.results['dns_records'] = self.dns_enumeration(domain)
                print(Fore.GREEN + "\n[+] DNS Records:")
                print(json.dumps(self.results['dns_records'], indent=2))
                
            elif choice == '6':
                domain = input(Fore.YELLOW + "[?] Enter domain: " + Fore.WHITE)
                self.results['http_headers'] = self.check_headers(domain)
                print(Fore.GREEN + "\n[+] Security Headers:")
                print(json.dumps(self.results['http_headers'], indent=2))
                
            elif choice == '7':
                domain = input(Fore.YELLOW + "[?] Enter domain: " + Fore.WHITE)
                self.results['whois'] = self.whois_lookup(domain)
                print(Fore.GREEN + "\n[+] WHOIS Results:")
                print(json.dumps(self.results['whois'], indent=2))
                
            elif choice == '8':
                email = input(Fore.YELLOW + "[?] Enter email: " + Fore.WHITE)
                self.results['email_check'] = self.email_reputation(email)
                print(Fore.GREEN + "\n[+] Results:")
                print(json.dumps(self.results['email_check'], indent=2))
                
            elif choice == '9':
                filename = input(Fore.YELLOW + "[?] Enter filename prefix: " + Fore.WHITE)
                self.save_results(filename)
                
            elif choice == '10':
                print(Fore.RED + "\n[!] Exiting Aditya OSINT Framework...")
                sys.exit(0)
                
            elif choice == '11':
                mobile = input(Fore.YELLOW + "[?] Enter mobile number: " + Fore.WHITE)
                self.results['mobile_lookup'] = self.mobile_lookup(mobile)
                print(Fore.GREEN + "\n[+] Results:")
                print(json.dumps(self.results['mobile_lookup'], indent=2))
                
            else:
                print(Fore.RED + "\n[!] Invalid option!")
            
            input(Fore.YELLOW + "\n[Press Enter to continue...]")

if __name__ == "__main__":
    # Check dependencies
    try:
        import colorama, pyfiglet, dns.resolver, whois
    except ImportError:
        print("[!] Missing dependencies. Install with:")
        print("pip install colorama pyfiglet dnspython python-whois requests")
        sys.exit(1)
    
    # Display legal warning
    print(Fore.RED + "\n" + "="*60)
    print(Fore.RED + "LEGAL WARNING: This tool is for authorized security testing only!")
    print(Fore.RED + "Using this tool against systems you don't own is illegal.")
    print(Fore.RED + "You are responsible for complying with all applicable laws.")
    print(Fore.RED + "="*60 + "\n")
    
    confirm = input("Do you agree to use this tool legally? (yes/no): ").lower()
    if confirm == 'yes':
        tool = AdityaOSINT()
        tool.run()
    else:
        print("Exiting...")
        sys.exit(0)
