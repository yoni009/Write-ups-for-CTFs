import os

def solve_payload(file_path):
    with open(file_path, "rb") as f:
        data = f.read()

    # Skip 12-byte save header
    payload = data[12:]
    tail = payload[1132:] if len(payload) >= 1401 else payload

    print(f"[+] Loaded {file_path}: Total {len(data)} bytes, Tail {len(tail)} bytes")

    # Try multi-byte XOR stream derivation using rolling LCG state
    # Key formula: K_i = (A * i + B) ^ C
    found_tokens = []

    for a in range(1, 256, 2):  # Odd multipliers for full period
        for b in range(256):
            for c in range(256):
                dec = []
                for i, byte in enumerate(tail):
                    keystream_byte = ((a * i + b) & 0xFF) ^ c
                    dec.append(byte ^ keystream_byte)
                
                dec_bytes = bytes(dec)
                if b"POCTF" in dec_bytes:
                    print(f"[!] MATCH FOUND with A={a}, B={b}, C={c}!")
                    print(f"    Decrypted tail preview: {dec_bytes}")
                    return dec_bytes
                
                # Check for 16-character ASCII tokens
                import re
                tokens = re.findall(rb'[a-zA-Z0-9_]{16}', dec_bytes)
                for t in tokens:
                    if len(set(t)) >= 10:  # High character diversity filter
                        found_tokens.append((a, b, c, t.decode('ascii', errors='ignore')))

    if found_tokens:
        print("[+] Potential Candidate Tokens:")
        for a, b, c, tok in found_tokens[:5]:
            print(f"    Key params (A={a}, B={b}, C={c}) -> Token: {tok}")

if __name__ == "__main__":
    solve_payload("Team.sav" if os.path.exists("Team.sav") else "source_4.bin")