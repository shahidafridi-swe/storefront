from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)

    BRONZE = "B"
    SILVER = "S"
    GOLD = "G"
    MEMBERSHIP_CHOICES = [
        (BRONZE, "Bronze"),
        (SILVER, "Silver"),
        (GOLD, "Gold"),
    ]
    membership = models.CharField(
        max_length=1,
        choices=MEMBERSHIP_CHOICES,
        default=BRONZE,
    )


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    birth_date = models.DateField(blank=True, null=True)


class Order(models.Model):
    placed_at = models.DateField(auto_now_add=True)

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

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
    