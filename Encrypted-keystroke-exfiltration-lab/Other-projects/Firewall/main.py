from scapy.all import sniff
from utils import extract_packet_info

from detctor import (
    detect_port_scan,
    detect_syn_flood,
    detect_packet_flood
    )

from logger import log_allow, log_info
from config import WHITELIST

import signal
import sys

packets_monitored = 0

def banner():

    print("""
===============================
SMART PERSONAL FIREWALL v1.0
IDS + IPS HYBRID
===============================
""")


def process_packet(packet):

    global packets_monitored

    try:
        ip, port, is_syn = extract_packet_info(packet)

        if not ip:
            return

        if ip in WHITELIST:
            return

        packets_monitored += 1

        log_allow(ip, port)

        detect_port_scan(ip, port)
        detect_syn_flood(ip, is_syn)
        detect_packet_flood(ip)

    except Exception as e:
        print(f"[ERROR] Packet processing failed: {e}")

def shutdown(sig, frame):

    print("\n\nFirewall shutting down safely...")

    print(f"Packets monitored: {packets_monitored}")

    sys.exit(0)


def start_firewall():

    banner()

    log_info("Firewall Started")

    signal.signal(signal.SIGINT, shutdown)

    sniff(
        filter="tcp",
        prn=process_packet,
        store=0
        )

if __name__ == "__main__":
    start_firewall()
