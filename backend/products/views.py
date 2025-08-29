from rest_framework import generics, mixins
from .models import Product
from .serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'  #By default, DRF assumes you want to look up objects using the primary key (pk).
    # lookup_url_kwarg → the URL parameter name you want to capture.

#class ProductsListAPIView(generics.ListAPIView):
#    queryset = Product.objects.all() #[Product(id=1, title="iPhone 15 Pro"),  Product(id=2, title="Samsung Galaxy S23"),...]
#    serializer_class = ProductSerializer #[ {"id": 1, "title": "iPhone 15 Pro", "price": 1299}, {"id": 2, "title": "Samsung Galaxy S23", "price": 999} ]


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        #you can modify the data before saving it to the database.
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(content=content)


class ProductDestroyAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_destroy(self, instance):    
        #instance -> object that is going to be deleted
        super().perform_destroy(instance)   #call the parent class's perform_destroy method to actually delete the object.



class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
#When DRF gets to perform_update, it does already know the instance.
#So by the time perform_update() is called:
#The instance exists
#The serializer is bound to both that instance and the new input data.
#Validation has already run.
#Then why pass serializer instead of instance?

#Because DRF wants you to work with the serializer workflow, not the raw instance.
#Serializer knows how to merge the instance + validated data correctly.
#serializer.save() internally decides:
#If instance is present → call update(instance, validated_data)
#If not → call create(validated_data)

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title
            instance.save(update_fields=["content"])


class ProductMixinView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs) #detail view
        return self.list(request, *args, **kwargs) #list view

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(content=content)


@api_view(['GET', 'POST'])
def product_alt_view(request,pk=None, *args, **kwargs):
    method = request.method  
    if method == "GET":
        if pk is not None:
            #detail view
            #queryset = Product.objects.filter(id=pk)
            #if not queryset.exists():
            #    return Response({"detail": "Not found."}, status=404)
            #data = ProductSerializer(obj, many=False)
            obj = get_object_or_404(Product, id=pk)
            data = ProductSerializer(obj, many=False)
            return Response(data.data)
        #list view
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True)
        return Response(data.data)
    if method == "POST":
        #create an item
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data)
        return Response({"invalid": "not good data"}, status=400)