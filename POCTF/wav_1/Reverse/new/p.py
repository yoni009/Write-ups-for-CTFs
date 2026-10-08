import struct

def solve():
    filepath = "team_417.sav"
    
    with open(filepath, "rb") as f:
        data = f.read()

    offset = 0

    def read_fmt(fmt):
        nonlocal offset
        size = struct.calcsize(fmt)
        if offset + size > len(data):
            raise IndexError(f"Reached EOF at offset {offset}")
        res = struct.unpack_from(fmt, data, offset)
        offset += size
        return res[0] if len(res) == 1 else res

    def read_bytes(n):
        nonlocal offset
        if offset + n > len(data):
            raise IndexError(f"Reached EOF attempting to read {n} bytes at offset {offset}")
        res = data[offset:offset + n]
        offset += n
        return res

    # --- 1. HEADER ---
    magic = read_bytes(4)                           # 4 bytes: Static Magic Signature
    v_major, v_minor = read_fmt("<HH")              # Version info (u16, u16)
    payload_len = read_fmt("<I")                    # Payload length (u32)
    
    print(f"[*] Magic: {magic.hex()}")
    print(f"[*] Version: {v_major}.{v_minor}")
    print(f"[*] Expected Payload Length: {payload_len} bytes")

    # --- 2. PLAYER BLOCK ---
    p_len = read_fmt("B")                           # u8 name length
    p_name = read_bytes(p_len).decode("ascii", errors="ignore")
    p_level = read_fmt("<H")                        # u16 level
    p_gold = read_fmt("<I")                         # u32 gold

    print(f"[+] Player Name: {p_name}")
    print(f"[+] Level: {p_level} | Gold: {p_gold}")

    # --- 3. LOCATION BLOCK ---
    l_len = read_fmt("B")                           # u8 location name length
    l_name = read_bytes(l_len).decode("ascii", errors="ignore")
    print(f"[+] Location: {l_name}")

    # --- 4. INVENTORY ARRAY ---
    # Shape: u16 count -> (u16 item_id, u8 rarity, u8 name_len, name, u16 desc_len, desc)
    inv_count = read_fmt("<H")                      # u16 inventory count
    print(f"[*] Total Inventory Items: {inv_count}")

    item_names = []
    for i in range(inv_count):
        item_id = read_fmt("<H")                    # u16 item_id
        rarity = read_fmt("B")                      # u8 rarity
        
        n_len = read_fmt("B")                       # u8 name_len
        name = read_bytes(n_len).decode("ascii", errors="ignore")
        
        d_len = read_fmt("<H")                      # u16 desc_len
        desc = read_bytes(d_len)                    # desc bytes
        
        item_names.append(name)

    # --- 5. EXTRACT ACROSTIC FLAG ---
    # First 5 letters = P O C T F
    # Next 16 letters = Flag Body
    first_letters = [item[0] for item in item_names if item]
    full_acrostic = "".join(first_letters)

    print("\n" + "=" * 45)
    print(f"[+] Extracted First-Letter Sequence:\n    {full_acrostic}")
    print("=" * 45)

    if len(full_acrostic) >= 21:
        prefix = "".join(first_letters[:5])
        flag_body = "".join(first_letters[5:21])
        
        print(f"\n[+] Detected Acrostic Prefix: {prefix}")
        print(f"==========================================")
        print(f"  FLAG: POCTF{{{flag_body}}}")
        print(f"==========================================")
    else:
        print(f"[-] Warning: Acrostic shorter than 21 chars ({len(full_acrostic)} items found).")

if __name__ == "__main__":
    solve()