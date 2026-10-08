import sys

def extract_flag(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    lines = data.split(b'\n')
    bits = []
    for line in lines:
        line = line.rstrip(b'\r')
        trailing = b''
        for b in reversed(line):
            if b in (0x20, 0x09):  # space or tab
                trailing = bytes([b]) + trailing
            else:
                break
        for b in trailing:
            bits.append('0' if b == 0x20 else '1')  # space=0, tab=1
    bits_str = ''.join(bits)
    # Pad to multiple of 8
    if len(bits_str) % 8 != 0:
        bits_str += '0' * (8 - len(bits_str) % 8)
    chars = []
    for i in range(0, len(bits_str), 8):
        byte = bits_str[i:i+8]
        chars.append(chr(int(byte, 2)))
    return ''.join(chars)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python extract.py invisible_text_417.py")
        sys.exit(1)
    flag = extract_flag(sys.argv[1])
    print("Flag:", flag)