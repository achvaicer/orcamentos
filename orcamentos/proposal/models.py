# -*- coding: utf-8 -*-

from django.db import models
from django.shortcuts import resolve_url as r
from django.template.defaultfilters import slugify
from django.utils.formats import number_format
from orcamentos.core.models import TimeStampedModel, Address
from .managers import EntryManager, ProposalManager

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



class Work(Address):
    name_work = models.CharField('obra', max_length=100, unique=True)
    slug = models.SlugField('slug', blank=True)
    person = models.ForeignKey(
        'crm.Person', verbose_name='contato', related_name='work_person',
        null=True, blank=True)
    customer = models.ForeignKey(
        'crm.Customer', verbose_name='cliente', related_name='work_customer')

    class Meta:
        ordering = ['name_work']
        verbose_name = 'obra'
        verbose_name_plural = 'obras'

    def __str__(self):
        return self.name_work

    def get_absolute_url(self):
        if self.slug:
            return r('proposal:work_detail', slug=self.slug)

    def save(self):
        self.slug = slugify(self.name_work)
        super(Work, self).save()


class Proposal(TimeStampedModel):
    ''' Orçamento é todo orçamento com num_prop > 0 '''
    num_prop = models.PositiveIntegerField(u'número', default=0)
    priority = models.CharField(
        'prioridade', max_length=2, choices=PRIORITY, default=NORMAL)
    prop_type = models.CharField(
        u'tipo de orçamento', max_length=20, choices=PROP_TYPE, default='R')
    num_prop_type = models.PositiveIntegerField(
        u'número da revisão', default=0)
    category = models.CharField(
        'categoria', max_length=4, choices=CATEGORY, default='orc')
    description = models.TextField(u'descrição', blank=True)
    work = models.ForeignKey(
        'Work', verbose_name='obra', related_name='proposal_work')
    person = models.ForeignKey(
        'crm.Person', verbose_name='contato', related_name='proposal_person',
        null=True, blank=True)
    employee = models.ForeignKey(
        'crm.Employee', verbose_name=u'orçamentista',
        related_name='proposal_employee', null=True, blank=True)
    seller = models.ForeignKey(
        'crm.Seller', verbose_name='vendedor', related_name='proposal_seller',
        null=True, blank=True)
    status = models.CharField(
        max_length=4, choices=STATUS_LIST, default='elab')
    date_conclusion = models.DateTimeField(
        u'data de conclusão', null=True, blank=True)
    price = models.DecimalField(
        'valor', max_digits=9, decimal_places=2, default=0)
    obs = models.TextField(u'observação', blank=True)
    created_orc = models.DateTimeField('orç. criado em', null=True, blank=True)

    objects = ProposalManager()

    class Meta:
        ordering = ['id']
        verbose_name = u'orçamento'
        verbose_name_plural = u'orçamentos'

    def __str__(self):
        # formato 001.15.0
        self.actual_year = self.created.strftime('%y')
        return "%03d.%s.%d" % (self.num_prop, self.actual_year, self.num_prop_type)
    codigo = property(__str__)

    def get_absolute_url(self):
        return r('proposal:proposal_detail', pk=self.pk)

    def get_price(self):
        return u"R$ %s" % number_format(self.price, 2)

    def get_customer(self):
        return self.work.customer
    cliente = property(get_customer)

    def get_customer_url(self):
        return u'/crm/customer/%s' % self.work.customer.slug

    def get_work_url(self):
        return u'/proposal/work/%s' % self.work.slug

    def get_person_url(self):
        return u'/crm/person/%s' % self.person.slug

    def get_seller(self):
        if self.seller:
            return '{} {}'.format(self.seller.employee.first_name,
                                  self.seller.employee.last_name)
        return ''

    def get_employee(self):
        if self.employee:
            return '{} {}'.format(self.employee.first_name, self.employee.last_name)
        return ''

    def get_address(self):
        if self.work.address:
            return '{}, {}, {} - {}'.format(
                self.work.address, self.work.district,
                self.work.city, self.work.uf)


class Entry(Proposal):
    ''' Entrada é todo orçamento com num_prop = 0 '''
    objects = EntryManager()

    class Meta:
        proxy = True
        ordering = ['priority', 'created']
        verbose_name = 'entrada'
        verbose_name_plural = 'entradas'

    def __str__(self):
        return str(self.work)

    def get_absolute_url(self):
        return r('proposal:entry_detail', pk=self.pk)

    def save(self):
        self.status = 'n'  # não iniciado
        super(Entry, self).save()


class Contract(TimeStampedModel):
    proposal = models.OneToOneField(
        'Proposal', verbose_name=u'orçamento', related_name='contract_proposal')
    contractor = models.ForeignKey(
        'crm.Customer', verbose_name=u'contratante', related_name='contract_person')
    is_canceled = models.BooleanField('cancelado', default=False)

    class Meta:
        ordering = ['proposal']
        verbose_name = u'contrato'
        verbose_name_plural = u'contratos'

    def __str__(self):
        return str(self.proposal)

    def get_absolute_url(self):
        return r('proposal:contract_detail', pk=self.pk)

    def get_price(self):
        return u"R$ %s" % number_format(self.proposal.price, 2)


class NumLastProposal(models.Model):
    num_last_prop = models.PositiveIntegerField(u'número', default=0)

    class Meta:
        verbose_name = u'número último orçamento'
        verbose_name_plural = u'número último orçamento'

    def __str__(self):
        return str(self.num_last_prop)
