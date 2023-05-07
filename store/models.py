from django.db import models


class Promotion(models.Model):
    decription = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')

    # change the title name in administration
    def __str__(self):
        return self.title

    # for ordering in administration
    class Meta:
        ordering = ['title']


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)

    # change the title name in administration
    def __str__(self):
        return self.title

    # for ordering in administration
    class Meta:
        ordering = ['title']


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    birth_date = models.DateField(blank=True, null=True)
    BRONZE = "B"
    SILVER = "S"
    GOLD = "G"
    MEMBERSHIP_CHOICES = [
        (BRONZE, "Bronze"),
        (SILVER, "Silver"),
        (GOLD, "Gold"),
    ]
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=BRONZE)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Order(models.Model):
    placed_at = models.DateField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    PENDING = "B"
    COMPLETE = "S"
    FAILED = "G"
    PAYMENT_STATUS_CHOICE = [
        (PENDING, "Pending"),
        (COMPLETE, "Complete"),
        (FAILED, "Failed"),
    ]
    PAYMENT_STATUS = models.CharField(
        max_length=1,
        choices=PAYMENT_STATUS_CHOICE,
        default=PENDING,
    )


class OrderItem(models.Model):
    # orderitem_set
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
