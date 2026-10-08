from pathlib import Path
import string

data = Path("team_417.sav").read_bytes()

def printable(s):
    return all(32 <= x < 127 for x in s)

for off in range(12, len(data)-2):
    count = int.from_bytes(data[off:off+2], "little")

    if not (1 <= count <= 100):
        continue

    pos = off + 2
    records = []

    try:
        for i in range(count):
            item_id = int.from_bytes(data[pos:pos+2], "little")
            rarity = data[pos+2]
            name_len = data[pos+3]

            if not (1 <= name_len <= 80):
                raise ValueError

            pos += 4

            name = data[pos:pos+name_len]
            if len(name) != name_len or not printable(name):
                raise ValueError

            pos += name_len

            desc_len = int.from_bytes(data[pos:pos+2], "little")
            if desc_len > 1000:
                raise ValueError

            pos += 2
            desc = data[pos:pos+desc_len]

            if len(desc) != desc_len:
                raise ValueError

            pos += desc_len
            records.append((item_id, rarity, name.decode(), desc.decode(errors="replace")))

        if count >= 5:
            print(f"\nCANDIDATE offset: 0x{off:x}, count={count}")
            for n, (item_id, rarity, name, desc) in enumerate(records[:25], 1):
                print(f"{n:2}: {name!r}")

    except (ValueError, IndexError, UnicodeDecodeError):
        pass
