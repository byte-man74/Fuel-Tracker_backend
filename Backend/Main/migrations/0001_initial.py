# Generated by Django 4.2 on 2023-06-10 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fueling_station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('logo', models.ImageField(upload_to='Fueling_station_Image_directory')),
                ('background_image', models.ImageField(upload_to='Fueling_station_Image_directory')),
            ],
        ),
        migrations.CreateModel(
            name='Fuel_Station_Traffic_Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('terrible_rating_count', models.IntegerField(default=0)),
                ('average_rating_count', models.IntegerField(default=0)),
                ('good_rating_count', models.IntegerField(default=0)),
                ('station', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Main.fueling_station')),
            ],
        ),
        migrations.CreateModel(
            name='Fuel_Station_Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.BigIntegerField(null=True)),
                ('votes', models.IntegerField(default=0)),
                ('last_updated', models.DateTimeField()),
                ('station', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Main.fueling_station')),
            ],
        ),
        migrations.CreateModel(
            name='Fuel_Station_Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.CharField(max_length=200, null=True)),
                ('latitude', models.CharField(max_length=200, null=True)),
                ('station', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Main.fueling_station')),
            ],
        ),
        migrations.CreateModel(
            name='Fuel_Station_Extra_Information',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_votes_for_fuel_station_being_open', models.IntegerField(default=0)),
                ('number_of_votes_for_fuel_station_being_close', models.IntegerField(default=0)),
                ('station', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Main.fueling_station')),
            ],
        ),
    ]
