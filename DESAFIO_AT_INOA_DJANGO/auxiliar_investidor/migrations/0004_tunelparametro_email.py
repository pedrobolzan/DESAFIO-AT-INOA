# Generated by Django 5.1 on 2024-08-23 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auxiliar_investidor', '0003_remove_cotacao_quantidade_negociada'),
    ]

    operations = [
        migrations.AddField(
            model_name='tunelparametro',
            name='email',
            field=models.EmailField(default='pedrobolzan12345@gmail.com', help_text='Informe seu e-mail para receber alertas', max_length=254),
        ),
    ]
