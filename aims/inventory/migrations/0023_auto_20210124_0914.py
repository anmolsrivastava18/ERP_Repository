# Generated by Django 2.2.5 on 2021-01-24 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0022_auto_20210124_0208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parts',
            name='part_image',
            field=models.ImageField(blank=True, null=True, upload_to='image', verbose_name='Image'),
        ),
    ]
