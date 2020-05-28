import base64
import hashlib
import random
import string

modular = 251
mod_inv = 157
W_8 =  [1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, modular-1, modular-1, modular-1, modular-1,
        1, 1, modular-1, modular-1, modular-1, modular-1, 1, 1,
        1, 1, modular-1, modular-1, 1, 1, modular-1, modular-1,
        1, modular-1, modular-1, 1, 1, modular-1, modular-1, 1,
        1, modular-1, modular-1, 1, modular-1, 1, 1, modular-1,
        1, modular-1, 1, modular-1, modular-1, 1, modular-1, 1,
        1, modular-1, 1, modular-1, 1, modular-1, 1, modular-1]


def walsh_transform(ipt):
    opt = bytearray()
    for m in range(8):
        round_val = 0
        for n in range(8):
            round_val += (ipt[n] * W_8[m*8+n]) % modular
        round_val %= modular
        opt.append(round_val)

    return opt


def in_walsh_transform(ipt):
    opt = bytearray()
    for m in range(8):
        round_val = 0
        for n in range(8):
            round_val += (ipt[n] * W_8[m*8+n]) % modular
        round_val = (round_val * mod_inv) % modular
        opt.append(round_val)
    return opt

<<<<<<< HEAD

def tree_encryption(x):    #inorder -> preorder
=======
def tree_encryption(x):
>>>>>>> b4424a0ee4893cb0879734c751ab8ef37108ae12

    s_box = [3, 2, 4, 1, 6, 5, 7, 0]

    y = bytearray([x[s_box[i]] for i in range(8)])

    return y
    
def tree_decryption(x):    #preorder -> inorder

    s_box = [7, 3, 1, 0, 2, 5, 4, 6]

    y = bytearray([x[s_box[i]] for i in range(8)])

    return y

def block_encryption(m, k):
    for round_k in k:
        # print("=====begin round=====")
        # print("round key:", end='')
        # print(round_k)
        # print("original m:", end='')
        # print(m)
        m = walsh_transform(m)
        # print("after walsh:", end='')
        # print(m)
        m = bytearray([(m[i] + round_k[i]) % modular for i in range(8)])    #xor

        m = tree_encryption(m)
        # print("after xor:", end='')
        # print(m)
        # print("=====end round=====")
    return m


def block_decryption(m, k):
    for round_k in k:
        # print("=====begin round=====")
        # print("round key:", end='')
        # print(round_k)
        # print("original m:", end='')
        # print(m)
        m = tree_decryption(m)
        m = bytearray([(m[i] - round_k[i]) % modular for i in range(8)])    #xor
        # print("after xor:", end='')
        # print(m)
        m = in_walsh_transform(m)
        # print("after inv-walsh:", end='')
        # print(m)
        # print("=====end round=====")
    return m


def encryption(M, K):
    opt = bytearray(b"")
    M = bytearray(M.encode("UTF-8"))

    while len(M) % 8 != 0:  # padding
        M.append(0x20)

    internal_key = hashlib.sha256()
    K = K.encode("UTF-8")
    internal_key.update(K)
    round_k = internal_key.digest()

    round_k = [i % modular for i in round_k]

    round_k = [round_k[i*8:(i+1)*8] for i in range(4)]

    # print(round_k)

    for i in range(len(M)//8):
        block_p = M[i*8:(i+1)*8]  # 8個一單位
        # print("===begin block=====")
        # print("origin block: ", end='')
        # print(block_p)
        encrypted_block = block_encryption(block_p, round_k)
        # print("encrypted block: ", end='')
        # print(encrypted_block)
        # print("===end block=====")
        opt.extend(encrypted_block)

    opt = base64.b64encode(opt).decode("UTF-8")

    return opt


def decryption(C, K):
    opt = bytearray(b"")
    #M = bytearray(M.encode("UTF-8"))

    C = C.encode("UTF-8")
    C = base64.b64decode(C)

    # while len(C) % 8 != 0:  # padding
    #    C.append(0)

    internal_key = hashlib.sha256()
    K = K.encode("UTF-8")
    internal_key.update(K)
    round_k = internal_key.digest()

    round_k = [i % modular for i in round_k]

    round_k = [round_k[i*8:(i+1)*8] for i in range(3, -1, -1)]

    # print(round_k)

    for i in range(len(C)//8):
        block_p = C[i*8:(i+1)*8]  # 8個一單位
        # print("===begin block=====")
        # print("origin block: ", end='')
        # print(block_p)
        decrypted_block = block_decryption(block_p, round_k)
        # print("decrypted block: ", end='')
        # print(decrypted_block)
        # print("===end block=====")
        opt.extend(decrypted_block)
    # print(opt)

    opt = opt.decode("UTF-8")
    opt = opt.strip()
    return opt


def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


##################################### main ######################################################


# test = b'01234567'
# s_t = tree_encryption(test)
# print(s_t)
# d_t = tree_decryption(s_t)
# print(d_t)

# test = b'\x9a)\xcdJ\xb6\x9a.\xd5'
# w_t = walsh_transform(test)
# i_t = in_walsh_transform(w_t)
# print(i_t)


for _ in range(1000):
    x = randomString(random.randrange(1, 100))
    key = randomString(random.randrange(1, 100))
    y = encryption(x, key)
    decrypted = decryption(y, key)
    # print("M : ", x)
    # print("C : ", y)
    # print("D(C): ", decrypted)
    # decrypted = decrypted.strip()
    if x != decrypted : print(x, "!=" , decrypted)
    # assert(x == decrypted, "{}!={}".format(x, decrypted))
# print(type(decryption(y,key)))


# qrcode_making(k,c)
# im = Image.open('QR code.png')
# im.show()
