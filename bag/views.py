from django.shortcuts import render, redirect, reverse, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages

from products.models import Product
# Create your views here.


def view_bag(request):
    """
    A view that renders the bag content page
    """
    print("about to render...")
    
    return render(
        request,
        "bag/bag.html"
    )


def add_to_bag(request, item_id):
    """
    Add a quantity of the specified product to the bag
    """
    product = Product.objects.get(pk=item_id)
    quantity = int(request.POST.get('quantity'))
    print('request.POST: ', request.POST)
    redirect_url = request.POST.get('redirect_url')
    size = None

    if 'product_size' in request.POST:
        size = request.POST['product_size']

    bag = request.session.get('bag', {})
    #print('request.session-->>: ', request.session)

    #print('bag0: ', bag)
    #print('bag.items0: ', bag.items())
    #print('bag.keys()0:', bag.keys())
    #print('list(bag.keys())0:', list(bag.keys()))
    

    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
               # print('------------------------')
                #print('bag1: ', bag)
                #print("bag[item_id]['items_by_size'].keys()1: ", bag[item_id]['items_by_size'].keys())
                #print('------------------------')
                
            else:
                bag[item_id]['items_by_size'][size] = quantity
               # print('------------------------')
                #print('bag2: ', bag)
                #print('------------------------')
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
            #print('------------------------')
            #print('bag3: ', bag)
            #print('bag[item_id]3: ', bag[item_id])
            #print('------------------------')
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag.')
            #messages.add_message(request, messages.SUCCESS, f'Added {product.name} to your bag.')
    request.session['bag'] = bag
    #messages.add_message(request, messages.SUCCESS, 'OKKKKK')
    
    #print(request.session['bag'])
    #print('last bag--->>>', bag)
    #print('request.session--->>>', request.session)
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """
    Adjust quantity of the specified product to the specified amount
    """

    quantity = int(request.POST.get('quantity'))
    
    print('request.POST: ', request.POST)
    
    size = None

    if 'product_size' in request.POST:
        size = request.POST['product_size']

    bag = request.session.get('bag', {})
    print('bag------>>: ', bag)
    print('request.session-->>: ', request.session)

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)

    else:
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)

    request.session['bag'] = bag
    #print(request.session['bag'])
    print('last bag--->>>', bag)
    #print('request.session--->>>', request.session)
    #return redirect(reverse('view_bag'))
    return HttpResponseRedirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """
    remove the item from shopping bag
    """

    print('request.POST: ', request.POST)
    
    try:
        size = None

        if 'product_size' in request.POST:
            size = request.POST['product_size']

        bag = request.session.get('bag', {})
        print('request.session-->>: ', request.session)

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
        else:
            bag.pop(item_id)

        request.session['bag'] = bag
        #print(request.session['bag'])
        print('last bag--->>>', bag)
        #print('request.session--->>>', request.session)
        return HttpResponse(status=200)
    except Exception as e:
        print('-------Error-------')
        return HttpResponse(status=500)