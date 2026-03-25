import os
import time
import threading

from config import TEMP_BAN_TIME
from logger import log_block

temp_banned = {}
permanent_banned = set()

def block_ip(ip):

    if ip in permanent_banned:
        return

    # Second attack -> permanent ban
    if ip in temp_banned:

        permanent_banned.add(ip)

        os.system(f"iptable - A INPUT -s {ip} -j DROP")

        log_block(f"{ip} PERMANENTLY BANNED")

        return

    # first attack -> temporary ban
    os.system(f"iptables - A INPUT -s {ip} -j DROP")

    temp_banned[ip] = time.time()

    log_block(f"{ip} TEMPORARILY BANNED")

    threading.Thread(
        target=unban_ip,
        args=(ip,),
        daemon=True
        ).start()

def unban_ip(ip):
     time.sleep(TEMP_BAN_TIME)

     if ip in temp_banned:

         os.system(f"iptables -D INPUT -s {ip} -j DROP")

         del temp_banned[ip]
