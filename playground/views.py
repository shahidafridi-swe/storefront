from django.shortcuts import render
from django.db.models import Q, F
from store.models import Product


def say_hello(request):

    # queryset = Product.objects.all()
    queryset = Product.objects.select_related('collection').all()

    context = {
        'products': queryset,
    }
    return render(request, 'hello.html', context)
