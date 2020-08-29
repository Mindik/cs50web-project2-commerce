# Generated by Django 3.0.8 on 2020-07-25 10:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_listings_max_bet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('newBet', models.FloatField()),
                ('id_listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listBet', to='auctions.Listings')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userBet', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
