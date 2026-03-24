#!/usr/bin/env python3
import argparse
import sys
import os

# Make sure imports work from same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BANNER = """
 ███████  █████  ██████       █████  ████████ ████████  █████   ██████ ██   ██ ███████ ██████  
 ██      ██   ██ ██   ██     ██   ██    ██       ██    ██   ██ ██      ██  ██  ██      ██   ██ 
 █████   ███████ ██████  ──  ███████    ██       ██    ███████ ██      █████   █████   ██████  
 ██      ██   ██ ██          ██   ██    ██       ██    ██   ██ ██      ██  ██  ██      ██   ██ 
 ███████ ██   ██ ██          ██   ██    ██       ██    ██   ██  ██████ ██   ██ ███████ ██   ██ 

         WPA2-Enterprise Attack Framework
         For authorized penetration testing only
         ─────────── by babysamrat ───────────
"""

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(
        description="WPA2-Enterprise Attack Framework",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("-i", "--interface", required=False,
                        help="Wireless interface (e.g. wlan0)")
    parser.add_argument("--essid", required=False,
                        help="Target SSID to clone")
    parser.add_argument("--channel", type=int, default=6,
                        help="Channel number (default: 6)")
    parser.add_argument("--auth", choices=["wpa-eap", "open"],
                        default="wpa-eap",
                        help="Auth type: wpa-eap or open (default: wpa-eap)")
    parser.add_argument("--creds", action="store_true",
                        help="Steal RADIUS credentials via evil twin")
    parser.add_argument("--hostile-portal", action="store_true",
                        help="Launch AD credential phishing portal")
    parser.add_argument("--karma", action="store_true",
                        help="Enable KARMA attack (respond to all probes)")
    parser.add_argument("--deauth", metavar="BSSID",
                        help="Continuously deauth clients from this AP BSSID")
    parser.add_argument("--negotiate",
                        choices=["balanced", "gtc-downgrade", "default"],
                        default="balanced",
                        help=(
                            "EAP negotiation strategy:\n"
                            "  balanced     = try GTC (cleartext) then MSCHAPv2 (hash)\n"
                            "  gtc-downgrade = force GTC only (cleartext, macOS/iOS)\n"
                            "  default      = MSCHAPv2 only (Windows/Android)"
                        ))
    parser.add_argument("--cert-wizard", action="store_true",
                        help="Generate fake RADIUS certificates")

    args = parser.parse_args()

    # ── Cert Wizard (no interface or essid needed) ──────────────
    if args.cert_wizard:
        from cert_wizard import generate_certs
        generate_certs()
        return

    # ── All other attacks need -i and --essid ───────────────────
    if not args.interface or not args.essid:
        print("[!] Error: -i/--interface and --essid are required for attacks")
        parser.print_help()
        sys.exit(1)

    # ── Evil Twin + Credential Capture ──────────────────────────
    if args.creds:
        from rogue_ap import launch_ap
        launch_ap(args.interface, args.essid, args.channel, args.negotiate)

    # ── KARMA Attack ────────────────────────────────────────────
    if args.karma:
        from karma import start_karma
        start_karma(f"{args.interface}mon")

    # ── Deauthentication Attack ──────────────────────────────────
    if args.deauth:
        from deauth import deauth_attack
        deauth_attack(f"{args.interface}mon", args.deauth, count=0)

    # ── Hostile Portal ───────────────────────────────────────────
    if args.hostile_portal:
        from hostile_portal import start_portal
        start_portal()


if __name__ == "__main__":
    main()
