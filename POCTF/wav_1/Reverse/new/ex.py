import struct

def try_key(filename, key):
    with open(filename, 'rb') as f:
        data = f.read()
    payload = data[12:]
    if isinstance(key, int):
        key_bytes = bytes([key])
    else:
        key_bytes = key
    decrypted = bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(payload))
    # Validate name field
    name_len = decrypted[0]
    if not (1 <= name_len <= 20):
        return None
    name = decrypted[1:1+name_len]
    if not all(32 <= c < 127 for c in name):
        return None
    off = 1 + name_len
    if off + 8 > len(decrypted):
        return None
    amount = struct.unpack_from('<I', decrypted, off)[0]
    money = struct.unpack_from('<I', decrypted, off+4)[0]
    off += 8
    loc_len = decrypted[off]
    off += 1
    if not (0 <= loc_len <= 50):
        return None
    loc = decrypted[off:off+loc_len]
    if not all(32 <= c < 127 for c in loc):
        return None
    off += loc_len
    if off + 2 > len(decrypted):
        return None
    inv_count = struct.unpack_from('<H', decrypted, off)[0]
    if not (0 <= inv_count <= 100):
        return None
    return name.decode(), amount, money, loc.decode(), inv_count

def find_key(filename):
    # Try 1-byte
    for k in range(256):
        res = try_key(filename, k)
        if res:
            print(f"1-byte key: {k:02x} -> {res}")
            return k
    # Try 2-byte
    for k1 in range(256):
        for k2 in range(256):
            key = bytes([k1, k2])
            res = try_key(filename, key)
            if res:
                print(f"2-byte key: {k1:02x}{k2:02x} -> {res}")
                return key
    print("No key found")
    return None

def parse_items(filename, key):
    with open(filename, 'rb') as f:
        data = f.read()
    payload = data[12:]
    if isinstance(key, int):
        key_bytes = bytes([key])
    else:
        key_bytes = key
    decrypted = bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(payload))
    off = 0
    name_len = decrypted[off]; off += 1
    name = decrypted[off:off+name_len].decode('latin-1'); off += name_len
    off += 8  # amount, money
    loc_len = decrypted[off]; off += 1
    loc = decrypted[off:off+loc_len].decode('latin-1'); off += loc_len
    inv_count = struct.unpack_from('<H', decrypted, off)[0]; off += 2
    items = []
    for i in range(inv_count):
        item_id = struct.unpack_from('<H', decrypted, off)[0]; off += 2
        rarity = decrypted[off]; off += 1
        name_len = decrypted[off]; off += 1
        item_name = decrypted[off:off+name_len].decode('latin-1'); off += name_len
        desc_len = struct.unpack_from('<H', decrypted, off)[0]; off += 2
        desc = decrypted[off:off+desc_len].decode('latin-1'); off += desc_len
        items.append(item_name)
    first_letters = ''.join(item[0] for item in items if item)
    print("First letters:", first_letters)
    if first_letters.startswith('POCTF'):
        token = first_letters[5:21]
        print(f"Token: {token}")
        print(f"Flag: POCTF{{{token}}}")
    else:
        print("First letters do not start with POCTF. Check parsing.")

if __name__ == '__main__':
    key = find_key('team_417.sav')
    if key:
        parse_items('team_417.sav', key)
