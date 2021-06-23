# Generated by Django 3.2.4 on 2021-06-06 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0002_alter_skill_competency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='competency',
            field=models.CharField(choices=[(1, 'python'), (2, 'java'), (3, 'js'), (4, '.net')], max_length=200),
        ),
    ]
