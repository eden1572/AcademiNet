# Generated by Django 5.0.3 on 2024-04-08 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0031_studygroups_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='department_choices',
            field=models.CharField(choices=[('program', 'Software Engineering'), ('machines', 'Mechanical Engineering'), ('electrical', 'Electrical Engineering'), ('architectural', 'Architecture'), ('structural', 'Structural Engineering'), ('industrial', 'Industrial Engineering'), ('comp_science', 'Computer science'), ('Chemical', 'Chemical Engineering')], default='tech', max_length=20),
        ),
        migrations.AlterField(
            model_name='studygroups',
            name='division',
            field=models.CharField(choices=[('program', 'Software Engineering'), ('machines', 'Mechanical Engineering'), ('electrical', 'Electrical Engineering'), ('architectural', 'Architecture'), ('structural', 'Structural Engineering'), ('industrial', 'Industrial Engineering'), ('comp_science', 'Computer science'), ('Chemical', 'Chemical Engineering')], max_length=100),
        ),
    ]
