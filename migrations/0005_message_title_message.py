# Generated by Django 5.0.3 on 2024-04-07 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0004_message_file_sumbit_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='title_message',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
