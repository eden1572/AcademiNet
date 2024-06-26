# Generated by Django 5.0.2 on 2024-03-28 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboardlink',
            name='name',
            field=models.CharField(default='Default Name', max_length=100, verbose_name='Link Name'),
        ),
        migrations.AddField(
            model_name='dashboardlink',
            name='url',
            field=models.URLField(default='https://example.com', verbose_name='Link URL'),
        ),
    ]
