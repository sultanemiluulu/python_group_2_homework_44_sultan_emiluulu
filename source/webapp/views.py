from django.views.generic import ListView, DetailView, CreateView, UpdateView, View, DeleteView
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from webapp.models import Food, Order, OrderFood, Employee
from webapp.forms import FoodForm, OrderForm, OrderFoodForm


class FoodListView(ListView):
    model = Food
    template_name = 'food_list.html'


class FoodDetailView(DetailView):
    model = Food
    template_name = 'food_detail.html'


class FoodCreateView(CreateView):
    model = Food
    template_name = 'food_create.html'
    form_class = FoodForm

    def get_success_url(self):
        return reverse('food_detail', kwargs={'pk': self.object.pk})


class FoodUpdateView(UpdateView):
    model = Food
    template_name = 'food_update.html'
    form_class = FoodForm

    def get_success_url(self):
        return reverse('food_detail', kwargs={'pk': self.object.pk})


class FoodDeleteView(DeleteView):
    model = Food
    template_name = 'food_delete.html'

    def get_success_url(self):
        return reverse('food_list')


class EmployeeListView(ListView):
    model = Employee
    template_name = 'employee_list.html'


class OrderListView(ListView):
    model = Order
    template_name = 'order_list.html'

