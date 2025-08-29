from django.http import JsonResponse
import json
from products.models import Product 
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.serializers import ProductSerializer

def first_api_home(request, *args, **kwargs):
    # request -> HttpRequest object -> Django
    body = request.body  # JSON data string
    print(request.GET) #url query params

    data  = {}
    try :
        data = json.loads(body)  # convert JSON string to Python dict
    except :
        pass
    print(data) # {'query': 'hello world'}
    data  = dict(request.data)
    data['headers'] = dict(request.headers)
    data['content_type'] = request.content_type 
    print(data)
    return JsonResponse(data, status=200)

# In JsonResponse we pass a Python dict or list as data. It automatically serializes it into JSON. Internally it uses json.dumps() for you.
# It also sets the HTTP header Content-Type: application/json.
# Python dict ➝ JSON string → json.dumps()
# JSON string ➝ Python dict → json.loads()



def second_api_home(request, *args, **kwargs): 
    if request.method == "POST" : 
        return JsonResponse({"message": "POST request not allowed."}, status=405)
    model_data = Product.objects.all().order_by("?").first()
    data  = {} 
    if model_data : 
        data = model_to_dict(model_data, fields=['id', 'title', 'content', 'price'])
        data['sale_price'] = model_data.sale_price 
    return JsonResponse(data)

@api_view(['GET','POST']) #now this will do the basic method checking for us
def api_home(request, *args, **kwargs):
    """Django REST Framework"""
    if request.method == "POST" : 
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # instance = serializer.save()
            print(serializer.data)
            return Response(serializer.data)
    instance = Product.objects.all().order_by("?").first()
    data = {}
    if instance :
        data = ProductSerializer(instance).data
    return Response(data)

