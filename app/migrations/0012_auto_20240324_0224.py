# Generated by Django 3.2.23 on 2024-03-24 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_cliente_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='endereco',
            name='endereco',
        ),
        migrations.AddField(
            model_name='endereco',
            name='bairro',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='endereco',
            name='cep',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='endereco',
            name='cidade',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='endereco',
            name='numero',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='endereco',
            name='observacao',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='endereco',
            name='rua',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]