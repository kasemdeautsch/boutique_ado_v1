from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    sub_total = 0
    bag = request.session.get('bag', {})
    #print('----------------')
    #print('initial_bag', bag)
    #print('----------------')

    for item_id, item_data in bag.items():
        #print('now-----')
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            sub_total = item_data * product.price
            #print('product_count-->>>', product_count)
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product':  product,
                'sub_total': sub_total,
            })
            #print('----------------')
            #print('bag_items_1', bag_items)
            #print('----------------')

        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['items_by_size'].items():
                #print('----------------')
                #print("item_data['items_by_size'].items()", item_data['items_by_size'].items())
                #print('----------------')
                total += quantity * product.price
                product_count += quantity
                sub_total = quantity * product.price
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'size': size,
                    'sub_total': sub_total,
                    'product':  product,
                    'sub_total': sub_total,
            })
                #print('----------------')
                #print('bag_items_3', bag_items)
                #print('----------------')

    if total < settings.FREE_DELIVERY_THRESHOLD:
        #delivery = total * Decimal(settings.STANDARD_DELIVERY_PRECENTAGE/100)
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
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
        'mex': 'Kass',
    }

    return context
