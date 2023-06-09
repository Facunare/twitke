# Generated by Django 4.1.7 on 2023-05-13 02:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0006_remove_tweet_is_retwitted'),
    ]

    operations = [
        migrations.CreateModel(
            name='TweetImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='tweetImages')),
                ('tweet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tweets.tweet')),
            ],
        ),
    ]
