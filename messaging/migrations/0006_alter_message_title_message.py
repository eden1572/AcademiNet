# Generated by Django 5.0.3 on 2024-04-07 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0005_message_title_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='title_message',
            field=models.CharField(choices=[('User Error', 'User Error'), ('Forum Problem', 'Forum Problem'), ('Rights and Benefits', 'Rights and Benefits'), ('Other', 'Other')], max_length=100, null=True),
        ),
    ]
