from django.forms import ModelForm,DateInput
from .models import *

class ProductsForm(ModelForm):
    class Meta:
        model = Products
        fields = '__all__'

class SupplierOrderForm(ModelForm):
    class Meta:
        model = SupplierOrderDetails
        fields = ['sup_name', 'Date', 'product_name', 'size', 'pcs', 'Pcs_cost']
        widgets = {
            'Date': DateInput(attrs={'type': 'date'})
        }

class PaymentForm(ModelForm):
    class Meta:
        model = PaymentDetails
        fields = '__all__'
        widgets = {
            'Date': DateInput(attrs={'type': 'date'})
        }

class CustomerOrderForm(ModelForm):
    class Meta:
        model = CustOrder
        fields = ['Supplier_name','Date','Product_name','size','pcs','Sale_cost']
        widgets = {
            'Date': DateInput(attrs={'type': 'date'})
        }