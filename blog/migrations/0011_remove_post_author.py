# Generated by Django 5.0.2 on 2024-03-12 23:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_delete_choices'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
    ]
