from django.shortcuts import render
from store.models import Product

def say_hello(request):

    queryset = Product.objects.filter(unit_price__range=(20,30))

    context = {
        'products': queryset,
    }
    return render(request, 'hello.html', context)
