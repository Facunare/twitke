# Generated by Django 4.1.7 on 2023-05-06 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_profiles_retweets'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiles',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
