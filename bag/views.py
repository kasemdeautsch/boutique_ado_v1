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
    print('request.POST: ', request.POST)
    redirect_url = request.POST.get('redirect_url')

    bag = request.session.get('bag', {})
    print('bag.keys():', bag.keys())
    print('list(bag.keys()):', list(bag.keys()))
    
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    request.session['bag'] = bag
    print(request.session['bag'])
    print(bag)
    return redirect(redirect_url)