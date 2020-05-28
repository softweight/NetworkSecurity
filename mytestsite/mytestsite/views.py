from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import qrcode as qr
from PIL import Image

def encrypt(request):
    return render(request,'Encrypt.html')

def testk():
    k = 123
    return k

def testc():
    c=456
    return c

def decrypt(request,k,c):
    print("k = "+k+"   "+"c = "+c)
    return render(request, 'Decrypt.html',{'c_text':c,'e_k':k})

@csrf_exempt
def decryptK(request):
    if request.method == 'POST':
        result=[]
        result.append({'ans':"wow"})
        return JsonResponse(result,safe=False, json_dumps_params={'ensure_ascii': False})
@csrf_exempt
def decryptC(request):
    if request.method == 'POST':
        result=[]
        result.append({'ans':"yeah"})
        return JsonResponse(result,safe=False, json_dumps_params={'ensure_ascii': False})

@csrf_exempt
def qrcode_making(request):
    if request.method == 'POST':
        k=testk()
        c=testc()
        img = qr.make("http://192.168.43.161:8080/k="+str(k)+"c="+str(c))  # 輸入內容
        img.save("C:/Users/sheep/OneDrive/桌面/NS/NetworkSecurity/mytestsite/static/images/QRcode.png")
        return JsonResponse({'result':True})