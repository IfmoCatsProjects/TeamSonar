# Generated by Django 4.2.7 on 2024-01-09 11:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('friendship', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='follow',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_sender', to=settings.AUTH_USER_MODEL),
        ),
    ]