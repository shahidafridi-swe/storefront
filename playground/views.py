from django.shortcuts import render
from store.models import Product

def say_hello(request):

    queryset = Product.objects.filter(title__icontains='coffee')

    context = {
        'products': queryset,
    }
    return render(request, 'hello.html', context)
