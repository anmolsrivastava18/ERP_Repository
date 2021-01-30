# Generated by Django 2.2.5 on 2019-12-15 09:48

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillOfMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bom_name', models.CharField(help_text='BOM name', max_length=100, unique=True, verbose_name='BOM Name')),
                ('bom_description', models.CharField(blank=True, help_text='BOM description', max_length=500, null=True, verbose_name='BOM Description')),
                ('parts', django.contrib.postgres.fields.jsonb.JSONField()),
                ('bom_file', models.FileField(blank=True, help_text='Any Documents Related to BOM', null=True, upload_to='documents/', verbose_name='BOM Document')),
                ('remarks', models.CharField(blank=True, help_text='BOM Remarks', max_length=200, null=True, verbose_name='Remarks')),
                ('slug', models.SlugField(default=uuid.uuid4, editable=False, unique=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'BillOfMaterials',
                'ordering': ['updated'],
                'permissions': [('full_details_billofmaterial', 'Can View Full Details BillOfMaterials')],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(help_text='Name of the Product', max_length=100, unique=True, verbose_name='Product Name')),
                ('description', models.CharField(blank=True, help_text='Description', max_length=200, null=True, verbose_name='Description')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Product',
                'ordering': ['updated'],
                'permissions': [('full_details_product', 'Can View Full Details Product')],
            },
        ),
        migrations.AlterModelOptions(
            name='availability',
            options={'ordering': ['updated'], 'permissions': [('full_details_availability', 'Can View Full Details Availability')]},
        ),
        migrations.AlterModelOptions(
            name='commodity',
            options={'ordering': ['updated'], 'permissions': [('full_details_commodity', 'Can View Full Details Commodity')]},
        ),
        migrations.AlterModelOptions(
            name='domesticinvoice',
            options={'ordering': ['updated'], 'permissions': [('full_details_domesticinvoice', 'Can View Full Details Domesticinvoice')]},
        ),
        migrations.AlterModelOptions(
            name='inward',
            options={'ordering': ['updated'], 'permissions': [('full_details_inward', 'Can View Full Details Inward')]},
        ),
        migrations.AlterModelOptions(
            name='outward',
            options={'ordering': ['updated'], 'permissions': [('full_details_outward', 'Can View Full Details Outward')]},
        ),
        migrations.AlterModelOptions(
            name='overseasinvoice',
            options={'ordering': ['updated'], 'permissions': [('full_details_overseasinvoice', 'Can View Full Details Overseasinvoice')]},
        ),
        migrations.AlterModelOptions(
            name='parts',
            options={'ordering': ['updated'], 'permissions': [('full_details_parts', 'Can View Full Details Part')]},
        ),
        migrations.AlterModelOptions(
            name='type',
            options={'ordering': ['updated'], 'permissions': [('full_details_type', 'Can View Full Details Type')]},
        ),
        migrations.AlterModelOptions(
            name='unitofmeasure',
            options={'ordering': ['updated'], 'permissions': [('full_details_unitofmeasure', 'Can View Full Details UnitOfMeasure')]},
        ),
        migrations.AlterModelOptions(
            name='vendor',
            options={'ordering': ['updated'], 'permissions': [('full_details_vendor', 'Can View Full Details Vendor')]},
        ),
        migrations.AlterModelOptions(
            name='warehouse',
            options={'ordering': ['updated'], 'permissions': [('full_details_warehouse', 'Can View Full Details Warehouse')]},
        ),
        migrations.AddField(
            model_name='domesticinvoice',
            name='domestic_invoice',
            field=models.FileField(blank=True, help_text='Invoice Related to this record', null=True, upload_to='domesticinvoice/', verbose_name='Invoice'),
        ),
        migrations.AddField(
            model_name='overseasinvoice',
            name='clearance_invoice',
            field=models.FileField(blank=True, help_text='Clearance Invoice Related to this record', null=True, upload_to='overseasinvoice/clearance', verbose_name='Clearance Invoice'),
        ),
        migrations.AddField(
            model_name='overseasinvoice',
            name='customs_invoice',
            field=models.FileField(blank=True, help_text='Customs Invoice Related to this record', null=True, upload_to='overseasinvoice/customs', verbose_name='Customs Invoice'),
        ),
        migrations.AddField(
            model_name='overseasinvoice',
            name='fright_invoice',
            field=models.FileField(blank=True, help_text='Fright Invoice Related to this record', null=True, upload_to='overseasinvoice/fright', verbose_name='Fright Invoice'),
        ),
        migrations.AddField(
            model_name='overseasinvoice',
            name='overseas_invoice',
            field=models.FileField(blank=True, help_text='Invoice Related to this record', null=True, upload_to='overseasinvoice/', verbose_name='Invoice'),
        ),
        migrations.CreateModel(
            name='AveragePrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('average_price', models.DecimalField(decimal_places=3, help_text='Average Price of a part', max_digits=12, verbose_name='Average Price')),
                ('slug', models.SlugField(default=uuid.uuid4, editable=False, unique=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('part_number', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.Parts', verbose_name='Part Number')),
            ],
            options={
                'db_table': 'AveragePrice',
                'ordering': ['updated'],
                'permissions': [('full_details_averageprice', 'Can View Full Details AveragePrice')],
            },
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_id', models.CharField(editable=False, max_length=100, unique=True)),
                ('parts', django.contrib.postgres.fields.jsonb.JSONField(default=dict, verbose_name='Parts Used Details')),
                ('mfg_date', models.DateField(help_text='Mfg Date', verbose_name='Mfg Date')),
                ('quantity', models.PositiveIntegerField(default=1, help_text='Quantity', verbose_name='Quantity')),
                ('asset_state', models.CharField(choices=[('On Lease', 'Lease'), ('Warehouse Change', 'Warehouse Change'), ('In warehouse', 'In warehouse')], default='In warehouse', max_length=100, verbose_name='Asset State')),
                ('total_price', models.DecimalField(decimal_places=3, help_text='Total Raw Material Cost of an Asset', max_digits=20, verbose_name='Total Price')),
                ('remarks', models.CharField(blank=True, help_text='Remarks', max_length=200, null=True, verbose_name='Remarks')),
                ('slug', models.SlugField(unique=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('bom_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.BillOfMaterial', verbose_name='BOM Name')),
                ('product_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.Product', verbose_name='Product Name')),
                ('warehouse_name', models.ForeignKey(help_text='Select Warehouse Name where the part is in.', on_delete=django.db.models.deletion.PROTECT, to='inventory.Warehouse', verbose_name='Warehouse Name')),
            ],
            options={
                'db_table': 'Asset',
                'ordering': ['updated'],
                'permissions': [('full_details_asset', 'Can View Full Details Asset')],
            },
        ),
    ]
