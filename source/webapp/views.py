from django.views.generic import ListView, DetailView, CreateView, UpdateView, View, DeleteView
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from webapp.models import Food, Order, OrderFood, Employee
from webapp.forms import FoodForm, OrderForm, OrderFoodForm


class EmployeeListView(ListView):
    model = Employee
    template_name = 'employee_list.html'

