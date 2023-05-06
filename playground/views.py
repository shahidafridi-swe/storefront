from django.shortcuts import render
from django.db.models import Q, F
from store.models import Product


def say_hello(request):

    # select_related(1)
    # prefetch_related(n)
    queryset = Product.objects.prefetch_related(
        'promotions').select_related('collection').all()

    context = {
        'products': queryset,
    }
    return render(request, 'hello.html', context)
