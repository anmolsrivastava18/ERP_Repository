# Generated by Django 2.2.5 on 2021-01-25 19:38

import aims.inventory.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0024_remove_parts_part_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='warehouse',
            name='aims_person',
        ),
        migrations.RemoveField(
            model_name='warehouse',
            name='aims_person_phone_number',
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='address',
            field=models.CharField(max_length=120, unique=True, verbose_name='Warehouse address'),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='city',
            field=models.CharField(max_length=120, verbose_name='Warehouse City'),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='incharge_name',
            field=models.CharField(max_length=120, verbose_name='Warehouse incharge'),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='incharge_phone_number',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name="Incharge's Contact No."),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='remarks',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Remarks'),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='warehouse_code',
            field=models.CharField(default=aims.inventory.models.gen_warehouse_code, editable=False, max_length=10, unique=True, verbose_name='Warehouse Code'),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='warehouse_name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Warehouse Name'),
        ),
    ]
