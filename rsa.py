import random
import base64
"""
    todo : 隨機大數質數  , PowerMod /2問題 //2連小數有問題  , 英文+數字 
"""

# # 確定是否為質數
# def isPrime(number):
#     for i in range(2,number):
#         if number % i == 0:
#             return False
#     return True

# 比較兩者是否互質


def computeGCD(x, y):

    while(y):
        x, y = y, x % y

    return x


p = 2**512-1
q = 2**1279-1

# p = random.randint(10**64,10**128)
# while isPrime(p)==False:
#     p = random.randint(10**64,10**128)

# q = random.randint(10**64,10**128)
# while isPrime(q)==False:
#     q = random.randint(10**64,10**128)

N = p * q
fn = (p-1)*(q-1)
e = 0
# 用線性找最小的互質數
for i in range(2, fn-1):
    if computeGCD(i, fn) == 1:
        e = i
        break
print(e)

# 擴展歐幾里德算法 求出d ( e*d ≡ 1 (mod φ(n)) )


def ext_euclid(a, b):
    old_s = 1
    s = 0
    old_t = 0
    t = 1
    old_r = a
    r = b
    if b == 0:
        return 1, 0, a
    else:
        while(r != 0):
            q = old_r//r
            old_r, r = r, old_r-q*r
            old_s, s = s, old_s-q*s
            old_t, t = t, old_t-q*t
    if old_s < 0:
        old_s += fn
    return old_s, old_t, old_r


d = ext_euclid(e, fn)
print(d[0])
d = d[0]

# 建立public and private key
publicKey = [e, N]
privateKey = [d, N]

# 利用快速冪取餘數


def PowerMod(a, b, c):
    ans = 1
    a = a % c
    while(b > 0):
        if b % 2 == 1:
            ans = (ans * a) % c
        b >>= 1
    return ans

# def PowerMod(a, b, c):
#     i = 1
#     ans = 1
#     for i in range(b):
#         ans = (ans * a) % c
#     return ans


# 加密 m^e ≡ c (mod N)
arr = []
m = "FUCKME"
for i in range(len(m)):
    arr.append(ord(m[i]))
print(arr)
c = PowerMod(m, e, N)
# c = (m**e) % N
# 解密 c^d ≡ m (mod N)
ansM = PowerMod(c, d, N)
# ansM = (c**d) % N

print(ansM)



"""
import random
import base64


# # 確定是否為質數
# def isPrime(number):
#     for i in range(2,number):
#         if number % i == 0:
#             return False
#     return True

# 比較兩者是否互質
def computeGCD(x, y): 
  
   while(y): 
       x, y = y, x % y 
  
   return x 

p = 2**512-1
q = 2**1279-1

# p = random.randint(10**64,10**128)
# while isPrime(p)==False:
#     p = random.randint(10**64,10**128)

# q = random.randint(10**64,10**128)
# while isPrime(q)==False:
#     q = random.randint(10**64,10**128)

N = p * q
fn = (p-1)*(q-1)
e = 0
# 用線性找最小的互質數
for i in range(2,fn-1):
    if computeGCD(i,fn)==1:
        e = i
        break
print(e)

# 擴展歐幾里德算法 求出d ( e*d ≡ 1 (mod φ(n)) )
def ext_euclid(a, b):
    old_s = 1
    s = 0
    old_t = 0
    t = 1
    old_r = a
    r = b
    if b == 0:
        return 1, 0, a
    else:
        while(r!=0):
            q=old_r//r
            old_r,r=r,old_r-q*r
            old_s,s=s,old_s-q*s
            old_t,t=t,old_t-q*t
    if old_s < 0:
        old_s += fn
    return old_s, old_t, old_r

d = ext_euclid(e,fn)
print(d[0])
d = d[0]

# 建立public and private key
publicKey = [e,N]
privateKey = [d,N]

# 利用快速冪取餘數
def PowerMod ( a, b, c):
    ans = 1
    a %=  c
    base = a
    while(b>0):
        if b % 2 == 1:
            ans = (ans * base) % c
        else:
            base = (base*base)%c
        b >>= 1
             
    return ans

# def PowerMod(a, b, c):
#     i = 1 
#     ans = 1
#     for i in range(b):
#         ans = (ans * a) % c
#     return ans


# 加密 m^e ≡ c (mod N)
arr = []
m ="FUCKME"
for i in range(len(m)):
    arr.append(ord(m[i]))
print(arr)
c = []
for i in arr:
    c.append(PowerMod(i,e,N))
# c = (m**e) % N
# 解密 c^d ≡ m (mod N)

for i in c:
    ansM = PowerMod(i,d,N)
    # ansM = (c**d) % N

    print(ansM)

"""
