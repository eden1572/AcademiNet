# Generated by Django 5.0.3 on 2024-04-06 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0026_comment_file_comment_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='Topic_choice',
            field=models.CharField(choices=[('summaries', 'Summaries'), ('Help with the educational material', 'Help with the educational material'), ('Study Groups', 'Study Groups')], max_length=100, null=True),
        ),
    ]
