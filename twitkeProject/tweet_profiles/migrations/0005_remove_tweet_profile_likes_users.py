# Generated by Django 4.1.7 on 2023-05-16 02:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweet_profiles', '0004_remove_tweet_profile_images_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet_profile',
            name='likes_users',
        ),
    ]
