#!/usr/bin/env python3
from pwn import log
import argparse
import os
import re
import sys
import urllib.request
from urllib.parse import urlparse


def is_url(s: str) -> bool:
    try:
        u = urlparse(s)
        return u.scheme in ("http", "https") and bool(u.netloc)
    except Exception:
        return False


def fetch_text(source: str) -> str:
    """
    If source is a URL, download it (wget-like) and return content.
    If source is a local path, read it from disk.
    """
    if is_url(source):
        log.info(f"Downloading: {source}")
        with urllib.request.urlopen(source) as r:
            data = r.read()
        try:
            text = data.decode("utf-8", errors="replace")
        except Exception:
            text = data.decode(errors="replace")
        log.success(f"Downloaded {len(text)} bytes")
        return text

    # local file
    if not os.path.exists(source):
        log.error(f"File not found: {source}")
        raise FileNotFoundError(source)

    log.info(f"Reading local file: {source}")
    with open(source, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    log.success(f"Read {len(text)} bytes")
    return text


def parse_asm2_constants(asm_text: str):
    """
    Extract loop behavior for the common asm2 pattern:
      - local2 is [ebp-0x8]
      - local1 is [ebp-0x4]
      - loop body includes:
            add/sub [ebp-0x4], IMM (usually 1)
            add/sub [ebp-0x8], IMM
        loop condition includes:
            cmp [ebp-0x8], IMM
            jle ... (so while local2 <= IMM)
    Returns:
      (delta_local1_per_iter, delta_local2_per_iter, threshold)
    """
    # Example lines:
    # <+24>: add DWORD PTR [ebp-0x4],0x1
    # <+28>: add DWORD PTR [ebp-0x8],0x9f
    # <+35>: cmp DWORD PTR [ebp-0x8],0x2d12

    # normalize spacing for easier regex
    t = asm_text

    # find delta for local1 ([ebp-0x4])
    m1 = re.search(r"\b(add|sub)\s+DWORD PTR\s+\[ebp-0x4\]\s*,\s*(0x[0-9a-fA-F]+|\d+)", t)
    if not m1:
        log.error("Could not find update instruction for local1 ([ebp-0x4]).")
        return None
    op1, imm1 = m1.group(1).lower(), m1.group(2)
    imm1_val = int(imm1, 0)
    delta1 = imm1_val if op1 == "add" else -imm1_val

    # find delta for local2 ([ebp-0x8])
    m2 = re.search(r"\b(add|sub)\s+DWORD PTR\s+\[ebp-0x8\]\s*,\s*(0x[0-9a-fA-F]+|\d+)", t)
    if not m2:
        log.error("Could not find update instruction for local2 ([ebp-0x8]).")
        return None
    op2, imm2 = m2.group(1).lower(), m2.group(2)
    imm2_val = int(imm2, 0)

    # In x86, immediates like 0xffffff80 may represent negative numbers in 32-bit.
    # We'll interpret as signed 32-bit when needed.
    def to_signed32(x: int) -> int:
        x &= 0xFFFFFFFF
        return x - 0x100000000 if x & 0x80000000 else x

    imm2_signed = to_signed32(imm2_val)
    # if instruction is sub, subtract signed immediate; if add, add signed immediate
    delta2 = imm2_signed if op2 == "add" else -imm2_signed

    # find cmp threshold
    m3 = re.search(r"\bcmp\s+DWORD PTR\s+\[ebp-0x8\]\s*,\s*(0x[0-9a-fA-F]+|\d+)", t)
    if not m3:
        log.error("Could not find cmp threshold for local2 ([ebp-0x8]).")
        return None
    threshold = int(m3.group(1), 0)

    log.info(f"Parsed loop constants:")
    log.info(f"  local1 delta/iter = {delta1} (0x{(delta1 & 0xFFFFFFFF):x})")
    log.info(f"  local2 delta/iter = {delta2} (0x{(delta2 & 0xFFFFFFFF):x})")
    log.info(f"  threshold         = 0x{threshold:x}")

    return delta1, delta2, threshold


def solve_asm2(arg1: int, arg2: int, delta1: int, delta2: int, threshold: int) -> int:
    """
    Based on parsed pattern:
      local1 = arg2
      local2 = arg1
      while local2 <= threshold:
          local1 += delta1
          local2 += delta2
      return local1

    We compute iterations mathematically when delta2 moves monotonically upward.
    Fallback to safe simulation if needed.
    """
    local1 = arg2
    local2 = arg1

    # If delta2 <= 0, the loop may never terminate depending on start/threshold.
    # For safety, we simulate with a hard cap.
    if delta2 <= 0:
        log.warning("delta2 <= 0 (local2 not increasing). Falling back to capped simulation.")
        cap = 10_000_000
        it = 0
        while local2 <= threshold:
            local1 = (local1 + delta1) & 0xFFFFFFFF
            local2 = (local2 + delta2) & 0xFFFFFFFF
            it += 1
            if it > cap:
                log.error("Simulation cap reached — loop may be non-terminating with these constants.")
                raise RuntimeError("Non-terminating loop?")
        log.success(f"Simulated iterations: {it}")
        return local1 & 0xFFFFFFFF

    # If already above threshold, zero iterations.
    if local2 > threshold:
        return local1 & 0xFFFFFFFF

    # We need smallest k such that: local2 + delta2*k > threshold
    # => delta2*k > threshold - local2
    diff = threshold - local2
    k = (diff // delta2) + 1  # ceil((diff+1)/delta2) effectively
    log.success(f"Computed iterations: {k}")

    local1 = (local1 + delta1 * k) & 0xFFFFFFFF
    return local1


def main():
    ap = argparse.ArgumentParser(
        description="Solve picoCTF asm2-style challenge by parsing test.S from disk or URL (pwntools-style)."
    )
    ap.add_argument("source", help="Path to test.S or URL to download it (e.g. https://.../test.S)")
    ap.add_argument("--arg1", default="0x6", help="First argument (default: 0x6)")
    ap.add_argument("--arg2", default="0x21", help="Second argument (default: 0x21)")
    args = ap.parse_args()

    arg1 = int(args.arg1, 0)
    arg2 = int(args.arg2, 0)

    asm_text = fetch_text(args.source)
    parsed = parse_asm2_constants(asm_text)
    if not parsed:
        log.error("Failed to parse assembly constants. Check file format.")
        sys.exit(1)

    delta1, delta2, threshold = parsed
    result = solve_asm2(arg1, arg2, delta1, delta2, threshold)

    print(hex(result))


if __name__ == "__main__":
    main()
