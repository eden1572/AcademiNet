# Generated by Django 5.0.3 on 2024-04-09 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0036_rename_isbenefits_post_isevents_post_islectures_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='isevents',
            new_name='isbenefits',
        ),
        migrations.RemoveField(
            model_name='post',
            name='islectures',
        ),
        migrations.RemoveField(
            model_name='post',
            name='isworkshops',
        ),
        migrations.AddField(
            model_name='post',
            name='benefits_choices',
            field=models.CharField(choices=[('Events', 'Events'), ('workshops', 'workshops'), ('Lectures', 'Lectures')], max_length=100, null=True),
        ),
    ]
