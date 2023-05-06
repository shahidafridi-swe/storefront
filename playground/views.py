from django.shortcuts import render
from django.db.models import Q, F
from store.models import Product, Order


def say_hello(request):

    # Get the last 5 orders with their customer and items (incl product)

    queryset = Order.objects.select_related('customer').prefetch_related(
        'orderitem_set__product').order_by('-placed_at')[:5]

    context = {
        'orders': list(queryset),
    }
    return render(request, 'hello.html', context)
