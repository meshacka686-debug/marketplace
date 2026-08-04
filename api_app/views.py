from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Product
from .serializers import ProductSerializer


@api_view(["GET"])
def api_home(request):
    return Response({
        "message": "Marketplace API is working"
    })


@api_view(["GET"])
def products(request):
    products = Product.objects.filter(available=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)