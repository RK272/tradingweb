#from django.urls import pathlib

from . import views

from django.contrib import admin
from django.urls import path

from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="expenses"),
    path('add-expense', views.add_expense, name="add-expenses" )]

