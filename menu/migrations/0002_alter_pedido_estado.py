# Generated by Django 5.1.5 on 2025-03-28 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='estado',
            field=models.CharField(choices=[('confirmacion', 'En confirmación'), ('preparacion', 'En preparación'), ('entregado', 'Entregado'), ('cancelado', 'Cancelado')], default='confirmacion', max_length=15),
        ),
    ]
