# Generated by Django 2.2.5 on 2019-10-20 03:36

import aims.inventory.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('availability', models.CharField(help_text='Availability Status', max_length=100, unique=True, verbose_name='Availability')),
                ('description', models.CharField(blank=True, help_text='Description', max_length=200, null=True, verbose_name='Description')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Availability',
                'ordering': ['updated'],
            },
        ),
        migrations.CreateModel(
            name='Commodity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commodity_name', models.CharField(help_text='Name of the Commodity', max_length=100, unique=True, verbose_name='Commodity')),
                ('description', models.CharField(blank=True, help_text='Description', max_length=200, null=True, verbose_name='Description')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Commodity',
                'ordering': ['updated'],
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(help_text='Name of the Type', max_length=100, unique=True, verbose_name='Type')),
                ('description', models.CharField(blank=True, help_text='Description', max_length=200, null=True, verbose_name='Description')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Type',
                'ordering': ['updated'],
            },
        ),
        migrations.CreateModel(
            name='UnitOfMeasure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uom', models.CharField(help_text='Unit Of Measure for Parts', max_length=100, unique=True, verbose_name='Unit Of Measure')),
                ('description', models.CharField(blank=True, help_text='Description', max_length=200, null=True, verbose_name='Description')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'UnitOfMeasure',
                'ordering': ['updated'],
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_name', models.CharField(help_text='Vendor Name', max_length=100, unique=True, verbose_name='Vendor Name')),
                ('vendor_code', models.CharField(default=aims.inventory.models.gen_vendor_code, editable=False, help_text='Vendor Code', max_length=10, unique=True, verbose_name='Vendor Code')),
                ('vendor_address', models.CharField(help_text='Vendor address', max_length=120, unique=True, verbose_name='Vendor address')),
                ('vendor_poc', models.CharField(help_text='Vendor Point of Contact', max_length=120, verbose_name='Vendor POC')),
                ('email1', models.EmailField(max_length=254, verbose_name='Vendor Email-1')),
                ('email2', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Vendor Email-2')),
                ('phone_number1', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Vendor phone number 1')),
                ('phone_number2', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Vendor phone number 2')),
                ('products_available', models.CharField(blank=True, help_text='Type of Products Available', max_length=120, null=True, verbose_name='Type of Products Available')),
                ('procured_by_adm', models.CharField(help_text='Components Procured by ADM', max_length=120, verbose_name='Components Procured by ADM')),
                ('vendor_since', models.DateField()),
                ('adm_poc', models.CharField(help_text='ADM Point of Contact', max_length=120, verbose_name='ADM POC')),
                ('remarks', models.CharField(blank=True, help_text='Warehouse Remarks', max_length=200, null=True, verbose_name='Remarks')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'db_table': 'Vendor',
                'ordering': ['updated'],
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('warehouse_name', models.CharField(help_text='Warehouse Name', max_length=100, unique=True, verbose_name='Warehouse Name')),
                ('warehouse_code', models.CharField(default=aims.inventory.models.gen_warehouse_code, editable=False, help_text='Warehouse Code', max_length=10, unique=True, verbose_name='Warehouse Code')),
                ('address', models.CharField(help_text='Warehouse address', max_length=120, unique=True, verbose_name='Warehouse address')),
                ('city', models.CharField(help_text='Warehouse City', max_length=120, verbose_name='Warehouse City')),
                ('phone_number', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('warehouse_email', models.EmailField(max_length=254, verbose_name='Warehouse Email')),
                ('incharge_name', models.CharField(help_text='Warehouse incharge', max_length=120, verbose_name='Warehouse incharge')),
                ('incharge_email', models.EmailField(max_length=254, verbose_name='Warehouse Incharge Email')),
                ('incharge_phone_number', models.CharField(blank=True, help_text='Warehouse Incharge Number', max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Incharge Number')),
                ('aims_person', models.CharField(help_text='AIMS Person', max_length=120, verbose_name='AIMS Person')),
                ('aims_person_phone_number', models.CharField(blank=True, help_text='AIMS Person Number', max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='AIMS Person Number')),
                ('remarks', models.CharField(blank=True, help_text='Warehouse Remarks', max_length=200, null=True, verbose_name='Remarks')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'db_table': 'Warehouse',
                'ordering': ['updated'],
            },
        ),
        migrations.CreateModel(
            name='Parts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_name', models.CharField(help_text='Name of the Part', max_length=100, unique=True, verbose_name='Part Name')),
                ('part_number', models.CharField(help_text='Unique Part Number', max_length=12, unique=True, validators=[django.core.validators.MinLengthValidator(12)], verbose_name='Part Number')),
                ('part_description', models.CharField(help_text='Part Description', max_length=500, verbose_name='Description')),
                ('vendor_name', models.CharField(help_text='Vendor Name', max_length=100, verbose_name='Vendor Name')),
                ('weight', models.CharField(help_text='Weight', max_length=100, verbose_name='Weight')),
                ('part_class', models.CharField(help_text='Part Class', max_length=60, verbose_name='Part Class')),
                ('dimensions', models.CharField(help_text='Part Dimensions', max_length=60, verbose_name='Dimensions')),
                ('tech_spec', models.CharField(help_text='Tech Specifications', max_length=120, verbose_name='Tech Spec')),
                ('part_life', models.CharField(help_text='Part Life', max_length=120, verbose_name='Part Life')),
                ('reorder_point', models.PositiveIntegerField(help_text='Reorder Point', verbose_name='Reorder Point')),
                ('lead_time', models.PositiveIntegerField(help_text='Lead Time In Days', verbose_name='Lead time')),
                ('safety_stock', models.PositiveIntegerField(help_text='Safety Stock', verbose_name='Safety Stock')),
                ('remarks', models.CharField(blank=True, help_text='Part Remarks', max_length=200, null=True, verbose_name='Remarks')),
                ('part_image', models.ImageField(help_text='Part Image', upload_to='image', verbose_name='Image')),
                ('part_usermanual', models.FileField(blank=True, help_text='Any Documents Related to Part', null=True, upload_to='documents/', verbose_name='Part Documents')),
                ('slug', models.SlugField(unique=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('availability', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.Availability')),
                ('commodity_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.Commodity')),
                ('part_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.Type')),
                ('unit_of_measure', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.UnitOfMeasure')),
            ],
            options={
                'db_table': 'Part',
                'ordering': ['updated'],
            },
        ),
        migrations.CreateModel(
            name='Overseasinvoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_name', models.CharField(blank=True, help_text='Name of the Part', max_length=100, null=True, verbose_name='Part Name')),
                ('vendor_code', models.CharField(blank=True, default=0, editable=False, help_text='Vendor Code', max_length=10, null=True, verbose_name='Vendor Code')),
                ('invoice_number', models.CharField(help_text='Invoice Number', max_length=40, verbose_name='Invoice Number')),
                ('invoice_date', models.DateField(help_text='Invoice Date', verbose_name='Invoice Date')),
                ('invoice_quantity', models.DecimalField(decimal_places=3, help_text='Invoice Quantity', max_digits=12, verbose_name='Invoice Quantity')),
                ('invoice_amount', models.DecimalField(blank=True, decimal_places=3, help_text='Invoice Amount', max_digits=12, null=True, verbose_name='Invoice Amount')),
                ('invoice_gst', models.DecimalField(blank=True, decimal_places=3, help_text='Invoice GST Percentage', max_digits=12, null=True, verbose_name='Invoice GST %')),
                ('invoice_gst_amount', models.DecimalField(blank=True, decimal_places=3, help_text='Invoice GST Amount', max_digits=12, null=True, verbose_name='Invoice GST Amount')),
                ('bank_charges', models.DecimalField(blank=True, decimal_places=3, help_text='Bank Charges if any', max_digits=12, null=True, verbose_name='Bank Charges')),
                ('total_invoice_amount', models.DecimalField(decimal_places=3, help_text='Sum of the Invoice amount + Invoice GST Amount + Banck Charges', max_digits=12, verbose_name='Total Invoice Amount')),
                ('boe_number', models.CharField(blank=True, help_text='Bill of Entry Number', max_length=40, null=True, verbose_name='BOE Number')),
                ('boe_date', models.DateField(blank=True, help_text='Bill of Entry Date', null=True, verbose_name='BOE Date')),
                ('bcd', models.DecimalField(blank=True, decimal_places=3, help_text='Basic Customs Duty Percentage', max_digits=12, null=True, verbose_name='BCD Percentage')),
                ('bcd_amount', models.DecimalField(blank=True, decimal_places=3, help_text='Basic Customs Duty Amount', max_digits=12, null=True, verbose_name='BCD Amount')),
                ('customs_gst', models.DecimalField(blank=True, decimal_places=3, help_text='Customs GST Percentage', max_digits=12, null=True, verbose_name='Customs GST %')),
                ('customs_gst_amount', models.DecimalField(blank=True, decimal_places=3, help_text='Customs GST Amount', max_digits=12, null=True, verbose_name='Customs GST Amount')),
                ('customs_fine_amount', models.DecimalField(blank=True, decimal_places=3, help_text='Customs Fine Amount if any', max_digits=12, null=True, verbose_name='Customs Fine Amount')),
                ('intrest_amount', models.DecimalField(blank=True, decimal_places=3, help_text='Interest Amount if any', max_digits=12, null=True, verbose_name='Interest Amount')),
                ('total_duty_amount', models.DecimalField(decimal_places=3, default=0, help_text='Sum of the BCD amount + Customs GST Amount + Fine Amount + Intrest Amount', max_digits=12, verbose_name='Total Duty Amount')),
                ('fright_agency', models.CharField(blank=True, help_text='Freight Agency Company Name', max_length=40, null=True, verbose_name='Freight Agency')),
                ('weight', models.CharField(blank=True, help_text='Weight', max_length=40, null=True, verbose_name='weight')),
                ('fright_invoice_number', models.CharField(blank=True, help_text='Freight Invoice Number', max_length=40, null=True, verbose_name='Freight Invoice Number')),
                ('fright_invoice_date', models.DateField(blank=True, help_text='Freight Invoice Date', null=True, verbose_name='Freight Invoice Date')),
                ('fright_charges_taxable', models.DecimalField(blank=True, decimal_places=3, help_text='Taxable Freight Charges', max_digits=12, null=True, verbose_name='Freight Charges Taxable')),
                ('fright_gst', models.DecimalField(blank=True, decimal_places=3, help_text='Freight GST Percentage', max_digits=12, null=True, verbose_name='Freight GST %')),
                ('fright_gst_amount', models.DecimalField(blank=True, decimal_places=3, help_text='Freight GST Amount', max_digits=12, null=True, verbose_name='Freight GST Amount')),
                ('fright_charges_nontaxable', models.DecimalField(blank=True, decimal_places=3, help_text='Non Taxable Freight Charges', max_digits=12, null=True, verbose_name='Freight Charges Non Taxable')),
                ('total_fright_amount', models.DecimalField(decimal_places=3, default=0, help_text='Total Freight Amount', max_digits=12, verbose_name='Total Freight Amount')),
                ('clearance_agency', models.CharField(blank=True, help_text='Clearance Agency Company', max_length=40, null=True, verbose_name='Clearance Agency')),
                ('clearance_invoice_number', models.CharField(blank=True, help_text='Clearance Invoice Number', max_length=40, null=True, verbose_name='Clearance Invoice Number')),
                ('clearance_invoice_date', models.DateField(blank=True, help_text='Clearance Invoice Date', null=True, verbose_name='Clearance Invoice Date')),
                ('clearance_charges_taxable', models.DecimalField(blank=True, decimal_places=3, help_text='Taxable Clearance Charges', max_digits=12, null=True, verbose_name='Clearance Charges Taxable')),
                ('clearance_gst', models.DecimalField(blank=True, decimal_places=3, help_text='Clearance GST Percentage', max_digits=12, null=True, verbose_name='Clearance GST %')),
                ('clearance_gst_amount', models.DecimalField(blank=True, decimal_places=3, help_text='Clearance GST Amount', max_digits=12, null=True, verbose_name='Clearance GST Amount')),
                ('clearance_charges_nontaxable', models.DecimalField(blank=True, decimal_places=3, help_text='Non Taxable Clearance Charges', max_digits=12, null=True, verbose_name='Clearance Charges Non Taxable')),
                ('local_transport_fee', models.DecimalField(blank=True, decimal_places=3, help_text='Local Transport Fee', max_digits=12, null=True, verbose_name='Local Transport Fee')),
                ('total_clearance_amount', models.DecimalField(decimal_places=3, default=0, help_text='Total Clearance Amount', max_digits=12, verbose_name='Total Clearance Amount')),
                ('total_amount', models.DecimalField(decimal_places=3, default=0, editable=False, help_text='Total Amount', max_digits=12, verbose_name='Total Amount')),
                ('price_per_part', models.DecimalField(decimal_places=3, default=0, editable=False, help_text='Price per Part', max_digits=12, verbose_name='Price per Part')),
                ('stage', models.CharField(blank=True, help_text='Invoice Stage', max_length=40, null=True, verbose_name='Invoice Stage')),
                ('remarks', models.CharField(blank=True, help_text='Part Remarks', max_length=200, null=True, verbose_name='Remarks')),
                ('slug', models.SlugField(default=uuid.uuid4, editable=False, unique=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('part_number', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.Parts', verbose_name='Part Number')),
                ('unit_of_measure', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.UnitOfMeasure', verbose_name='Unit of Measure')),
                ('vendor_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='inventory.Vendor', verbose_name='Vendor Name')),
            ],
            options={
                'db_table': 'Overseasinvoice',
                'ordering': ['updated'],
            },
        ),
        migrations.CreateModel(
            name='Outward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_name', models.CharField(blank=True, help_text='Name of the Part', max_length=100, null=True, verbose_name='Part Name')),
                ('quantity', models.PositiveIntegerField(help_text='Quantity', verbose_name='Quantity')),
                ('batch_number', models.CharField(blank=True, help_text='Batch Number if any', max_length=40, null=True, verbose_name='Batch Number if any')),
                ('outward_receipt_number', models.CharField(default=aims.inventory.models.gen_orn, help_text='Outward Receipt Number', max_length=40, verbose_name='Outward Receipt Number')),
                ('authorised_by', models.CharField(help_text='Authorised User Name', max_length=20, verbose_name='Authorised By')),
                ('verified_by', models.CharField(help_text='Verified User Name', max_length=20, verbose_name='Verified By')),
                ('mode_of_transport', models.CharField(help_text='Mode of Transport', max_length=120, verbose_name='Mode of Transport')),
                ('transport_charges', models.PositiveIntegerField(default=0, help_text='Transport Charges if any', verbose_name='Transport Charges')),
                ('remarks', models.CharField(blank=True, help_text='Part Remarks', max_length=200, null=True, verbose_name='Remarks')),
                ('slug', models.SlugField(default=uuid.uuid4, editable=False, unique=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('from_warehouse_name', models.ForeignKey(help_text='Select Warehouse Name from where part is Outward/Sent', on_delete=django.db.models.deletion.PROTECT, related_name='outward_from_warehouse_name', to='inventory.Warehouse')),
                ('part_number', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.Parts')),
                ('part_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.Type')),
                ('to_warehouse_name', models.ForeignKey(blank=True, help_text='Select Warehouse Name if Part is internal transfered', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='outward_to_warehouse_name', to='inventory.Warehouse')),
                ('unit_of_measure', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.UnitOfMeasure')),
                ('vendor_name', models.ForeignKey(blank=True, help_text='Select Vendor Name if Part is sent to Vendor', null=True, on_delete=django.db.models.deletion.PROTECT, to='inventory.Vendor')),
            ],
            options={
                'db_table': 'Outward',
                'ordering': ['updated'],
            },
        ),
        migrations.CreateModel(
            name='Inward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_name', models.CharField(blank=True, help_text='Name of the Part', max_length=100, null=True, verbose_name='Part Name')),
                ('received_date', models.DateField(help_text='Parts Inward Date', verbose_name='In Date')),
                ('invoice_number', models.CharField(help_text='Invoice Number', max_length=40, verbose_name='Invoice Number')),
                ('invoice_date', models.DateField(help_text='Invoice Date', verbose_name='Invoice Date')),
                ('invoice_quantity', models.PositiveIntegerField(help_text='Invoice Quantity', verbose_name='Invoice Quantity')),
                ('received_quantity', models.PositiveIntegerField(help_text='Quantity Received', verbose_name='Received Quantity')),
                ('defected_quantity', models.PositiveIntegerField(default=0, help_text='Defected Quantity Received', verbose_name='Defected Items Quantity')),
                ('batch_number', models.CharField(blank=True, help_text='Batch Number if any', max_length=40, null=True, verbose_name='Batch Number if any')),
                ('recived_by', models.CharField(help_text='Enter Person Name', max_length=40, verbose_name='Items Received By')),
                ('remarks', models.CharField(blank=True, help_text='Part Remarks', max_length=200, null=True, verbose_name='Remarks')),
                ('transport_charges', models.PositiveIntegerField(default=0, help_text='Transport Charges if any', verbose_name='Transport Charges')),
                ('slug', models.SlugField(default=uuid.uuid4, editable=False, unique=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('from_warehouse_name', models.ForeignKey(blank=True, help_text='Select Warehouse Name if Part is internal transfered', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='inward_from_warehouse_name', to='inventory.Warehouse')),
                ('part_number', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.Parts')),
                ('part_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.Type')),
                ('to_warehouse_name', models.ForeignKey(help_text='Warehouse Name in which Part Inwarding', on_delete=django.db.models.deletion.PROTECT, related_name='inward_to_warehouse_name', to='inventory.Warehouse')),
                ('unit_of_measure', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.UnitOfMeasure')),
                ('vendor_name', models.ForeignKey(blank=True, help_text='Select Vendor Name if Part is Procured', null=True, on_delete=django.db.models.deletion.PROTECT, to='inventory.Vendor')),
            ],
            options={
                'db_table': 'Inward',
                'ordering': ['updated'],
            },
        ),
        migrations.CreateModel(
            name='Domesticinvoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_name', models.CharField(blank=True, help_text='Name of the Part', max_length=100, null=True, verbose_name='Part Name')),
                ('vendor_code', models.CharField(blank=True, default=0, editable=False, help_text='Vendor Code', max_length=10, null=True, verbose_name='Vendor Code')),
                ('invoice_number', models.CharField(help_text='Invoice Number', max_length=40, verbose_name='Invoice Number')),
                ('invoice_date', models.DateField(help_text='Invoice Date', verbose_name='Invoice Date')),
                ('invoice_quantity', models.DecimalField(decimal_places=3, help_text='Invoice Quantity', max_digits=12, verbose_name='Invoice Quantity')),
                ('invoice_amount', models.DecimalField(decimal_places=3, help_text='Invoice Amount', max_digits=12, verbose_name='Invoice Amount')),
                ('invoice_gst', models.DecimalField(blank=True, decimal_places=3, help_text='Invoice GST (%)', max_digits=12, null=True, verbose_name='Invoice GST Percentage')),
                ('invoice_gst_amount', models.DecimalField(blank=True, decimal_places=3, help_text='Invoice GST Amount', max_digits=12, null=True, verbose_name='Invoice GST Amount')),
                ('transport_charges', models.DecimalField(decimal_places=3, default=0, help_text='Transport Charges', max_digits=12, verbose_name='Transport Charges')),
                ('total_invoice_amount', models.DecimalField(decimal_places=3, help_text='Sum of the Invoice amount + Invoice GST Amount + Bank Charges', max_digits=12, verbose_name='Total Invoice Amount')),
                ('price_per_part', models.DecimalField(decimal_places=3, default=0, editable=False, help_text='Price per Part', max_digits=12, verbose_name='Price per Part')),
                ('stage', models.CharField(blank=True, help_text='Invoice Stage', max_length=40, null=True, verbose_name='Invoice Stage')),
                ('remarks', models.CharField(blank=True, help_text='Part Remarks', max_length=200, null=True, verbose_name='Remarks')),
                ('slug', models.SlugField(default=uuid.uuid4, editable=False, unique=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('part_number', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.Parts', verbose_name='Part Number')),
                ('unit_of_measure', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.UnitOfMeasure', verbose_name='Unit of Measure')),
                ('vendor_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='inventory.Vendor', verbose_name='Vendor Name')),
            ],
            options={
                'db_table': 'Domesticinvoice',
                'ordering': ['updated'],
            },
        ),
    ]
