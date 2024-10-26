# Generated by Django 5.1.2 on 2024-10-26 11:18

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='部署名')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='日付')),
            ],
        ),
        migrations.CreateModel(
            name='Employ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20, verbose_name='名')),
                ('last_name', models.CharField(max_length=20, verbose_name='姓')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='メールアドレス')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='日付')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='employ.department', verbose_name='部署')),
            ],
        ),
    ]
