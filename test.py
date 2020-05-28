import rsa
key ="中文fuck"
enc = rsa.encryption(key)
print(enc)
# print(enc[0])
# print(enc[1][0])
# print(rsa.decryption(m[0],m[1]))
dec = rsa.decryption(enc[0],enc[1][0],enc[1][1])