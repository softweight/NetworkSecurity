from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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