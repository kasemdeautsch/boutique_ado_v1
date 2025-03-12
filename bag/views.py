from django.shortcuts import render, redirect

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

    quantity = int(request.POST.get('quantity'))
    #print('request.POST: ', request.POST)
    redirect_url = request.POST.get('redirect_url')
    size = 0

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

    request.session['bag'] = bag
    #print(request.session['bag'])
    #print('last bag--->>>', bag)
    #print('request.session--->>>', request.session)
    return redirect(redirect_url)