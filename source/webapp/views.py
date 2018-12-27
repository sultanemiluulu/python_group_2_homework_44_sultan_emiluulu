from django.views.generic import ListView, DetailView, CreateView, UpdateView, View, DeleteView
from django.urls import reverse, reverse_lazy
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


class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_detail.html'


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'order_update.html'
    form_class = OrderForm

    def get_success_url(self):
        return reverse('order_detail', kwargs={'pk': self.object.pk})


def order_deliver_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.status == 'new':
        order.status = 'preparing'
    elif order.status == 'preparing':
        order.status = 'on_way'
    elif order.status == 'on_way':
        order.status = 'delivered'
    order.save()
    return redirect('order_detail', pk)


def order_reject_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.status in ('delivered', 'on_way'):
        return redirect('error.html')
    else:
        order.status = 'canceled'
        order.save()

    return redirect('order_detail', pk)


class OrderCreateView(CreateView):
    model = Order
    template_name = 'order_create.html'
    form_class = OrderForm

    def get_success_url(self):
        return reverse('order_detail', kwargs={'pk': self.object.pk})


class OrderFoodCreateView(CreateView):
    model = OrderFood
    form_class = OrderFoodForm
    template_name = 'order_food_create.html'

    def get_success_url(self):
        return reverse_lazy('order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        form.instance.order = Order.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)


class OrderFoodUpdateView(UpdateView):
    model = OrderFood
    form_class = OrderFoodForm
    template_name = 'order_food_update.html'

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.order.pk})


class OrderFoodDeleteView(DeleteView):
    model = OrderFood
    form_class = OrderFoodForm
    template_name = 'order_food_delete.html'

    def get_success_url(self):
        return reverse('order_detail', kwargs={'pk': self.object.order.pk})

