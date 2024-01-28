# Generated by Django 5.0.1 on 2024-01-28 11:49

import api.models
import django.contrib.auth.models
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('isbn', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=256)),
                ('author', models.CharField(max_length=256)),
                ('category', models.CharField(max_length=256)),
                ('pubyear', models.CharField(max_length=5)),
                ('language', models.CharField(max_length=30)),
                ('price', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=1024)),
                ('reviews', models.PositiveSmallIntegerField(default=0)),
                ('reviews_score', models.PositiveSmallIntegerField(default=0)),
                ('cover_image', models.ImageField(default='books/default.png', upload_to=api.models.upload_to)),
            ],
        ),
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('isbn', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=200, unique=True)),
                ('name', models.CharField(max_length=256)),
                ('password', models.CharField(max_length=1024)),
                ('birth_date', models.CharField(max_length=30)),
                ('avatar', models.ImageField(default='users/default_user.svg', upload_to=api.models.upload_to)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
