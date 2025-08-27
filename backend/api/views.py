from django.http import JsonResponse
import json
from products.models import Product 
from django.forms.models import model_to_dict

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
    data  = dict(request.GET)
    data['headers'] = dict(request.headers)
    data['content_type'] = request.content_type 
    print(data)
    return JsonResponse(data, status=200)

# In JsonResponse we pass a Python dict or list as data. It automatically serializes it into JSON. Internally it uses json.dumps() for you.
# It also sets the HTTP header Content-Type: application/json.
# Python dict ➝ JSON string → json.dumps()
# JSON string ➝ Python dict → json.loads()



def api_home(request, *args, **kwargs): 
    model_data = Product.objects.all().order_by("?").first()
    data  = {} 
    if model_data : 
        data = model_to_dict(model_data, fields=['id', 'title', 'content', 'price'])
    return JsonResponse(data)

