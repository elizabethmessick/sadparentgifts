# Generated by Django 2.1.2 on 2018-10-18 16:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gift',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='gift',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gift',
            name='photo_url',
            field=models.CharField(max_length=150),
        ),
    ]