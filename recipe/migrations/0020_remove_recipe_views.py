# Generated by Django 4.2.3 on 2023-08-08 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0019_alter_notifications_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='views',
        ),
    ]
