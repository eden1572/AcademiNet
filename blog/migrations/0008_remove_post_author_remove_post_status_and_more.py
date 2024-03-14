# Generated by Django 5.0.2 on 2024-03-14 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_post_header_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.RemoveField(
            model_name='post',
            name='status',
        ),
        migrations.RemoveField(
            model_name='post',
            name='updated_on',
        ),
        migrations.AddField(
            model_name='post',
            name='department_choices',
            field=models.CharField(choices=[('program', 'Program'), ('machines', 'Machines'), ('electrical', 'Electrical'), ('architectural', 'Architectural'), ('structural', 'Structural'), ('industrial', 'Industrial'), ('comp_science', 'Computer Science')], default='tech', max_length=20),
        ),
    ]