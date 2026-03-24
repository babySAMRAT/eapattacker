import subprocess
import os

def generate_certs(cn="FakeRADIUS", org="Corp", country="IN"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cert_dir = os.path.join(base_dir, "certs")
    os.makedirs(cert_dir, exist_ok=True)

    # Generate CA key + self-signed certificate
    subprocess.run([
        "openssl", "req", "-new", "-x509", "-nodes",
        "-keyout", os.path.join(cert_dir, "ca.key"),
        "-out", os.path.join(cert_dir, "ca.pem"),
        "-days", "3650",
        "-subj", f"/C={country}/O={org}/CN={cn}-CA"
    ], check=True)

    # Generate server key + CSR
    subprocess.run([
        "openssl", "req", "-new", "-nodes",
        "-keyout", os.path.join(cert_dir, "server.key"),
        "-out", os.path.join(cert_dir, "server.csr"),
        "-subj", f"/C={country}/O={org}/CN={cn}"
    ], check=True)

    # Sign server cert with CA
    subprocess.run([
        "openssl", "x509", "-req",
        "-in", os.path.join(cert_dir, "server.csr"),
        "-CA", os.path.join(cert_dir, "ca.pem"),
        "-CAkey", os.path.join(cert_dir, "ca.key"),
        "-CAcreateserial",
        "-out", os.path.join(cert_dir, "server.pem"),
        "-days", "3650"
    ], check=True)

    print(f"[+] Certificates generated successfully in {cert_dir}/")
    print("    ca.pem | ca.key | server.pem | server.key | server.csr")
