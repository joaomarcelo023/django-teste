# Generated by Django 3.2.23 on 2024-03-24 02:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_cliente_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='user',
        ),
    ]
