# Generated by Django 4.2.16 on 2024-12-31 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_auto_20241231_1833'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('link', models.CharField(blank=True, max_length=200, null=True)),
                ('image', models.ImageField(upload_to='empresas')),
            ],
        ),
    ]