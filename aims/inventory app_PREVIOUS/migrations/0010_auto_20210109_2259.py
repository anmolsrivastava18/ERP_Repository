# Generated by Django 2.2.5 on 2021-01-09 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_auto_20210109_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domesticinvoice',
            name='domestic_invoice',
            field=models.FileField(help_text='Invoice Related to this record', upload_to='domesticinvoice/', verbose_name='Invoice'),
        ),
    ]