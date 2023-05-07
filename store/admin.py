from django.contrib import admin, messages
from django.db.models import Count
from django.db.models.query import QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse

from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
            ('>9', 'OK')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        elif self.value() == '<10':
            return queryset.filter(inventory__gt=9)


class PriceFilter(admin.SimpleListFilter):
    title = 'price'
    parameter_name = 'unit_price'

    def lookups(self, request, model_admin):
        return [
            ('1-10', '$ 1-10'),
            ('11-20', '$ 11-20'),
            ('21-50', '$ 21-50'),
            ('>50', '$ 50+'),
        ]
    
    def queryset(self, request, queryset: QuerySet):
        if self.value() == '1-10':
            return queryset.filter(unit_price__lte=10)
        elif self.value() == '11-20':
            return queryset.filter(unit_price__gt=10).filter(unit_price__lte=20)
        elif self.value() == '21-50':
            return queryset.filter(unit_price__gt=20).filter(unit_price__lte=50)
        elif self.value() == '>50':
            return queryset.filter(unit_price__gt=50)


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        # reverse('admin:app_model_page')
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection_id': str(collection.id)
            })
        )
        return format_html('<a href="{}"> {} </a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):

    #Forms
    # fields = ['title', 'slug']
    # exclude = ['title', 'slug']
    # readonly_fields = ['title', 'slug']
    autocomplete_fields = ['collection']
    prepopulated_fields ={
        'slug':['title']
    } 


    actions = ['clear_inventory']
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter, PriceFilter]
    list_per_page = 10

    list_select_related = ['collection']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request,queryset):
        updated_count = queryset.update(inventory = 0)
        self.message_user(
            request,
            f'{updated_count} product\'s inventory were successfully updated.',
            messages.ERROR
        )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders_count']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
  

    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        # reverse('admin:app_model_page')
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer_id': str(customer.id)
            })
        )
        return format_html('<a href="{}"> {} </a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    autocomplete_fields = ['customer']

