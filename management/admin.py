from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Supplier)
admin.site.register(Products)
admin.site.register(SupplierStockDetails)
admin.site.register(SupplierOrderDetails)
admin.site.register(PaymentDetails)
admin.site.register(CustOrder)