# Generated by Django 2.2.5 on 2021-01-03 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20200206_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parts',
            name='dimensions',
            field=models.CharField(blank=True, help_text='Part Dimensions', max_length=60, verbose_name='Dimensions'),
        ),
        migrations.AlterField(
            model_name='parts',
            name='part_class',
            field=models.CharField(blank=True, help_text='Part Class', max_length=60, verbose_name='Part Class'),
        ),
        migrations.AlterField(
            model_name='parts',
            name='part_image',
            field=models.ImageField(blank=True, help_text='Part Image', upload_to='image', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='parts',
            name='part_life',
            field=models.CharField(blank=True, help_text='Part Life', max_length=120, verbose_name='Part Life'),
        ),
        migrations.AlterField(
            model_name='parts',
            name='tech_spec',
            field=models.CharField(blank=True, help_text='Tech Specifications', max_length=120, verbose_name='Tech Spec'),
        ),
        migrations.AlterField(
            model_name='parts',
            name='weight',
            field=models.CharField(blank=True, help_text='Weight', max_length=100, verbose_name='Weight'),
        ),
    ]