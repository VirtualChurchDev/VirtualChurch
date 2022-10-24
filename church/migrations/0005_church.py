# Generated by Django 4.1.1 on 2022-10-09 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('church', '0004_alter_news_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Church',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('foto', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=2000)),
                ('tour', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Churches',
            },
        ),
    ]