# Generated by Django 2.2.5 on 2021-01-16 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_individualdomesticinvoice'),
    ]

    operations = [
        migrations.RenameField(
            model_name='individualdomesticinvoice',
            old_name='invoiceDate',
            new_name='invoice_date',
        ),
        migrations.RenameField(
            model_name='individualdomesticinvoice',
            old_name='invoiceNumber',
            new_name='invoice_number',
        ),
    ]
