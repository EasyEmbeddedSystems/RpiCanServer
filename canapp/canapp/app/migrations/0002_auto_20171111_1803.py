# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-12 00:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensajes',
            name='transaccion_modo',
            field=models.CharField(choices=[('ENVIAR', 'Envio'), ('RECIBIR', 'Recepcion')], max_length=200),
        ),
    ]
