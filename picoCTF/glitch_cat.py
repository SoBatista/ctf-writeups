#!/usr/bin/env python3
"""
glitchcat.py
Plain and simple: connect, print whatever the server sends, decode a line like:
  'picoCTF{gl17ch_m3_n07_' + chr(0x61) + chr(0x34) + '}'
into the assembled string.

Usage:
    python3 glitchcat.py
    python3 glitchcat.py host port
"""
import sys
from pwn import remote

HOST = "saturn.picoctf.net"
PORT = 57885
TIMEOUT = 2.0

def decode_token(token: str) -> str:
    token = token.strip()
    if (token.startswith("'") and token.endswith("'")) or (token.startswith('"') and token.endswith('"')):
        return token[1:-1]            # remove quotes (no escape handling, keeps it simple)
    if token.startswith("chr(") and token.endswith(")"):
        inner = token[4:-1].strip()
        try:
            # allow hex (0x..) or decimal (e.g. 97)
            val = int(inner, 0)
            return chr(val)
        except Exception:
            return ""   # on error, return empty so it won't break the join
    # nothing matched
    return ""

def decode_concat_line(line: str) -> str:
    # split on + (the challenge uses '+' between pieces)
    parts = [p for p in line.split('+')]
    decoded_parts = [decode_token(p) for p in parts]
    return "".join(decoded_parts)

def main():
    host = sys.argv[1] if len(sys.argv) > 1 else HOST
    port = int(sys.argv[2]) if len(sys.argv) > 2 else PORT

    r = remote(host, port, timeout=10)

    try:
        # receive everything available (short timeout)
        raw = b""
        while True:
            try:
                chunk = r.recv(timeout=TIMEOUT)
            except Exception:
                break
            if not chunk:
                break
            raw += chunk

        text = raw.decode(errors="replace").strip()
        if not text:
            print("[!] No data received.")
            return

        # print raw output so user can inspect
        print("----- RAW OUTPUT -----")
        print("[+]", text)
        print("----------------------")

        # try each line until one decodes to something non-empty
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            decoded = decode_concat_line(line)
            if decoded:
                print("\n[+] Decoded assembled string:")
                print(decoded)
                # if it's not a full picoCTF{...} flag, you can wrap it:
                if decoded.startswith("picoCTF{") and decoded.endswith("}"):
                    print("\n[+] Flag:", decoded)
                else:
                    print("\n[+] Wrapped flag:", f"picoCTF{{gl17ch_m3_n07_{decoded}}}")
                break
        else:
            print("\n[!] No concatenation-like line was decoded.")
    finally:
        r.close()

if __name__ == "__main__":
    main()
