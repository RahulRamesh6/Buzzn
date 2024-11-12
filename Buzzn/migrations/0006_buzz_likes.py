# Generated by Django 5.1.2 on 2024-11-07 17:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buzzn', '0005_buzz'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='buzz',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='buzz_like', to=settings.AUTH_USER_MODEL),
        ),
    ]