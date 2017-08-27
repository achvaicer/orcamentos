# -*- coding: utf-8 -*-
from django.db import models
from django.shortcuts import resolve_url as r
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from orcamentos.core.models import TimeStampedModel, Address
from .managers import CustomerManager, PersonManager, SellerManager

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



class People(TimeStampedModel, Address):
    gender = models.CharField(u'gênero', max_length=1,
                              choices=GENDER, blank=True)
    treatment = models.CharField(
        'tratamento', max_length=4, choices=TREATMENT, null=True, blank=True)
    slug = models.SlugField('slug', blank=True)
    photo = models.URLField('foto', null=True, blank=True)
    birthday = models.DateTimeField('nascimento', null=True, blank=True)
    company = models.CharField('empresa', max_length=50, null=True, blank=True)
    department = models.CharField('departamento', max_length=50, blank=True)
    cpf = models.CharField('CPF', max_length=11,
                           unique=True, null=True, blank=True)
    rg = models.CharField('RG', max_length=11, null=True, blank=True)
    cnpj = models.CharField('CNPJ', max_length=14,
                            unique=True, null=True, blank=True)
    ie = models.CharField(u'inscrição estadual',
                          max_length=12, null=True, blank=True)
    active = models.BooleanField('ativo', default=True)
    blocked = models.BooleanField('bloqueado', default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return ' '.join(filter(None, [self.get_treatment_display(), self.first_name, self.last_name]))

    full_name = property(__str__)


class Person(People):
    first_name = models.CharField('nome', max_length=50)
    last_name = models.CharField(
        'sobrenome', max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    occupation = models.ForeignKey(
        'Occupation', verbose_name='cargo', related_name='person_occupation',
        null=True, blank=True)
    person_type = models.CharField(
        'cliente ou contato', max_length=1, choices=PERSON_TYPE, default='p')
    customer_type = models.CharField(
        'tipo de cliente', max_length=1, choices=CUSTOMER_TYPE, blank=True)

    objects = PersonManager()

    class Meta:
        ordering = ['first_name']
        verbose_name = 'contato'
        verbose_name_plural = 'contatos'

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return r('crm:person_detail', slug=self.slug)

    def save(self):
        self.fullname = '{} {}'.format(self.first_name, self.last_name)
        self.slug = slugify(self.fullname)
        super(Person, self).save()


class PhonePerson(models.Model):
    phone = models.CharField('telefone', max_length=20, blank=True)
    person = models.ForeignKey('Person')
    phone_type = models.CharField(
        'tipo', max_length=3, choices=PHONE_TYPE, default='pri')


class Customer(Person):
    objects = CustomerManager()

    class Meta:
        proxy = True
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'

    def get_absolute_url(self):
        return r('crm:customer_detail', slug=self.slug)


class Employee(People, User):
    occupation = models.ForeignKey(
        'Occupation', verbose_name='cargo', related_name='employee_occupation',
        null=True, blank=True)
    internal = models.BooleanField('interno', default=True)
    commissioned = models.BooleanField('comissionado', default=True)
    commission = models.DecimalField(
        u'comissão', max_digits=6, decimal_places=2, default=0.01)
    date_release = models.DateTimeField(
        u'data de saída', null=True, blank=True)

    class Meta:
        ordering = ['username']
        verbose_name = u'funcionário'
        verbose_name_plural = u'funcionários'


class PhoneEmployee(models.Model):
    phone = models.CharField('telefone', max_length=20, blank=True)
    employee = models.ForeignKey('Employee')
    phone_type = models.CharField(
        'tipo', max_length=3, choices=PHONE_TYPE, default='pri')


class Occupation(models.Model):
    occupation = models.CharField('cargo', max_length=50, unique=True)

    class Meta:
        ordering = ['occupation']
        verbose_name = 'cargo'
        verbose_name_plural = 'cargos'

    def __str__(self):
        return self.occupation


class Seller(Employee):
    objects = SellerManager()

    class Meta:
        proxy = True
        verbose_name = 'vendedor'
        verbose_name_plural = 'vendedores'
