# Generated by Django 3.0.2 on 2020-01-28 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagepost',
            name='gmt_create',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
