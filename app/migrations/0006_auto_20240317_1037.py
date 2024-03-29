# Generated by Django 3.2.23 on 2024-03-17 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_encarte'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produto',
            name='preco_mercado',
        ),
        migrations.AddField(
            model_name='produto',
            name='fechamento_embalagem',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='produto',
            name='unidade',
            field=models.CharField(default='un', max_length=30),
        ),
        migrations.AlterField(
            model_name='produto',
            name='venda',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
