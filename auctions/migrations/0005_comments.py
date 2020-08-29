# Generated by Django 3.0.8 on 2020-07-25 08:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_watchlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('id_listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listCom', to='auctions.Listings')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userCom', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
