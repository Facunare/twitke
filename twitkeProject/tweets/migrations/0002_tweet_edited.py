# Generated by Django 4.1.7 on 2023-04-30 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='edited',
            field=models.BooleanField(default=False),
        ),
    ]
