from django.shortcuts import render
from products.models import Product
# Create your views here.
def all_products(request):
    """
    A view to show all products, including search and queries
    """
    products = Product.objects.all()
    context = {
        "products":products,
    }
    return render(request, "products/products.html", context)