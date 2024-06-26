# Generated by Django 5.0.3 on 2024-04-09 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0035_rename_isright_post_isbenefits_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='isbenefits',
            new_name='isevents',
        ),
        migrations.AddField(
            model_name='post',
            name='islectures',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='isworkshops',
            field=models.BooleanField(default=False),
        ),
    ]
