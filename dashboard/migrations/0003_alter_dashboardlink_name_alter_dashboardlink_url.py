# Generated by Django 5.0.2 on 2024-03-28 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_dashboardlink_name_dashboardlink_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboardlink',
            name='name',
            field=models.CharField(default='Default Name', max_length=100),
        ),
        migrations.AlterField(
            model_name='dashboardlink',
            name='url',
            field=models.URLField(default='https://example.com'),
        ),
    ]
