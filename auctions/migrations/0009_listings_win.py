# Generated by Django 3.0.8 on 2020-07-25 12:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_bet'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='win',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='win', to=settings.AUTH_USER_MODEL),
        ),
    ]
