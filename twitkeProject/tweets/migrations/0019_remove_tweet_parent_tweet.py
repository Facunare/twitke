# Generated by Django 4.2.1 on 2023-06-05 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0018_remove_tweet_havemultimedia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='parent_tweet',
        ),
    ]
