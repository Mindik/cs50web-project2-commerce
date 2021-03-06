# Generated by Django 3.0.8 on 2020-07-25 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_listings_win'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['cat']},
        ),
        migrations.AlterModelOptions(
            name='comments',
            options={'ordering': ['-create_date']},
        ),
        migrations.AlterModelOptions(
            name='listings',
            options={'ordering': ['-create_date']},
        ),
        migrations.AddField(
            model_name='comments',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, default='2020-07-24 22:04:39.328447+00:00'),
            preserve_default=False,
        ),
    ]
