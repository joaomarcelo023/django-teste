# Generated by Django 4.2.16 on 2025-06-12 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0075_pedidoerro'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log', models.CharField(max_length=200)),
                ('ocorrido_em', models.DateTimeField(auto_now_add=True)),
                ('funcionario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.admin')),
            ],
        ),
    ]
