# Generated by Django 4.2.7 on 2023-11-28 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
    ]
