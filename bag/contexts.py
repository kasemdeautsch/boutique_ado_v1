from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0

    bag = request.session.get('bag', {})
    print('----------------')
    print('initial_bag', bag)
    print('----------------')

    for item_id, item_data in bag.items():
        #print('now-----')
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            #print('product_count-->>>', product_count)
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product':  product,
            })
            print('----------------')
            print('bag_items_1', bag_items)
            print('----------------')

        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['items_by_size'].items():
                print('----------------')
                print("item_data['items_by_size'].items()", item_data['items_by_size'].items())
                print('----------------')
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': item_data,
                    'product':  product,
                    'size': size
            })
                print('----------------')
                print('bag_items_3', bag_items)
                print('----------------')

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PRECENTAGE/100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
        'me':12,
    }

    return context