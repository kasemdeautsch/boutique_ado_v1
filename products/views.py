from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from products.models import Product,Category
# Create your views here.


def all_products(request):
    """
    A view to show all products, including search and queries
    """
    products = Product.objects.all()
    query = None
    categories = None
    #print(query)
    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories= Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, 'You did not enter any search criteria')
                return redirect(reverse('products'))
            queries= Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'serch_term': query,
        'current_categories': categories,
    }

    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """
    A view to show indivisual product details.
    """
    product = get_object_or_404(Product, pk=product_id)

    context = {
        "product": product,
    }

    return render(request, "products/product_detail.html", context)

