# Generated by Django 4.2.3 on 2023-07-17 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_customuser_otp_alter_customuser_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_user',
            field=models.BooleanField(default=False),
        ),
    ]
