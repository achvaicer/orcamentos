from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Entry, Proposal, Contract, Employee, NumLastProposal


@login_required
def conclude_proposal(request, proposal_id):
    if request.user.is_authenticated:
        proposal = Proposal.objects.get(pk=proposal_id)
        ''' Se o status for 'aprovado', então não pode concluir '''
        if proposal.status == 'a':
            return HttpResponse('Este orçamento já virou contrato.')
        else:
            # só falta ver o formato
            v = request.POST.get('price')
            ''' verifica se o novo valor é positivo '''
            if float(v) <= 0 or float(v) is None:
                return HttpResponse('O valor deve ser positivo.')
            else:
                proposal.price = v
                proposal.status = 'co'
                proposal.date_conclusion = timezone.now()
                proposal.save()
                return redirect('/proposal/%d' % proposal.id)


@login_required
def create_proposal(request, entry_id):
    if request.user.is_authenticated:
        employee = Employee.objects.get(pk=request.user.id)
        nlp = NumLastProposal.objects.get(pk=1)  # sempre pk=1
        entry = Entry.objects.get(pk=entry_id)
        proposal = Proposal(
            num_prop=nlp.num_last_prop + 1,
            type_prop='R',
            category=entry.category,
            description=entry.description,
            work=entry.work,
            person=entry.person,
            employee=employee,
            seller=entry.seller,
        )
        proposal.save()
        ''' Define que foi dado entrada '''
        entry.is_entry = True
        entry.save()
        ''' Incrementa o número do último orçamento '''
        nlp.num_last_prop += 1
        nlp.save()
        print('Orçamento criado com sucesso')
    return redirect('/proposal/%d' % proposal.id)


@login_required
def create_contract(request, proposal_id):
    if request.user.is_authenticated:
        proposal = Proposal.objects.get(pk=proposal_id)
        ''' Se o status for diferente de 'concluído', então não faz nada '''
        if proposal.status != 'co':
            return HttpResponse('O status do orçamento deve ser concluido.')
        else:
            contractor = proposal.work.customer
            contract = Contract(
                proposal=proposal,
                contractor=contractor
            )
            contract.save()
            proposal.status = 'a'  # aprovado
            proposal.save()
    return redirect('/contract/%d' % contract.id)
