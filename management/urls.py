from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard,name='home'),
    path('cust_home',views.dashboard,name='cust_home'),
    path('suppliers/<str:pk>/',views.suppliers,name='supp_page'),
    path('Add_products/<str:pk>/',views.new_product,name='newproduct_page'),
    path('pay_det/<str:idd>/',views.Payment_details,name='pay_page'),
    path('ord_list/<str:idd>/',views.order_details,name='ord_list_page'),
    path('supp_ord/<str:pk>/',views.supp_order,name='supp_order_page'),
    path('update_ord/<str:pk>/',views.update_order,name='update_order_page'),
    path('order_delete/<str:pk>/',views.delete_order,name='delete_order_page'),
    path('payment_list/<str:pk>/',views.payment_list,name='payment_order_page'),
    path('payment_update/<str:pk>/',views.update_payment,name='payment_update_page'),
    path('payment_delete/<str:pk>/',views.deletepay,name='payment_delete_page'),
    path('customer_page/<str:pk>/',views.sell_details,name='cust_page'),
    path('customer_order/<str:pk>/',views.sell_order,name='cust_order_page'),
]



