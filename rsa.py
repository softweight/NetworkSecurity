import random
flag = 0
bitsNumber = 512

# 利用快速冪取餘數
def PowerMod(a, b, c):
    ans = 1
    a = a % c
    base = a
    while(b > 0):
        if b % 2 == 1:
            ans = (ans * base) % c
        b >>= 1
        base  = (base*base)%c
    return ans

def encryption(m, e, N):
    # 加密 m^e ≡ c (mod N)
    m = m.encode("UTF-8")
    #print(chr(m[0]))
    #for i in range(len(m)):
    #    arr.append(ord(m[i]))
    c=[]
    for i in m:
        c.append(PowerMod(i,e,N))
    #c = PowerMod(m, e, N)
    # c = (m**e) % N
    return c

def decryption(c, d, N):   
    # 解密 c^d ≡ m (mod N)
    #ansM = PowerMod(c, d, N)
    # ansM = (c**d) % N
    #print(ansM)
    ans = bytearray()
    for i in c:
        ansM = PowerMod(i,d,N)
        # ansM = (c**d) % N
        ans.append(ansM)
    ans = ans.decode('UTF-8')
    return ans

# Miller-Rabin質數檢測演算法
def miller_rabin(n, k):
    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def computeGCD(x, y):
    while(y):
        x, y = y, x % y

    return x

# 擴展歐幾里德算法 求出d ( e*d ≡ 1 (mod φ(n)) )
def ext_euclid(a, b):
    old_s = 1
    s = 0
    old_r = a
    r = b
    if b == 0:
        return 1, 0, a
    else:
        while(r != 0):
            q = old_r//r
            old_r, r = r, old_r-q*r
            old_s, s = s, old_s-q*s
    if old_s < 0:
        old_s += b
    return old_s

def gen_key():
    flag = 0
    e = 0
    d = 0
    N = 0
    while flag == 0:

        p = (random.getrandbits(bitsNumber)) * 30 + 1
        while miller_rabin(p,100)==False:
            p = (random.getrandbits(bitsNumber)) * 30 + 1

        q = (random.getrandbits(bitsNumber)) * 30 + 1 
        while miller_rabin(q,100)==False:
            q = (random.getrandbits(bitsNumber)) * 30 + 1 

        N = p * q
        fn = (p-1)*(q-1)
        e = 0

        # 找互質數e
        while True:
        #for i in range(2**64, fn-1):
            i = random.randrange(2**64, fn-1)
            if computeGCD(i, fn) == 1:
                e = i
                break
        # print(e)

        d = ext_euclid(e, fn)
        # print(d)
        enc = encryption("SHE", e, N)
        dec = decryption(enc, d, N)
        if dec=="SHE":
            flag = 1
        else:
            flag = 0
        print(flag)
    return [[e,N],[d,N]]


# 建立public and private key
#publicKey = [e, N]
#privateKey = [d, N]
