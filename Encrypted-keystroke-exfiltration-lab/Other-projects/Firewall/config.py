#------------------------
# Port Scan Detection
#------------------------

SCAN_THRESHOLD = 10
SCAN_TIME_WINDOW = 5

#------------------------
# SYN Flood Detection
#------------------------

SYN_THRESHOLD = 30
SYN_TIME_WINDOW = 5

#------------------------
# Packet Flood Detection
#------------------------

PACKET_RATE_THRESHOLD = 100
PACKET_RATE_WINDOW =3

#------------------------
# Ban Configuration
#------------------------

TEMP_BAN_TIME = 60

#------------------------
# Whitelist
#------------------------

WHITELIST = [
    "127.0.0.1"
    ]
