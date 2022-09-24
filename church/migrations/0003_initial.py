# Generated by Django 4.1.1 on 2022-09-17 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('church', '0002_delete_news'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField(max_length=2000)),
                ('posted', models.CharField(max_length=255)),
            ],
        ),
    ]