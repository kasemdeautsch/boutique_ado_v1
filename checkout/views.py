from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm
from bag.contexts import bag_contents

import stripe
# Create your views here.


def checkout(request):

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    bag = request.session.get('bag', {})

    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    current_bag = bag_contents(request)
    #total= grand_total
    total = current_bag['grand_total']
    stripe_total = round(total * 100)
    #total = current_bag.get('grand_total')
    #print('current_bag------>', current_bag, type(current_bag))
    print('grand_total------>XXX', total)
    print('stripe_total------>XXX', stripe_total)

    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,

    )
    print('STRIPE_PUBLIC_KEY------', stripe_public_key)
    print('STRIPE_SECRET_KEY------', stripe_secret_key)
    print("intent---->", intent, type(intent))
    order_form = OrderForm()
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing, \
        did you forget to set it in your Enviroment?')
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_publik_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)
