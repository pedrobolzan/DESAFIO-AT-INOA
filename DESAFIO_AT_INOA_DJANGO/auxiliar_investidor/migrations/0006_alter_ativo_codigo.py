# Generated by Django 5.1 on 2024-08-24 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auxiliar_investidor', '0005_alter_cotacao_preco_negocio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ativo',
            name='codigo',
            field=models.CharField(max_length=7),
        ),
    ]
