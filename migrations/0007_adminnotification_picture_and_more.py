# Generated by Django 5.0.2 on 2024-04-05 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_rename_is_read_adminnotification_is_treated'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminnotification',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='pictures/'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
        migrations.AlterField(
            model_name='editor',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
    ]
