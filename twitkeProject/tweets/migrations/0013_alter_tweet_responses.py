# Generated by Django 4.1.7 on 2023-05-20 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0012_tweet_responses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='responses',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
