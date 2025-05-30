from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm
from bag.contexts import bag_contents
from products.models import Product
from .models import Order, OrderLineItem
from profiles.models import UserProfile
from profiles.forms import UserProfileForm

import stripe
import json
# Create your views here.


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    print('checkout started>>>>')
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    print('request.POST>> ', request.POST)
    print('request.session>> ', request.session)
    #print('request.session["save-info"]>> ', request.session['save-info'])

    tt = request.session['save-info'] = 'save-info' in request.POST
    print("request.session['save-info'] = 'save-info' in request.POST>>: ", tt)
    if request.method == "POST":
        print('request.POST received>>')
        
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county':  request.POST['county'],
        }
        order_form = OrderForm(form_data)
        #print('order_form>> ', order_form)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()
            print('order->> ', order)
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        #product = Product.objects.get(id=item_id)
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                product_size=size,
                                quantity=quantity,
                            )
                            order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )

                    order.delete()
                    return redirect(reverse('view_bag'))
        
            print('request.POST2>> ', request.POST)
            print('request.session2>> ', request.session)
            print('request.session["save-info"] before>> ', request.session['save-info'])

            request.session['save_info'] = 'save-info' in request.POST

            print('request.session["save-info"] after>> ', request.session['save-info'])
            
            return redirect(reverse('checkout_success', args=[order.order_number]))
            #return redirect(reverse('checkout'))
        else:
            messages.error(request, "There was an error with your form. \
                           Please check your informations!")
    else:

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
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country':  profile.default_country,
                    'postcode':  profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1':  profile.default_street_address1,
                    'street_address2':  profile.default_street_address2,
                    'county':  profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
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

def checkout_success(request, order_number):
    """
    Handle success checkout
    """
    #save_info = request.session.get('save_info')
    save_info = request.session.get('save_info')

    print("request.session.get('save_info')-->>> ", request.session.get('save_info'), save_info)

    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach user's profile to the order
        order.user_profile = profile
        order.save()
        print('Order Saved!!!')
        # save the user's info
        if save_info:
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_county': order.county,
                'default_postcode': order.postcode,
                'default_town_or_city': order.town_or_city,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_country': order.county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()
                print('Infos saved!!')

    messages.success(request, f'Order successfully processed! \
                     Your order number is {order_number}, A confirmation \
                        Email will be sent to {order.email}')
    
    if 'bag' in request.session:
        del request.session['bag']
    template = "checkout/checkout_success.html"
    context = {
        'order': order
    }
    return render(request, template, context)