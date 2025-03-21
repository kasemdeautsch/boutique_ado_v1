from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm
# Create your views here.


def checkout(request):

    bag = request.session.get('bag', {})

    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key':'pk_test_51R4juVD3PlWdN0L5wO4WKiycMKOcUzNVVpFwU82D0CXeCZnDcJXqZbeBEzBpFDdqAWL9A1F5X6JntPclMeli4lpY00z00sXjJu',
        'client_secret': 'test client secret'
    }

    return render(request, template, context)
