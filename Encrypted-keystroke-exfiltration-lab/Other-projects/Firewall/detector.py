import time
from collections import defaultdict

from config import (
    SCAN_THRESHOLD,
    SCAN_TIME_WINDOW,
    SYN_THRESHOLD,
    SYN_TIME_WINDOW,
    PACKET_RATE_THRESHOLD,
    PACKET_RATE_WINDOW
    )

from blocker import block_ip
from logger import log_alert

port_scan_tracker = defaultdict(list)
syn_tracker = defaultdict(list)
packet_tracker = defaultdict(list)

def detect_port_scan(ip, port):

    now = time.time()

    port_scan_tracker[ip].append((port, now))

    port_scan_tracker[ip] = [
        (p,t) for p,t in port_scan_tracker[ip]
        if now - t < SCAN_TIME_WINDOW
    ]

    ports = set(p for p,_ in port_scan_tracker[ip])

    if len(ports) > SCAN_THRESHOLD:

        log_alert(f"Port Scan Detected from {ip}")

        block_ip(ip)

        port_scan_tracker[ip].clear()


def detect_syn_flood(ip, is_syn):

    if not is_syn:
        return

    now = time.time()

    syn_tracker[ip].append(now)

    syn_tracker[ip] = [
        t for t in syn_tracker[ip]
        if now - t < SYN_TIME_WINDOW
    ]

    if len(syn_tracker[ip]) > SYN_THRESHOLD:

        log_alert(f"SYN Flood Detected from {ip}")

        block_ip(ip)

        syn_tracker[ip].clear()

def detect_packet_flood(ip):

    now = time.time()

    packet_tracker[ip].append(now)

    packet_tracker[ip] = [
        t for t in packet_tracker[ip]
        if now - t < PACKET_RATE_WINDOW
    ]

    if len(packet_tracker[ip]) > PACKET_RATE_THRESHOLD:

        log_alert(f"Packet Flood Detected from {ip}")

        block_ip(ip)

        packet_tracker[ip].clear()
        
