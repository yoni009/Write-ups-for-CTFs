from pathlib import Path
import math

FILES = [
    "sample1.sav",
    "sample2.sav",
    "sample3.sav",
    "team_417.sav",
]

def printable_score(data):
    if not data:
        return 0
    return sum(32 <= b <= 126 or b in (9,10,13) for b in data) / len(data)

def alpha_score(data):
    if not data:
        return 0
    return sum(
        b in range(ord('a'), ord('z')+1) or
        b in range(ord('A'), ord('Z')+1) or
        b in range(ord('0'), ord('9')+1) or
        b in b" _-{}[]:=,./"
        for b in data
    ) / len(data)

def strings(data, minimum=5):
    out = []
    cur = bytearray()

    for b in data:
        if 32 <= b <= 126:
            cur.append(b)
        else:
            if len(cur) >= minimum:
                out.append(cur.decode(errors="replace"))
            cur.clear()

    if len(cur) >= minimum:
        out.append(cur.decode(errors="replace"))

    return out

def rol8(x, n):
    return ((x << n) | (x >> (8-n))) & 0xff

def ror8(x, n):
    return ((x >> n) | (x << (8-n))) & 0xff

def reverse_bits(x):
    return int(f"{x:08b}"[::-1], 2)

def nibble_swap(x):
    return ((x & 0xf) << 4) | ((x & 0xf0) >> 4)

def swap_bits(x, a, b):
    ba = (x >> a) & 1
    bb = (x >> b) & 1
    if ba != bb:
        x ^= (1 << a) | (1 << b)
    return x

def transforms(data):
    yield "identity", data
    yield "NOT", bytes((~b) & 255 for b in data)
    yield "nibble_swap", bytes(nibble_swap(b) for b in data)
    yield "reverse_bits", bytes(reverse_bits(b) for b in data)

    for n in range(1, 8):
        yield f"ROL{n}", bytes(rol8(b,n) for b in data)
        yield f"ROR{n}", bytes(ror8(b,n) for b in data)

    for k in range(256):
        yield f"XOR_{k:02x}", bytes(b ^ k for b in data)

    for k in range(1, 256):
        yield f"ADD_{k:02x}", bytes((b + k) & 255 for b in data)
        yield f"SUB_{k:02x}", bytes((b - k) & 255 for b in data)

for filename in FILES:
    data = Path(filename).read_bytes()[12:]

    results = []

    for name, transformed in transforms(data):
        ps = printable_score(transformed)
        als = alpha_score(transformed)

        sigs = []

        for sig, label in [
            (b"PK\x03\x04", "ZIP"),
            (b"\x1f\x8b", "GZIP"),
            (b"x\x9c", "ZLIB"),
            (b"x\xda", "ZLIB"),
            (b"\x7fELF", "ELF"),
            (b"{", "JSON"),
            (b"[", "JSON_ARRAY"),
            (b"RIFF", "RIFF"),
            (b"OggS", "OGG"),
            (b"%PDF", "PDF"),
        ]:
            if sig in transformed:
                sigs.append(label)

        results.append((als, ps, name, transformed, sigs))

    results.sort(reverse=True, key=lambda x: (x[0], x[1]))

    print("\n" + "=" * 80)
    print(filename)

    for als, ps, name, transformed, sigs in results[:20]:
        print(
            f"{name:12} "
            f"structured={als*100:6.2f}% "
            f"printable={ps*100:6.2f}% "
            f"sigs={sigs}"
        )

        ss = strings(transformed)

        if ss:
            print("   ", ss[:3])

