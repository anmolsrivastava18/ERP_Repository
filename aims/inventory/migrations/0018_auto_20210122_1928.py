# Generated by Django 2.2.5 on 2021-01-22 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0017_auto_20210118_0138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualdomesticinvoice',
            name='part_number',
            field=models.CharField(max_length=20, verbose_name='Part Number'),
        ),
    ]
