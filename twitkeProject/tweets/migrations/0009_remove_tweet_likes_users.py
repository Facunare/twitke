# Generated by Django 4.1.7 on 2023-05-16 02:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0008_alter_tweetimage_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='likes_users',
        ),
    ]