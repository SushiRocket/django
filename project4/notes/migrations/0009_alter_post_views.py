# Generated by Django 5.1.2 on 2024-11-26 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0008_post_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='views',
            field=models.PositiveIntegerField(default=1),
        ),
    ]