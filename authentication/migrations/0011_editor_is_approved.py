# Generated by Django 5.0.2 on 2024-04-07 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_remove_editor_is_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='editor',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
