# Generated by Django 2.1.2 on 2018-10-13 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='gift',
        ),
        migrations.DeleteModel(
            name='Photo',
        ),
    ]
