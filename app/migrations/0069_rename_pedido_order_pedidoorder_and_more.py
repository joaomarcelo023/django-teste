# Generated by Django 4.2.16 on 2025-04-30 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0068_remove_pedido_order_ordenado_por'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Pedido_order',
            new_name='PedidoOrder',
        ),
        migrations.RenameModel(
            old_name='Pedido_Produto',
            new_name='PedidoProduto',
        ),
    ]
