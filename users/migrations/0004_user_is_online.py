# Generated by Django 5.0.11 on 2025-03-23 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_bio_alter_user_birthday_alter_user_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_online',
            field=models.BooleanField(default=False, verbose_name='En ligne'),
        ),
    ]
