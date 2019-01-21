from django.urls import path
from webapp.views import FoodListView, OrderListView, \
    FoodDetailView, FoodDeleteView, FoodUpdateView, FoodCreateView, OrderCreateView,\
    OrderDetailView, OrderUpdateView, OrderFoodDeleteView,\
    order_deliver_view, order_reject_view,\
    OrderFoodAjaxCreateView, OrderFoodAjaxUpdateView


app_name = 'webapp'

urlpatterns = [
    path('', FoodListView.as_view(), name='food_list'),
    path('food/<int:pk>', FoodDetailView.as_view(), name='food_detail'),
    path('food/<int:pk>/delete', FoodDeleteView.as_view(), name='food_delete'),
    path('food/<int:pk>/update', FoodUpdateView.as_view(), name='food_update'),
    path('food/create', FoodCreateView.as_view(), name='food_create'),
    path('order_list', OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
    path('order/create', OrderCreateView.as_view(), name='order_create'),
    path('order/<int:pk>/update', OrderUpdateView.as_view(), name='order_update'),
    # path('order/<int:pk>/order_food_create', OrderFoodCreateView.as_view(), name='order_food_create'),
    # path('order/<int:pk>/order_food_update', OrderFoodUpdateView.as_view(), name='order_food_update'),
    # path('order/<int:pk>/order_food_delete', OrderFoodDeleteView.as_view(), name='order_food_delete'),
    path('order/<int:pk>/order_food_delete', OrderFoodDeleteView.as_view(), name='order_food_delete'),
    path('order/<int:pk>/status', order_deliver_view, name='order_status'),
    path('order/<int:pk>/reject', order_reject_view, name='order_reject'),
    path('order/<int:pk>/food/create', OrderFoodAjaxCreateView.as_view(), name='order_food_create'),
    path('order_food/<int:pk>/update', OrderFoodAjaxUpdateView.as_view(), name='order_food_update'),
]
