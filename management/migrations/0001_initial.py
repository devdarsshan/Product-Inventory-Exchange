# Generated by Django 4.1.6 on 2023-06-01 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Product_Name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Supplier_Name', models.CharField(max_length=255)),
                ('Supplier_Email', models.EmailField(blank=True, max_length=254, null=True)),
                ('Supplier_phonenumber', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SupplierStockDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Size', models.CharField(choices=[('XS', 'Extra Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large'), ('XXL', 'Double Extra Large')], max_length=3)),
                ('Pcs', models.IntegerField(blank=True, default=0, null=True)),
                ('Pcs_cost', models.IntegerField()),
                ('Total_size_cost', models.IntegerField(blank=True, default=0, null=True)),
                ('Total_sup_cost', models.IntegerField(blank=True, default=0, null=True)),
                ('Product_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.products')),
                ('Supplier_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='SupplierOrderDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField()),
                ('size', models.CharField(choices=[('XS', 'Extra Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large'), ('XXL', 'Double Extra Large')], max_length=3)),
                ('pcs', models.IntegerField()),
                ('Pcs_cost', models.IntegerField()),
                ('total_cost', models.IntegerField()),
                ('product_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.products')),
                ('sup_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.supplier')),
            ],
        ),
        migrations.AddField(
            model_name='products',
            name='Supplier_Name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.supplier'),
        ),
        migrations.CreateModel(
            name='PaymentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField()),
                ('Amount_payed', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Comment', models.TextField()),
                ('sup_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.supplier')),
            ],
        ),
    ]
