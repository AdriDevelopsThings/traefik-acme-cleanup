#!/usr/bin/env python3
from argparse import ArgumentParser, FileType

import json
import socket

parser = ArgumentParser(
    prog="traefik-acme-cleanup",
    description="Clean domains that does not exist anymore from traefik acme json file",
)

parser.add_argument(
    "file", help="Path to the acme storage json file", type=FileType(mode="r+")
)
parser.add_argument("-c", "--certificate-authority", type=str, default="letsencrypt")


def is_valid_certificate(certificate: dict) -> bool:
    if "domain" not in certificate or "main" not in certificate["domain"]:
        return True
    domain = certificate["domain"]["main"]
    print(f"Checking {domain} ", end="")
    try:
        socket.gethostbyname(domain)
        print("✓")
        return True
    except socket.gaierror:
        print("✕")
        return False


if __name__ == "__main__":
    args = parser.parse_args()
    file = args.file
    j = json.load(file)

    certificates = j[args.certificate_authority]["Certificates"]
    certificates = [c for c in certificates if is_valid_certificate(c)]
    j[args.certificate_authority]["Certificates"] = certificates
    if input("Save? [y/n] ") == "y":
        file.seek(0)
        json.dump(j, file, indent=4)
        file.truncate()
    file.close()
