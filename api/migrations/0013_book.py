# Generated by Django 4.2.7 on 2023-12-28 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_remove_user_is_staff'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('isbn', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=256)),
                ('author', models.CharField(max_length=256)),
                ('category', models.CharField(max_length=256)),
                ('year', models.CharField(max_length=5)),
                ('language', models.CharField(max_length=30)),
                ('price', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=1024)),
                ('reviews', models.IntegerField()),
                ('reviews_score', models.FloatField()),
            ],
        ),
    ]
