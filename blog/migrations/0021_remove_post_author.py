# Generated by Django 5.0.2 on 2024-03-24 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_alter_post_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
    ]