# Generated by Django 4.1.7 on 2023-05-26 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0014_alter_tweetimage_tweet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweetimage',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='tweetImages'),
        ),
    ]