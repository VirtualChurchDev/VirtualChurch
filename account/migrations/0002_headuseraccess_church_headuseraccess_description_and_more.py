# Generated by Django 4.1.1 on 2022-10-16 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('church', '0005_church'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='headuseraccess',
            name='church',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='church.church'),
        ),
        migrations.AddField(
            model_name='headuseraccess',
            name='description',
            field=models.TextField(default='None', max_length=2000),
        ),
        migrations.AddField(
            model_name='headuseraccess',
            name='foto',
            field=models.CharField(default='None', max_length=255),
        ),
        migrations.AddField(
            model_name='headuseraccess',
            name='name',
            field=models.CharField(default='None', max_length=255),
        ),
        migrations.AddField(
            model_name='headuseraccess',
            name='role',
            field=models.CharField(default='None', max_length=255),
        ),
        migrations.AddField(
            model_name='headuseraccess',
            name='slug',
            field=models.SlugField(default='None', max_length=255),
        ),
        migrations.AddField(
            model_name='headuseraccess',
            name='video',
            field=models.CharField(default='None', max_length=255),
        ),
    ]
