# Generated by Django 5.0.2 on 2024-04-07 04:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_useractionlog'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserActionLog',
        ),
    ]
