# Generated by Django 4.2.2 on 2023-07-10 07:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Main', '0008_alter_fueling_station_background_image_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fueling_station',
            name='agent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]