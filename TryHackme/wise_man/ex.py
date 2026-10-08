import socket
import string
import re

HOST = '10.49.191.130'  # Your TryHackMe target IP
PORT = 1337

def solve():
    # 1. Open socket connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    # 2. Receive the challenge prompt
    data = ""
    while "encryption key?" not in data:
        chunk = s.recv(1024).decode()
        if not chunk:
            break
        data += chunk

    print("[+] Received from server:\n" + data)

    # 3. Extract the ciphertext hex string
    match = re.search(r'flag 1: ([0-9a-fA-F]+)', data)
    if not match:
        print("[-] Could not extract hex string!")
        s.close()
        return

    hex_str = match.group(1)
    ct = bytes.fromhex(hex_str)

    # 4. First 4 characters of key from known "THM{" prefix
    known_prefix = b"THM{"
    key_prefix = bytes([ct[i] ^ known_prefix[i] for i in range(4)])

    # 5. 5th key character from the final '}' byte at the end of flag 1
    # Index 39 (or ct_len - 1) corresponds to index 4 in a 5-byte repeating key (39 % 5 = 4)
    char5 = ct[-1] ^ ord('}')
    
    full_key = (key_prefix + bytes([char5])).decode()
    
    print(f"[+] Instantly calculated active Key: {full_key}")

    # 6. Decrypt and display Flag 1
    decrypted = bytes([ct[i] ^ ord(full_key[i % 5]) for i in range(len(ct))])
    print(f"[+] Flag 1: {decrypted.decode()}")

    # 7. Send key back over the SAME connection
    print(f"[+] Sending key '{full_key}' back to server...")
    s.sendall((full_key + "\n").encode())

    # 8. Print Flag 2 response
    response = s.recv(4096).decode()
    print("[+] Server Response:\n" + response)

    s.close()

if __name__ == '__main__':
    solve()