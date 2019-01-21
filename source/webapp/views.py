from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from webapp.models import Food, Order, OrderFood, Employee
from webapp.forms import FoodForm, OrderForm, OrderFoodForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class FoodListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Food
    template_name = 'food_list.html'
    permission_required = 'webapp.view_food'


class FoodDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Food
    template_name = 'food_detail.html'
    permission_required = 'webapp.view_food'


class FoodCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Food
    template_name = 'food_create.html'
    form_class = FoodForm
    permission_required = 'webapp.add_food'

    def get_success_url(self):
        return reverse('webapp:food_detail', kwargs={'pk': self.object.pk})


class FoodUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Food
    template_name = 'food_update.html'
    form_class = FoodForm
    permission_required = 'webapp.change_food'

    def get_success_url(self):
        return reverse('webapp:food_detail', kwargs={'pk': self.object.pk})


class FoodDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Food
    template_name = 'food_delete.html'
    success_url = reverse_lazy('webapp:food_list')
    permission_required = 'webapp.delete_food'


class OrderListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Order
    template_name = 'order_list.html'
    permission_required = 'webapp.view_order'


class OrderDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView, FormView):
    model = Order
    template_name = 'order_detail.html'
    permission_required = 'webapp.view_order'
    form_class = OrderFoodForm


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    template_name = 'order_update.html'
    form_class = OrderForm
    permission_required = 'webapp.change_order'

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.pk})


def order_deliver_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.user.has_perm('webapp.can_take_order'):
        user = request.user
        if not order.courier:
            order.courier = user
        else:
            return HttpResponseForbidden()
        if order.courier == user:
            if order.status == 'new':
                order.status = 'preparing'
            elif order.status == 'preparing':
                order.status = 'on_way'
            elif order.status == 'on_way':
                order.status = 'delivered'
            order.save()
            return redirect('webapp:order_detail', pk)
    else:
        return HttpResponseForbidden()


def order_reject_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.status in ('delivered', 'on_way'):
        return redirect('webapp:error.html')
    else:
        order.status = 'canceled'
        order.save()

    return redirect('webapp:order_detail', pk)


class OrderCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Order
    template_name = 'order_create.html'
    form_class = OrderForm
    permission_required = 'webapp.add_order'

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.operator = self.request.user
        return super().form_valid(form)


class OrderFoodAjaxCreateView(CreateView):
    model = OrderFood
    form_class = OrderFoodForm

    def form_valid(self, form):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        form.instance.order = order
        order_food = form.save()
        return JsonResponse({
            'food_name': order_food.food.name,
            'food_pk': order_food.food.pk,
            'amount': order_food.amount,
            'pk': order_food.pk,
            'edit_url': reverse('webapp:order_food_update', kwargs={'pk': order_food.pk}),
        })

    # обработка формы с ошибками
    # статус 422 - UnprocessableEntity, применяется,
    # когда запрос имеет корректный формат,
    # но неподходящие по смыслу данные (например, пустые).
    def form_invalid(self, form):
        return JsonResponse({
            'errors': form.errors
        }, status='422')


class OrderFoodAjaxUpdateView(UpdateView):
    model = OrderFood
    form_class = OrderFoodForm

    def form_valid(self, form):
        order_food = form.save()
        return JsonResponse({
            'food_name': order_food.food.name,
            'food_pk': order_food.food.pk,
            'amount': order_food.amount,
            'pk': order_food.pk
        })

    def form_invalid(self, form):
        return JsonResponse({
            'errors': form.errors
        }, status='422')


# class OrderFoodCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
#     model = OrderFood
#     form_class = OrderFoodForm
#     template_name = 'order_food_create.html'
#     permission_required = 'webapp.add_orderfood'
#
#     def get_success_url(self):
#         return reverse_lazy('webapp:order_list')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['order'] = Order.objects.get(pk=self.kwargs.get('pk'))
#         return context
#
#     def form_valid(self, form):
#         form.instance.order = Order.objects.get(pk=self.kwargs.get('pk'))
#         return super().form_valid(form)


# class OrderFoodUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
#     model = OrderFood
#     form_class = OrderFoodForm
#     template_name = 'order_food_update.html'
#     permission_required = 'webapp.change_orderfood'
#
#     def get_success_url(self):
#         return reverse('webapp:order_detail', kwargs={'pk': self.object.order.pk})


# class OrderFoodDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
#     model = OrderFood
#     form_class = OrderFoodForm
#     template_name = 'order_food_delete.html'
#     permission_required = 'webapp.delete_orderfood'
#
#     def get_object(self, queryset=None):
#         pass
#
#     def get_success_url(self):
#         return reverse('webapp:order_detail', kwargs={'pk': self.object.order.pk})

class OrderFoodDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = OrderFood
    permission_required = 'webapp.delete_orderfood'

    def delete(self, request, *args, **kwargs):
        orderfood = get_object_or_404(OrderFood, pk=self.kwargs.get('pk'))
        orderfood.delete()
        if orderfood:
            return JsonResponse({
                'orderfood_pk': orderfood.pk,
            })



