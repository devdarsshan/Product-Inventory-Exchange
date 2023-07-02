from django.db import models
from django.contrib import messages

class Supplier(models.Model):
    Supplier_Name = models.CharField(max_length=255)
    Supplier_Email = models.EmailField(null=True, blank=True)
    Supplier_phonenumber = models.CharField(max_length=20,null=True, blank=True)

    def __str__(self):
        return self.Supplier_Name
    
class Customer(models.Model):
    Customer_Name = models.CharField(max_length=255)
    def __str__(self):
        return self.Supplier_Name

class Products(models.Model):
    Supplier_Name = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    Product_Name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.Product_Name

class SupplierStockDetails(models.Model):
    Supplier_Name = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    Product_name = models.ForeignKey(Products, on_delete=models.CASCADE)
    SIZE_CHOICES = (
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    )
    Size = models.CharField(max_length=3, choices=SIZE_CHOICES)
    Pcs = models.IntegerField(null=True, blank=True, default=0)
    Pcs_cost = models.IntegerField(null=True, blank=True, default=0)
    In_Stock = models.IntegerField(null=True, blank=True, default=0)
    Total_size_cost = models.IntegerField(null=True, blank=True, default=0)
    Total_sup_cost = models.IntegerField(null=True, blank=True, default=0)

    def calculate_total_size_cost(self):
        self.Total_size_cost = self.Pcs * self.Pcs_cost

    def calculate_total_sup_cost(self):
        supplier_stock = SupplierStockDetails.objects.filter(Supplier_Name=self.Supplier_Name)#, Product_name=self.Product_name)
        total_stk_cost = supplier_stock.aggregate(total_cost=models.Sum('Total_size_cost'))['total_cost'] or 0
        total_pay_cost = PaymentDetails.objects.filter(sup_name=self.Supplier_Name).aggregate(total=models.Sum('Amount_payed'))['total'] or 0
        total_sup_cost = total_stk_cost - total_pay_cost
        if total_sup_cost > 0:
            supplier_stock.update(Total_sup_cost=total_sup_cost)
        else:
            supplier_stock.update(Total_sup_cost=0)

    def save(self, *args, **kwargs):
        # self.In_Stock = self.Pcs
        self.calculate_total_size_cost()
        super(SupplierStockDetails, self).save(*args, **kwargs)
        self.calculate_total_sup_cost()

    def __str__(self):
        return f'{self.Supplier_Name} - {self.Product_name}'

# Supplier Order Details

class SupplierOrderDetails(models.Model):
    sup_name = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    Date = models.DateField()
    product_name = models.ForeignKey(Products, on_delete=models.CASCADE)
    size = models.CharField(max_length=3, choices=SupplierStockDetails.SIZE_CHOICES)
    pcs = models.IntegerField(null=True, blank=True, default=0)
    Pcs_cost = models.IntegerField(null=True, blank=True, default=0)
    total_cost = models.IntegerField(null=True, blank=True, default=0)

    def save(self, *args, **kwargs):
        if self.pk:
            # Existing order
            original_order = SupplierOrderDetails.objects.get(pk=self.pk)
            # Calculate the difference in pcs count
            pcs_diff = self.pcs - original_order.pcs

            self.total_cost = self.Pcs_cost * self.pcs

            supplier_stock = SupplierStockDetails.objects.filter(
                Supplier_Name=self.sup_name,
                Product_name=self.product_name,
                Size=self.size
            ).first()
            if supplier_stock:
                supplier_stock.Pcs += pcs_diff
                supplier_stock.Total_size_cost += self.Pcs_cost * pcs_diff
                supplier_stock.calculate_total_sup_cost()  # Call the method to update the Total_sup_cost
                supplier_stock.save()
        else:
            self.total_cost = self.Pcs_cost * self.pcs

            supplier_stock = SupplierStockDetails.objects.filter(Supplier_Name=self.sup_name, Product_name=self.product_name, Size=self.size).first()
            if supplier_stock:
                supplier_stock.In_Stock += self.pcs
                supplier_stock.Pcs += self.pcs
                supplier_stock.Total_size_cost += self.Pcs_cost * self.pcs
                supplier_stock.calculate_total_sup_cost()  # Call the method to update the Total_sup_cost
                supplier_stock.save()
            else:
                supplier_stock = SupplierStockDetails(
                    Supplier_Name=self.sup_name,
                    Product_name=self.product_name,
                    Size=self.size,
                    Pcs=self.pcs,
                    Pcs_cost=self.Pcs_cost,
                    In_Stock = self.pcs,
                    Total_size_cost=self.Pcs_cost * self.pcs                    
                )
                supplier_stock.save()

                # Calculate total_sup_cost for the new entry
                supplier_stock.calculate_total_sup_cost()

        super(SupplierOrderDetails, self).save(*args, **kwargs)


    def __str__(self):
        return f'{self.sup_name} - {self.product_name}'

# Supplier Payment Details

class PaymentDetails(models.Model):
    sup_name = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    Date = models.DateField()
    Amount_payed = models.DecimalField(max_digits=10, decimal_places=2)
    Comment = models.TextField()

    def save(self, *args, **kwargs):
        super(PaymentDetails, self).save(*args, **kwargs)
        supplier_stocks = SupplierStockDetails.objects.filter(Supplier_Name=self.sup_name)

        for supplier_stock in supplier_stocks:
            supplier_stock.calculate_total_sup_cost()
            supplier_stock.save()

        

    def __str__(self):
        return f'{self.sup_name} - {self.Amount_payed}'

class CustOrder(models.Model):
    Supplier_name = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    Date = models.DateField()
    Product_name = models.ForeignKey(Products, on_delete=models.CASCADE)
    size = models.CharField(max_length=3, choices=SupplierStockDetails.SIZE_CHOICES)
    pcs = models.IntegerField(null=True, blank=True, default=0)
    Buy_cost = models.IntegerField(null=True, blank=True, default=0)
    Sale_cost = models.IntegerField(null=True, blank=True, default=0)
    Profit = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return f'{self.Product_name} - {self.pcs}'