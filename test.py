import rsa
# import time
# tStart = time.time()#計時開始

key = "AAA31321vsdvsdvsd哈哈"
enc = rsa.encryption(key)
print(enc)
# print(enc[0])
# print(enc[1][0])
# print(rsa.decryption(m[0],m[1]))
dec = rsa.decryption(enc[0],enc[1][0],enc[1][1])

# tEnd = time.time()#計時結束
# print(tEnd - tStart)