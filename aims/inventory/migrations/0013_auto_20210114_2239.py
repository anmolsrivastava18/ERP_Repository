# Generated by Django 2.2.5 on 2021-01-14 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_remove_domesticinvoice_vendor_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='domesticinvoice',
            name='invoice_amount',
        ),
        migrations.RemoveField(
            model_name='domesticinvoice',
            name='invoice_gst',
        ),
        migrations.RemoveField(
            model_name='domesticinvoice',
            name='invoice_gst_amount',
        ),
        migrations.RemoveField(
            model_name='domesticinvoice',
            name='invoice_quantity',
        ),
        migrations.RemoveField(
            model_name='domesticinvoice',
            name='part_name',
        ),
        migrations.RemoveField(
            model_name='domesticinvoice',
            name='part_number',
        ),
        migrations.RemoveField(
            model_name='domesticinvoice',
            name='price_per_part',
        ),
        migrations.RemoveField(
            model_name='domesticinvoice',
            name='stage',
        ),
        migrations.RemoveField(
            model_name='domesticinvoice',
            name='unit_of_measure',
        ),
    ]