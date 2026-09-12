#!/usr/bin/env python3
"""Flag'in sha256 hash'ini üretir — lab.yml'ye bunu yazarsın (düz metni ASLA).

Kullanım:
    python3 scripts/flag_hash.py 'TUGA{ornek_flag}'
    python3 scripts/flag_hash.py            # sorar (terminale flag yazdırmadan)
"""
import hashlib
import sys


def main():
    if len(sys.argv) > 1:
        flag = sys.argv[1]
    else:
        import getpass
        flag = getpass.getpass("Flag (ekrana yazılmaz): ")
    flag = flag.strip()
    if not flag:
        sys.exit("Boş flag.")
    print(hashlib.sha256(flag.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
