import qrcode as qr
from PIL import Image

def qrcode_makeing():
    img = qr.make("https://ppt.cc/flanQx")
    img.save("QR code.png")

def encrypt():
    pass
    

W_8 = [ 1,1,1,1,1,1,1,1,
        1,1,1,1,250,250,250,250,
        1,1,250,250,250,250,1,1,
        1,1,250,250,1,1,250,250,
        1,250,1250,1,1,250,250,1,
        1,250,250,1,250,1,1,250,
        1,250,1,250,250,1,250,1,
        1,250,1,250,1,250,1,250]

def walsh_transform(ipt):
    opt = []
    for m in range(8):
        temp = 0
        for n in range(8):
            temp += ord(ipt[n]) * W_8[n*8+m]
        if temp>0 :
            temp %=251
        
        opt.append(temp)
    
    return opt


def in_walsh_transform(ipt):
    opt = ""
    for m in range(8):
        temp = 0
        for n in range(8):
            temp += ipt[n] * W_8[n*8+m]
        opt+=chr(int(temp/8))
    
    return opt

x= "hello world and G9J"
# y = groupping(x)
y = walsh_transform(x)
print(y)
print(in_walsh_transform(y))

# qrcode_makeing()
# im = Image.open('QR code.png')
# im.show()

