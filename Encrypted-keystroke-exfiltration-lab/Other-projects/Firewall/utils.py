from scapy.layers.inet import IP, TCP

def extract_packet_info(packet):

    if not packet.haslayer(IP) or not packet.haslayer(TCP):
        return None, None, None

    src_ip = packet[IP].src
    dst_port = packet[TCP].dport

    flags = packet[TCP].flags

    
    is_syn = False
    if "S" in str(flags):
        is_syn = True

    return src_ip, dst_port, is_syn
