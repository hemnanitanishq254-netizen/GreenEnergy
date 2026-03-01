from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('order/create/<int:listing_id>/', views.create_order, name='create_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/payment/', views.payment, name='payment'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('history/', views.transaction_history, name='transaction_history'),
]