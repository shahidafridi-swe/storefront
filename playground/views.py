from django.shortcuts import render
from store.models import Product

def say_hello(request):

    # queryset = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    queryset = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20) #same of above

    context = {
        'products': queryset,
    }
    return render(request, 'hello.html', context)
