from django.views.generic import ListView, DetailView, CreateView, UpdateView, View, DeleteView
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from webapp.models import Food, Order, OrderFood, Employee
from webapp.forms import FoodForm, OrderForm, OrderFoodForm


class FoodListView(ListView):
    model = Food
    template_name = 'food_list.html'


class EmployeeListView(ListView):
    model = Employee
    template_name = 'employee_list.html'


class OrderListView(ListView):
    model = Order
    template_name = 'order_list.html'

