from django.shortcuts import render
from store.models import Product

def say_hello(request):

    queryset = Product.objects.filter(last_update__year=2021)

    context = {
        'products': queryset,
    }
    return render(request, 'hello.html', context)
