from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import qrcode as qr
from PIL import Image
import base64
import hashlib
import random
import string
from . import rsa
import os

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

#QR code的C跟K
forQR=[0]*2
private=[]

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

def tree_encryption(x):    #inorder -> preorder

    s_box = [7, 3, 1, 0, 2, 5, 4, 6]

    y = bytearray([x[s_box[i]] for i in range(8)])

    return y
    
def tree_decryption(x):    #preorder -> inorder

    s_box = [3, 2, 4, 1, 6, 5, 7, 0]

    y = bytearray([x[s_box[i]] for i in range(8)])

    return y

def s_box(x):

    _s_box = [107, 53, 242, 115, 3, 248, 236, 149, 38, 191, 221, 80, 164, 152, 240, 146, 147, 184, 135, 144, 1, 202, 28, 186, 130, 69, 90, 82, 114, 207, 133, 185, 168, 143, 40, 19, 208, 20, 44, 131, 181, 160, 96, 74, 198, 230, 102, 199, 241, 29, 222, 13, 177, 209, 137, 12, 204, 94, 225, 124, 170, 100, 58, 215, 163, 108, 37, 224, 121, 91, 173, 212, 233, 76, 99, 6, 93, 189, 113, 213, 234, 218, 55, 117, 157, 45, 162, 223, 17, 103, 71, 125, 140, 151, 14, 142, 159, 180, 97, 27, 8, 148, 134, 158, 106, 206, 214, 9, 161, 33, 77, 105, 87, 95, 235, 232, 228, 156, 138, 243, 79, 84, 227, 129, 10, 193, 195, 15, 122, 24, 34, 249, 245, 36, 126, 188, 219, 57, 11, 211, 25, 21, 109, 59, 226, 246, 41, 190, 200, 244, 83, 127, 104, 18, 56, 23, 155, 65, 250, 72, 46, 172, 128, 239, 210, 22, 139, 7, 169, 5, 39, 116, 73, 194, 187, 145, 171, 110, 42, 220, 112, 182, 150, 154, 98, 86, 64, 101, 88, 205, 75, 132, 92, 2, 120, 62, 153, 4, 81, 67, 196, 217, 231, 178, 78, 54, 52, 174, 85, 0, 50, 68, 89, 176, 167, 43, 238, 32, 70, 203, 229, 216, 179, 66, 51, 16, 183, 118, 31, 26, 201, 123, 111, 141, 237, 166, 30, 49, 119, 247, 192, 197, 47, 136, 48, 60, 63, 61, 175, 165, 35]

    y = bytearray()
    for i in x:
        y.append(_s_box[i])

    return y

def inv_s_box(x):

    _inv_s_box = [209, 20, 193, 4, 197, 169, 75, 167, 100, 107, 124, 138, 55, 51, 94, 127, 225, 88, 153, 35, 37, 141, 165, 155, 129, 140, 229, 99, 22, 49, 236, 228, 217, 109, 130, 250, 133, 66, 8, 170, 34, 146, 178, 215, 38, 85, 160, 242, 244, 237, 210, 224, 206, 1, 205, 82, 154, 137, 62, 143, 245, 247, 195, 246, 186, 157, 223, 199, 211, 25, 218, 90, 159, 172, 43, 190, 73, 110, 204, 120, 11, 198, 27, 150, 121, 208, 185, 112, 188, 212, 26, 69, 192, 76, 57, 113, 42, 98, 184, 74, 61, 187, 46, 89, 152, 111, 104, 0, 65, 142, 177, 232, 180, 78, 28, 3, 171, 83, 227, 238, 194, 68, 128, 231, 59, 91, 134, 151, 162, 123, 24, 39, 191, 30, 102, 18, 243, 54, 118, 166, 92, 233, 95, 33, 19, 175, 15, 16, 101, 7, 182, 93, 13, 196, 183, 156, 117, 84, 103, 96, 41, 108, 86, 64, 12, 249, 235, 214, 32, 168, 60, 176, 161, 70, 207, 248, 213, 52, 203, 222, 97, 40, 181, 226, 17, 31, 23, 174, 135, 77, 147, 9, 240, 125, 173, 126, 200, 241, 44, 47, 148, 230, 21, 219, 56, 189, 105, 29, 36, 53, 164, 139, 71, 79, 106, 63, 221, 201, 81, 136, 179, 10, 50, 87, 67, 58, 144, 122, 116, 220, 45, 202, 115, 72, 80, 114, 6, 234, 216, 163, 14, 48, 2, 119, 149, 132, 145, 239, 5, 131, 158]
    
    y = bytearray()
    for i in x:
        y.append(_inv_s_box[i])

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

        m = s_box(m)
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
        m = inv_s_box(m)

        m = tree_decryption(m)
        m = bytearray([(m[i] - round_k[i]) % modular for i in range(8)])    #xor
        # print("after xor:", end='')
        # print(m)
        m = in_walsh_transform(m)
        # print("after inv-walsh:", end='')
        # print(m)
        # print("=====end round=====")
    return m


def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def encrypt(request):
    return render(request,'Encrypt.html')

def testk():
    k = 123
    return k

def testc():
    c=456
    return c

def decrypt(request,c,k):
    print("c = "+c+"   "+"k = "+k)
    return render(request, 'Decrypt.html',{'c_text':c,'e_k':k})


@csrf_exempt
def decryptC(request):
    if request.method == 'POST':
        opt = bytearray(b"")
        #M = bytearray(M.encode("UTF-8"))
        C = forQR[0]
        K = rsa.decryption(forQR[1],private[0],private[1])
        print("I am K : ")
        print(K)
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
        result=[]
        result.append({'ans':opt})
        return JsonResponse(result,safe=False, json_dumps_params={'ensure_ascii': False})

@csrf_exempt
def qrcode_making(request):
    if request.method == 'POST':
        k=forQR[1]
        c=forQR[0]
        img = qr.make("http://192.168.43.161:8080/c"+str(c)+"k"+str(k))  # 輸入內容
        image_path = os.path.abspath("static/images/QRcode.png")
        img.save(image_path)
        return JsonResponse({'result':True})

@csrf_exempt
def encryption(request):
    if request.method == 'POST':
        M = request.POST['plaintext']
        K = request.POST['key']
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
        forQR[0]=opt
        result = []
        result.append({'ans':opt})
        return JsonResponse(result,safe=False, json_dumps_params={'ensure_ascii': False})

@csrf_exempt
def encryptionK(request):
    if request.method == 'POST':
        #RSA的密文[0]、private key [1][0]d [1][1]N
        K = request.POST['key']
        enc = rsa.encryption(K)
        forQR[1]=enc
        priv = rsa.gen_key()
        private.extend([priv[0],priv[1]])
        result = []
        result.append({'ans':enc})
        return JsonResponse(result,safe=False, json_dumps_params={'ensure_ascii': False})

