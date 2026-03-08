import hashlib, struct

serial   = b"ROUTER-61AAE6FC6A83FD56"
exe_hash = bytes.fromhex("")  # hash của binary hiện tại
secret   = struct.pack("<QQ", 0x334F5561102A3C19, 0x4C18217E0A6B2D72)

master_key = hashlib.sha256(serial + secret + exe_hash).digest()

dat  = open("etc/cloudsync/backup.dat", "rb").read()
iv   = dat[0x05:0x15]
ct   = dat[0x19:0x40]
key1 = master_key[:16]

flag = b""
for i in range((len(ct) + 31) // 32):
    ks    = hashlib.sha256(key1 + iv + struct.pack("<I", i)).digest()
    chunk = ct[i*32:(i+1)*32]
    flag += bytes(a ^ b for a, b in zip(ks, chunk))

print(flag[:39])