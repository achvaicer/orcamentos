# -*- coding: utf-8 -*-
from django.utils.timezone import now
from django import forms
# from orcamentos.crm.validate import validate_documents
# from orcamentos.utils.lists import GENDER, CUSTOMER_TYPE, PERSON_TYPE
from orcamentos.crm.models import Person, Employee, Customer

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


class SelectDateWidget(forms.SelectDateWidget):

    def create_select(self, *args, **kwargs):
        old_state = self.is_required
        self.is_required = False
        result = super().create_select(*args, **kwargs)
        self.is_required = old_state
        return result


class CustomerForm(forms.ModelForm):
    gender = forms.ChoiceField(
        label='Sexo', choices=GENDER, initial='M', widget=forms.RadioSelect)
    person_type = forms.ChoiceField(
        label='Cliente ou contato', choices=PERSON_TYPE, initial='c',
        widget=forms.RadioSelect)
    customer_type = forms.ChoiceField(
        label='Tipo', choices=CUSTOMER_TYPE, initial='p',
        widget=forms.RadioSelect)

    class Meta:
        model = Customer
        fields = ['gender', 'treatment', 'first_name', 'last_name', 'email',
                  'slug', 'photo', 'birthday', 'occupation', 'company',
                  'department', 'cpf', 'rg', 'cnpj', 'ie',
                  'address', 'complement', 'district', 'city', 'uf', 'cep',
                  'active', 'blocked', 'person_type', 'customer_type']
        widgets = {
            'birthday': SelectDateWidget
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_year = now().year
        self.fields['birthday'].widget.years = [
            current_year - x for x in range(50)][::-1]

    def clean_cpf(self):
        return self.cleaned_data['cpf'] or None

    def clean_cnpj(self):
        return self.cleaned_data['cnpj'] or None


class PersonForm(forms.ModelForm):
    gender = forms.ChoiceField(
        label='Sexo', choices=GENDER, initial='M', widget=forms.RadioSelect)
    person_type = forms.ChoiceField(
        label='Cliente ou contato', choices=PERSON_TYPE, initial='p',
        widget=forms.RadioSelect)

    class Meta:
        model = Person
        fields = ['gender', 'treatment', 'first_name', 'last_name', 'slug',
                  'photo', 'birthday', 'occupation', 'company', 'department',
                  'email', 'cpf', 'rg', 'cnpj', 'ie', 'person_type',
                  'customer_type', 'address', 'complement', 'district',
                  'city', 'uf', 'cep', 'active', 'blocked']

    def clean_cpf(self):
        return self.cleaned_data['cpf'] or None

    def clean_cnpj(self):
        return self.cleaned_data['cnpj'] or None


class EmployeeForm(forms.ModelForm):
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = ['username', 'email', 'password']

    def clean_cpf(self):
        return self.cleaned_data['cpf'] or None

    def clean_cnpj(self):
        return self.cleaned_data['cnpj'] or None


class EmployeeAdminForm(forms.ModelForm):
    gender = forms.ChoiceField(
        label='Sexo', choices=GENDER, initial='M', widget=forms.RadioSelect)

    class Meta:
        model = Employee
        fields = ['username', 'slug', 'gender', 'first_name', 'last_name',
                  'is_staff', 'email', 'photo', 'birthday', 'department',
                  'cpf', 'rg', 'occupation', 'address', 'complement',
                  'district', 'city', 'uf', 'cep', 'date_joined',
                  'date_release', 'active', 'blocked']

    def clean_cpf(self):
        return self.cleaned_data['cpf'] or None

    def clean_cnpj(self):
        return self.cleaned_data['cnpj'] or None
