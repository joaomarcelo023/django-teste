# Generated by Django 4.2.16 on 2025-06-12 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0076_adminlogs'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AdminLogs',
            new_name='AdminLog',
        ),
    ]
