# Generated by Django 4.2.1 on 2023-06-07 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0013_unbanrequests'),
    ]

    operations = [
        migrations.AddField(
            model_name='unbanrequests',
            name='reason',
            field=models.TextField(blank=True, default='', max_length=250, null=True),
        ),
    ]