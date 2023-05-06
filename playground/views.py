from django.shortcuts import render
from django.db.models import Q
from store.models import Product


def say_hello(request):

    # queryset = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    # queryset = Product.objects.filter(inventory__lt=10).filter(
    #     unit_price__lt=20)  # same of above

    queryset = Product.objects.filter(
        Q(inventory__lt=10) & ~Q(unit_price__lt=20)) 

    context = {
        'products': queryset,
    }
    return render(request, 'hello.html', context)
