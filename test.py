import rsa
# import time
# tStart = time.time()#計時開始
key = "AAA31321vsdvsdvsd哈哈"
key_pair = rsa.gen_key()
pub = key_pair[0]
priv = key_pair[1]
enc = rsa.encryption(key, pub[0], pub[1])
# print(enc)
# print(enc[0])
# print(enc[1][0])
# print(rsa.decryption(m[0],m[1]))
dec = rsa.decryption(enc, priv[0], priv[1])
print(dec)
# tEnd = time.time()#計時結束
# print(tEnd - tStart)