import sys

def extract_flag(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    flag = ''
    for line in lines:
        line = line.rstrip('\n')
        # Collect trailing spaces and tabs
        trailing = ''
        for ch in reversed(line):
            if ch in ' \t':
                trailing = ch + trailing
            else:
                break
        # Ignore lines that have only one trailing whitespace char (just a tab)
        if len(trailing) > 1:
            # Map space=0, tab=1
            bits = ''.join('0' if c == ' ' else '1' for c in trailing)
            # Convert binary to integer, then to ASCII character
            val = int(bits, 2)
            flag += chr(val)
    return flag

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python extract.py invisible_text_417.py")
        sys.exit(1)
    print("Flag:", extract_flag(sys.argv[1]))