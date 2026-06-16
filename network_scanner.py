import socket
import threading
import time
import sys
from datetime import datetime

CYAN = "\033[96m"
MAGENTA = "\033[95m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_banner():

    banner = f"""
    {CYAN}{BOLD}
    SCIENTIFIC PROJECT
    NETWORK SENTINEL v1.0
    -----------------------------------------{RESET}
    """

    print(banner)

class NetworkScanner:
    def __init__(self, target_host):
        self.target_host = target_host
        self.open_ports = []

    def scan_port(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((self.target_host, port))
            
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "UNKNOWN"
                
                self.open_ports.append((port, service))
                print(f" {GREEN}[+]{RESET} Port {BOLD}{port}{RESET} ({service}) is {GREEN}OPEN{RESET}")
            
            sock.close()
            
        except Exception:
            pass

    def run(self, start_port, end_port):
        print(f"{CYAN}[*]{RESET} Initializing scan for: {BOLD}{self.target_host}{RESET}")
        print(f"{CYAN}[*]{RESET} Range: {start_port} - {end_port}\n")
        
        threads = []
        for port in range(start_port, end_port + 1):
            t = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(t)
            t.start()
            
            if port % 100 == 0:
                time.sleep(0.1)

        for t in threads:
            t.join()
            
        self.report()

    def report(self):
        print(f"\n{MAGENTA}{'='*40}{RESET}")
        print(f"{BOLD}SENTINEL REPORT - {datetime.now().strftime('%H:%M:%S')}{RESET}")
        print(f"{MAGENTA}{'='*40}{RESET}")
        
        if self.open_ports:
            for port, service in sorted(self.open_ports):
                print(f" > PORT {port:<5} | SERVICE: {service}")
        else:
            print(f"{RED}No active services found in the specified range.{RESET}")
        
        print(f"{MAGENTA}{'='*40}{RESET}")
        print(f"{CYAN}SYSTEM READY. WAITING FOR NEXT COMMAND.{RESET}")

if __name__ == "__main__":
    print_banner()
    
    user_input = input(f"{BOLD}Enter target host (default 127.0.0.1): {RESET}")
    
    if user_input:
        target = user_input
    else:
        target = "127.0.0.1"
    
    scanner = NetworkScanner(target)
    
    try:
        scanner.run(1, 1024)
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Scan interrupted by user.{RESET}")
        sys.exit()
