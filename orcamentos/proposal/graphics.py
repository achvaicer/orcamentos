# -*- coding: utf-8 -*-

import json
import itertools
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse
from .models import Proposal, Contract
from orcamentos.crm.models import Customer
#from orcamentos.utils.lists import STATUS_LIST, CUSTOMER_TYPE

GENDER = [('M', 'masculino'), ('F', 'feminino')]

TREATMENT = (
    ('a', 'Arq.'),
    ('aa', 'Arqa.'),
    ('d', 'Dona'),
    ('dr', 'Dr.'),
    ('dra', 'Dra.'),
    ('e', 'Eng.'),
    ('ea', u'Engª.'),
    ('p', 'Prof.'),
    ('pa', 'Profa.'),
    ('sr', 'Sr.'),
    ('sra', 'Sra.'),
    ('srta', 'Srta.'),
)

PHONE_TYPE = (
    ('pri', 'principal'),
    ('com', 'comercial'),
    ('res', 'residencial'),
    ('cel', 'celular'),
    ('cl', 'Claro'),
    ('oi', 'Oi'),
    ('t', 'Tim'),
    ('v', 'Vivo'),
    ('n', 'Nextel'),
    ('fax', 'fax'),
    ('o', 'outros'),
)

CUSTOMER_TYPE = (
    ('c', 'construtora'),
    ('a', 'arquitetura'),
    ('p', 'particular')
)

PERSON_TYPE = (
    ('c', 'cliente'),
    ('p', 'contato'),
)

URGENTE = 'a1'
ALTA = 'a2'
NORMAL = 'a3'
BAIXA = 'a4'
PRIORITY = (
    (URGENTE, 'Urgente'),
    (ALTA, 'Alta'),
    (NORMAL, 'Normal'),
    (BAIXA, 'Baixa'),
)

PROP_TYPE = (
    ('R', 'R'),
    ('OP', 'OP')
)

STATUS_FILTER = (
    ('c', 'cancelado'),
    ('elab', 'em elaboração'),
    ('p', 'pendente'),
    ('co', 'concluido'),
    ('a', 'aprovado')
)

STATUS_LIST = (
    ('c', 'cancelado'),
    ('n', 'não iniciado'),
    ('elab', 'em elaboração'),
    ('p', 'pendente'),
    ('co', 'concluido'),
    ('a', 'aprovado')
)

CATEGORY = (
    ('orc', 'orçamento'),
    ('cc', 'concorrência'),
    ('cn', 'consulta'),
    ('ct', 'cotação'),
    ('e', 'extra'),
    ('g', 'global'),
    ('p', 'particular'),
    ('ou', 'outros'),
)

OCCUPATION_LIST = (
    u'Arquiteto',
    u'Coordenador',
    u'Diretor',
    u'Engenheiro',
    u'Estagiário',
    u'Gerente',
    u'Orçamentista',
    u'Vendedor',
)

COMPANY_LIST = (
    ('Acme'),
    ('Cyberdyne'),
    ('Ghostbusters'),
    ('Globex'),
    ('Gringotes'),
    ('ILM'),
    ('Oscorp'),
    ('RG Solutions'),
    ('Stark'),
    ('Tabajara'),
    ('Teknotronic'),
    ('Tivit'),
    ('Wayne'),
    ('Wonka'),
)


UF_LIST = (
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AM', 'Amazonas'),
    ('AP', u'Amapá'),
    ('BA', 'Bahia'),
    ('CE', u'Ceará'),
    ('DF', u'Brasília'),
    ('ES', u'Espírito Santo'),
    ('GO', u'Goiás'),
    ('MA', u'Maranhão'),
    ('MG', 'Minas Gerais'),
    ('MS', 'Mato Grosso do Sul'),
    ('MT', 'Mato Grosso'),
    ('PA', u'Pará'),
    ('PB', u'Paraíba'),
    ('PE', 'Pernambuco'),
    ('PI', u'Piauí'),
    ('PR', u'Paraná'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RO', u'Rondônia'),
    ('RR', 'Roraima'),
    ('RS', 'Rio Grande do Sul'),
    ('SC', 'Santa Catarina'),
    ('SE', 'Sergipe'),
    ('SP', u'São Paulo'),
    ('TO', 'Tocantins'),
)


STATUS_DICT = dict(STATUS_LIST)
CUSTOMER_DICT = dict(CUSTOMER_TYPE)


def proposal_per_status_json(request):
    ''' JSON used to generate the graphic '''
    ''' Quantidade de orçamentos por status '''
    data = Proposal.objects.values('status')\
        .annotate(value=Count('status'))\
        .order_by('status').values('status', 'value')
    '''
    Precisa reescrever o dicionário com os campos do gráfico,
    que são: 'label' e 'value'. E ainda retornar o get_status_display.
    '''
    lista = [{'label': STATUS_DICT[item['status']],
              'value': item['value']} for item in data]
    s = json.dumps(lista, cls=DjangoJSONEncoder)
    return HttpResponse(s)


def count_contract_aproved():
    return Contract.objects.filter(is_canceled=False).count()


def get_data(is_aproved, is_canceled):
    data = [{'label': 'Aprovados', 'value': is_aproved},
            {'label': 'Cancelados', 'value': is_canceled}]
    return data


def contract_aprov_canceled_json(request):
    ''' JSON used to generate the graphic '''
    ''' Quantidade de contratos aprovados x cancelados '''
    total = Contract.objects.count()
    is_aproved = count_contract_aproved()
    is_canceled = total - is_aproved
    resp = JsonResponse(get_data(is_aproved, is_canceled), safe=False)
    return HttpResponse(resp.content)


def contract_more_expensive_json(request):
    ''' 5 contratos mais caros '''
    c = Contract.objects.all().values(
        'proposal__work__name_work',
        'proposal__price').order_by('-proposal__price')[:5]
    s = json.dumps(list(c), cls=DjangoJSONEncoder)
    return HttpResponse(s)


def contract_total_per_month_json(request):
    ''' valor total fechado por mês no ano '''
    c = Contract.objects.all().values('created', 'proposal__price') \
        .filter(is_canceled=False)
    gr = itertools.groupby(c, lambda d: d.get('created').strftime('%Y-%m'))
    dt = [{'month': month, 'total': sum(
        [x['proposal__price'] for x in total])} for month, total in gr]
    s = json.dumps(list(dt), cls=DjangoJSONEncoder)
    return HttpResponse(s)


def percent_type_customer_json(request):
    ''' Porcentagem de tipos de clientes '''
    data = Customer.objects.values('customer_type')\
        .annotate(value=Count('customer_type'))\
        .order_by('customer_type').values('customer_type', 'value')
    total = Customer.objects.all().count()
    '''
    Precisa reescrever o dicionário com os campos do gráfico,
    que são: 'label' e 'value'. E ainda retornar o get_customer_type_display.
    '''
    lista = [{'label': CUSTOMER_DICT[item['customer_type']],
              'value': int((item['value'] / total) * 100)} for item in data]
    s = json.dumps(lista, cls=DjangoJSONEncoder)
    print(s)
    return HttpResponse(s)
