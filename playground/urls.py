from django.urls import path
from . import views


# URL Configerations
urlpatterns = [
    path('hello/',views.say_hello)
]
