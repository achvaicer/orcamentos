# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-08-27 01:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='category',
            field=models.CharField(choices=[(b'orc', b'or\xc3\xa7amento'), (b'cc', b'concorr\xc3\xaancia'), (b'cn', b'consulta'), (b'ct', b'cota\xc3\xa7\xc3\xa3o'), (b'e', b'extra'), (b'g', b'global'), (b'p', b'particular'), (b'ou', b'outros')], default=b'orc', max_length=4, verbose_name=b'categoria'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='created_orc',
            field=models.DateTimeField(blank=True, null=True, verbose_name=b'or\xc3\xa7. criado em'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='status',
            field=models.CharField(choices=[(b'c', b'cancelado'), (b'n', b'n\xc3\xa3o iniciado'), (b'elab', b'em elabora\xc3\xa7\xc3\xa3o'), (b'p', b'pendente'), (b'co', b'concluido'), (b'a', b'aprovado')], default=b'elab', max_length=4),
        ),
        migrations.AlterField(
            model_name='work',
            name='uf',
            field=models.CharField(blank=True, choices=[(b'AC', b'Acre'), (b'AL', b'Alagoas'), (b'AP', b'Amap\xc3\xa1'), (b'AM', b'Amazonas'), (b'BA', b'Bahia'), (b'CE', b'Cear\xc3\xa1'), (b'DF', b'Distrito Federal'), (b'ES', b'Esp\xc3\xadrito Santo'), (b'GO', b'Goi\xc3\xa1s'), (b'MA', b'Maranh\xc3\xa3o'), (b'MT', b'Mato Grosso'), (b'MS', b'Mato Grosso do Sul'), (b'MG', b'Minas Gerais'), (b'PA', b'Par\xc3\xa1'), (b'PB', b'Para\xc3\xadba'), (b'PR', b'Paran\xc3\xa1'), (b'PE', b'Pernambuco'), (b'PI', b'Piau\xc3\xad'), (b'RJ', b'Rio de Janeiro'), (b'RN', b'Rio Grande do Norte'), (b'RS', b'Rio Grande do Sul'), (b'RO', b'Rond\xc3\xb4nia'), (b'RR', b'Roraima'), (b'SC', b'Santa Catarina'), (b'SP', b'S\xc3\xa3o Paulo'), (b'SE', b'Sergipe'), (b'TO', b'Tocantins')], max_length=2, verbose_name=b'UF'),
        ),
    ]
