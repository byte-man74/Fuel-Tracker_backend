# Generated by Django 4.2 on 2023-06-10 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fuel_station_price',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='fueling_station',
            name='background_image',
            field=models.ImageField(null=True, upload_to='Fueling_station_Image_directory'),
        ),
        migrations.AlterField(
            model_name='fueling_station',
            name='logo',
            field=models.ImageField(null=True, upload_to='Fueling_station_Image_directory'),
        ),
    ]
