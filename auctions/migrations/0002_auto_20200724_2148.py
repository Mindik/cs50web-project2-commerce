# Generated by Django 3.0.8 on 2020-07-24 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_in_school', models.CharField(choices=[('AA', 'Freshman'), ('BB', 'Sophomore'), ('CC', 'Junior'), ('DD', 'Senior')], default='AA', max_length=2)),
            ],
        ),
        migrations.RemoveField(
            model_name='listings',
            name='category',
        ),
        migrations.AddField(
            model_name='listings',
            name='category',
            field=models.ManyToManyField(related_name='category', to='auctions.Category'),
        ),
    ]
