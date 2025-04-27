from django.http import HttpResponse
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def predict(request):
    '''
    javascriptの使い方の実験
    '''
    datas = json.loads(request.body)

    print("requ",request.body)
    print("requ",datas)
    print("aaaa")

    res = {"data1":"data"}

    return JsonResponse(res)
