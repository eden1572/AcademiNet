# Generated by Django 5.0.3 on 2024-04-09 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0040_post_author_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='isanonymous',
            field=models.BooleanField(default=False),
        ),
    ]
