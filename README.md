# EAP-ATTACKER — WPA2-Enterprise Attack Framework

> **⚠️ For authorized penetration testing and educational purposes only.**
> Unauthorized use of these tools against networks you do not own or have explicit permission to test is **illegal** and **unethical**.

```
 ███████  █████  ██████       █████  ████████ ████████  █████   ██████ ██   ██ ███████ ██████  
 ██      ██   ██ ██   ██     ██   ██    ██       ██    ██   ██ ██      ██  ██  ██      ██   ██ 
 █████   ███████ ██████  ──  ███████    ██       ██    ███████ ██      █████   █████   ██████  
 ██      ██   ██ ██          ██   ██    ██       ██    ██   ██ ██      ██  ██  ██      ██   ██ 
 ███████ ██   ██ ██          ██   ██    ██       ██    ██   ██  ██████ ██   ██ ███████ ██   ██ 
```

A modular Python framework for testing WPA2-Enterprise (802.1X / EAP) network security. It combines rogue access point creation, credential harvesting, deauthentication attacks, KARMA probing, and hostile captive portal phishing into a single CLI-driven toolkit.

---

## Features

| Module | Description |
|---|---|
| **Evil Twin AP** | Spins up a rogue WPA2-EAP access point using `hostapd` to intercept RADIUS credentials |
| **Cert Wizard** | Generates fake CA and server certificates for the rogue RADIUS server |
| **Deauthentication** | Sends 802.11 deauth frames to disconnect clients from a target AP |
| **KARMA Attack** | Listens for probe requests and auto-spawns matching APs for any SSID clients are looking for |
| **Hostile Portal** | Serves a phishing captive portal mimicking a corporate login page to harvest AD credentials |

## EAP Negotiation Strategies

The framework supports three credential capture strategies via the `--negotiate` flag:

| Strategy | Flag | Best For | Captures |
|---|---|---|---|
| Balanced | `balanced` | General use | Cleartext (GTC) → Hash (MSCHAPv2) fallback |
| GTC Downgrade | `gtc-downgrade` | macOS / iOS | Cleartext passwords via GTC-only |
| Default | `default` | Windows / Android | NTLMv2 hashes via MSCHAPv2 |

---

## Project Structure

```
eapattacker/
├── eapattacker.py        # Main CLI entry point
├── rogue_ap.py           # Rogue AP launcher (hostapd config generator)
├── cert_wizard.py        # Fake certificate generator (OpenSSL)
├── deauth.py             # Targeted deauthentication attack
├── karma.py              # KARMA attack module
├── hostile_portal.py     # Captive portal credential phishing
├── requirements.txt      # Python dependencies
├── .gitignore
├── __init__.py
└── README.md
```

Generated at runtime:

```
├── certs/                # Created by --cert-wizard
│   ├── ca.pem
│   ├── ca.key
│   ├── server.pem
│   ├── server.key
│   └── server.csr
└── ad_creds.txt          # Created by --hostile-portal
```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/babySAMRAT/eapattacker.git
cd eapattacker

# Install Python dependencies
sudo apt install -y python3-scapy python3-flask
```

---

## Requirements

### System Dependencies

- **Linux** with a wireless adapter that supports **monitor mode**
- `hostapd` — for rogue AP creation
- `airmon-ng` (from `aircrack-ng`) — for monitor mode management
- `openssl` — for certificate generation
- `iw` / `iwconfig` — for wireless interface control

### Python Dependencies

Install with:

```bash
sudo apt install -y python3-scapy python3-flask
```

Or manually:

```bash
pip install scapy flask
```

---

## Usage

All attack commands require **root privileges** (`sudo`).

### 1. Generate Fake Certificates (run first!)

```bash
sudo python3 eapattacker.py --cert-wizard
```

This creates `ca.pem`, `server.pem`, and `server.key` inside `certs/`.

> **Note:** You must run this before using `--creds` or `--karma`, as both require valid certificates for the rogue RADIUS server.

### 2. Launch Evil Twin AP + Credential Capture

```bash
sudo python3 eapattacker.py -i wlan0 --essid "CorpWiFi" --creds
```

Optionally specify a negotiation strategy:

```bash
sudo python3 eapattacker.py -i wlan0 --essid "CorpWiFi" --creds --negotiate gtc-downgrade
```

### 3. Deauthenticate Clients from a Target AP

```bash
sudo python3 eapattacker.py -i wlan0 --essid "CorpWiFi" --deauth AA:BB:CC:DD:EE:FF
```

### 4. KARMA Attack (Auto-respond to All Probe Requests)

```bash
sudo python3 eapattacker.py -i wlan0 --essid "CorpWiFi" --karma
```

### 5. Hostile Portal (Captive Portal Phishing)

```bash
sudo python3 eapattacker.py -i wlan0 --essid "CorpWiFi" --hostile-portal
```

Captured credentials are saved to `ad_creds.txt`.

---

## Full CLI Reference

```
usage: eapattacker.py [-h] [-i INTERFACE] [--essid ESSID] [--channel CHANNEL]
                      [--auth {wpa-eap,open}] [--creds] [--hostile-portal]
                      [--karma] [--deauth BSSID]
                      [--negotiate {balanced,gtc-downgrade,default}]
                      [--cert-wizard]
```

| Argument | Description |
|---|---|
| `-i`, `--interface` | Wireless interface (e.g. `wlan0`) |
| `--essid` | Target SSID to clone |
| `--channel` | Channel number (default: `6`) |
| `--auth` | Auth type: `wpa-eap` or `open` |
| `--creds` | Launch evil twin and steal RADIUS credentials |
| `--hostile-portal` | Serve AD credential phishing portal |
| `--karma` | Enable KARMA attack (respond to all probes) |
| `--deauth BSSID` | Continuously deauth clients from the given AP |
| `--negotiate` | EAP negotiation strategy (`balanced`, `gtc-downgrade`, `default`) |
| `--cert-wizard` | Generate fake RADIUS certificates |

---

## Legal Disclaimer

This toolkit is provided strictly for **authorized security testing** and **educational research**. You are solely responsible for ensuring you have proper authorization before using these tools. The authors assume no liability for misuse.

---

*Built by **babysamrat***
