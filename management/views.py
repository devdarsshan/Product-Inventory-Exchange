from django.shortcuts import render,redirect,reverse
from django.utils.timezone import now
from django.http import HttpResponse
from .models import *
from .forms import *


def dashboard(request):
    supp = Supplier.objects.all()
    sup_ord = SupplierOrderDetails.objects.all()
    data = {"Suppliers":supp,"Sup_ord":sup_ord}
    return render(request,"management/dashboard.html",data)

def suppliers(request,pk):
    #SUPPLIER
    supp = Supplier.objects.get(id=pk)
    supp_stk = supp.supplierstockdetails_set.all()     
    if supp_stk:   
        custom_order = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
        sorted_stocks = sorted(supp_stk, key=lambda stock: custom_order.index(stock.Size))
        credit_balance = supp_stk.first().Total_sup_cost
        #ORDER
        supp_ord = supp.supplierorderdetails_set.all()
        #PAYMENT
        payment_det = supp.paymentdetails_set.all()
        Total_Payed = 0
        for pay in payment_det:
            Total_Payed+=pay.Amount_payed

        if Total_Payed>credit_balance:
            balance = Total_Payed- credit_balance
            print(Total_Payed,"-",credit_balance)
        else:
            balance = 0

        data = {"sup_stk":sorted_stocks,'sup_ord':supp_ord,'pay_det':payment_det,'Cred_bal':credit_balance,'Tot_pay':Total_Payed,'sup_id':pk,'balance':balance}
        return render(request,"management/suppliers.html",data)
    data = {'sup_id':pk}
    return render(request,"management/suppliers.html",data)

def Payment_details(request,idd):
    supp = Supplier.objects.get(id=idd)
    supp_stk = supp.supplierstockdetails_set.all()  
    payment_det = supp.paymentdetails_set.all()
    if supp_stk:
        credit_balance = supp_stk.first().Total_sup_cost
        Total_Payed = 0
        for pay in payment_det:
            Total_Payed+=pay.Amount_payed

        data = {'pay_det':payment_det,'Cred_bal':credit_balance,'Tot_pay':Total_Payed,'sup_id':idd}
        return render(request,"management/pay_details.html",data)
    data = {'sup_id':idd}
    return render(request,"management/pay_details.html",data)

def order_details(request,idd):
    supp = Supplier.objects.get(id=idd)
    supp_ord = supp.supplierorderdetails_set.all()
    data = {'sup_ord':supp_ord,'sup_id':supp.id}

    return render(request,"management/order_list.html",data)

def customers(request):
    return render(request,"management/customers.html")

def new_product(request,pk):
    sup = Supplier.objects.get(id=pk)
    form = ProductsForm(initial={'Supplier_Name': sup}, instance=sup)
    if request.method == 'POST':
        form = ProductsForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.Supplier_Name = sup
            form.save()
            return redirect(reverse('supp_page', args=[pk]))

    data = {'form':form}
    return render(request,"management/products_form.html",data)

def supp_order(request,pk):
    sup = Supplier.objects.get(id=pk)
    order = SupplierOrderDetails(sup_name=sup)  # Create a new instance of SupplierOrderDetails with the sup_name set
    form = SupplierOrderForm(initial={'Date': now()},instance=order)  # Use the order instance for the form
    if request.method == 'POST':
        form = SupplierOrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_cost = order.pcs * order.Pcs_cost
            order.save()

            supplier_stock = SupplierStockDetails.objects.filter(Supplier_Name=pk).first()
            if supplier_stock:
                supplier_stock.calculate_total_size_cost()  # Update Total_size_cost
                supplier_stock.calculate_total_sup_cost()  # Update Total_sup_cost
                supplier_stock.save()
            return redirect(reverse('supp_page', args=[pk]))

    data = {'form':form}

    return render(request,"management/supp_order_form.html",data)

def update_order(request,pk):
    order = SupplierOrderDetails.objects.get(id=pk)
    form = SupplierOrderForm(instance=order)
    if request.method == 'POST':
        form = SupplierOrderForm(request.POST,instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_cost = order.pcs * order.Pcs_cost
            order.save()

            supplier_stock = SupplierStockDetails.objects.filter(Supplier_Name=order.sup_name,Product_name=order.product_name,Size=order.size).first()
            if supplier_stock:
                supplier_stock.Pcs_cost = order.Pcs_cost
                supplier_stock.calculate_total_size_cost()  # Update Total_size_cost
                supplier_stock.calculate_total_sup_cost()  # Update Total_sup_cost
                supplier_stock.save()
            return redirect(reverse('ord_list_page', args=[order.sup_name.id]))
        
    data = {'form':form}

    return render(request,"management/supp_order_form.html",data)

def payment_list(request,pk):
    sup = Supplier.objects.get(id=pk)
    form = PaymentForm(initial={'sup_name': sup, 'Date': now()}, instance=sup)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.sup_name = sup
            form.save()
            print("saved")
            return redirect(reverse('supp_page', args=[pk]))

    data = {'form':form}
    return render(request,"management/payment_form.html",data)

def update_payment(request, pk):
    payment = PaymentDetails.objects.get(id=pk)
    sup_id = payment.sup_name.id
    form = PaymentForm(instance=payment)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            updated_payment = form.save(commit=False)
            updated_payment.Amount_payed = updated_payment.Amount_payed  # Update the field you want to modify
            updated_payment.save()

            supplier_stock = SupplierStockDetails.objects.filter(Supplier_Name=payment.sup_name).first()
            if supplier_stock:
                supplier_stock.calculate_total_sup_cost()  # Update Total_sup_cost
                supplier_stock.save()
            return redirect(reverse('pay_page', args=[sup_id]))
        
    data = {'form': form,'sup_id':payment.sup_name}

    return render(request, "management/payment_form.html", data)

def delete_order(request, pk):
    order = SupplierOrderDetails.objects.get(id=pk)
    supplier_stock = SupplierStockDetails.objects.filter(
        Supplier_Name=order.sup_name,
        Product_name=order.product_name,
        Size=order.size
    ).first()

    if request.method == 'POST':
        order.delete()

        if supplier_stock:
            supplier_stock.Pcs -= order.pcs
            supplier_stock.Total_size_cost -= order.Pcs_cost * order.pcs
            supplier_stock.calculate_total_sup_cost()  # Update Total_sup_cost
            supplier_stock.save()
        return redirect(reverse('ord_list_page', args=[order.sup_name.id]))

    data = {'Prod': order.product_name,'Size':order.size}
    return render(request, "management/deleteord_form.html", data)

def deletepay(request,pk):
    payment = PaymentDetails.objects.get(id=pk)
    sup_id = payment.sup_name.id
    supplier_stock = SupplierStockDetails.objects.filter(Supplier_Name=payment.sup_name).first()

    if request.method == 'POST':
        payment.delete()

        if supplier_stock:
            supplier_stock.calculate_total_sup_cost()  # Update Total_sup_cost
            supplier_stock.save()
        return redirect(reverse('pay_page', args=[sup_id]))

    data = {'payment': payment.Comment}

    return render(request, "management/deletepay_form.html", data)

# def sell_details(request,pk):
    sup = Supplier.objects.get(id=pk)
    form = CustomerOrderForm(initial={'Supplier_name': sup, 'Date': now()}, instance=sup)
    if request.method == 'POST':
        form = CustomerOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            supplier_stock = SupplierStockDetails.objects.filter(Product_name=order.Product_name, Size=order.size).first()
        if supplier_stock:
            # Assign the Buy_cost based on the supplier stock details
            order.Buy_cost = supplier_stock.Pcs_cost

            # Check if there are enough available PCS in the stock
            if order.pcs <= supplier_stock.Pcs:
                # Deduct the ordered PCS from the stock
                supplier_stock.Pcs -= order.pcs
                supplier_stock.save()
            else:
                # Handle the case when there are not enough PCS in the stock
                raise ValueError("Not enough PCS available in the stock.")

            # Check if the remaining PCS in the stock is less than 100
            if supplier_stock.Pcs < 100:
                # Display an alert message using Django's messages framework
                messages.warning(request, f"Alert: PCS for {order.Product_name} - {order.size} is less than 100."
                )
        else:
            # Handle the case when supplier stock details are not found
            order.Buy_cost = 0

        # Calculate the Profit based on the Sale_cost and Buy_cost
        order.Profit = order.Sale_cost - order.Buy_cost

def sell_details(request,pk):
    supp = Supplier.objects.get(id=pk)
    sell_det = supp.custorder_set.all()

    data = {"list":sell_det,"sup_id":pk}
    return render(request,"management/cust_page.html",data)

def sell_order(request, pk):
    sup = Supplier.objects.get(id=pk)
    form = CustomerOrderForm(initial={'Supplier_name': sup, 'Date': now()}, instance=sup)
    if request.method == 'POST':
        form = CustomerOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            supplier_stock = SupplierStockDetails.objects.filter(Product_name=order.Product_name, Size=order.size).first()
            if supplier_stock:
                # Assign the Buy_cost based on the supplier stock details
                order.Buy_cost = supplier_stock.Pcs_cost

                # Check if there are enough available PCS in the stock
                if order.pcs <= supplier_stock.In_Stock:
                    # Deduct the ordered PCS from the stock
                    supplier_stock.In_Stock -= order.pcs
                    print("SUBTRACTED")
                    supplier_stock.save()
                else:
                    # Handle the case when there are not enough PCS in the stock
                    messages.error(request, f"Not enough PCS available in the stock for {order.Product_name} - {order.size}.")
                    return redirect(reverse('cust_page', args=[pk]))

                # Check if the remaining PCS in the stock is less than 100
                if supplier_stock.In_Stock < 100:
                    # Display an alert message using Django's messages framework
                    messages.warning(request, f"Alert: PCS for {order.Product_name} - {order.size} is less than 100.")

            else:
                # Handle the case when supplier stock details are not found
                messages.error(request, f"PCS not available in the stock for {order.Product_name} - {order.size}.")
                return redirect(reverse('cust_page', args=[pk]))

            # Calculate the Profit based on the Sale_cost and Buy_cost
            order.Profit = (order.Sale_cost - order.Buy_cost)*order.pcs

            order.save()

            return redirect(reverse('cust_page', args=[pk]))

    data = {'form': form}
    return render(request, "management/seller_form.html", data)
