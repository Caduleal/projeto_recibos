from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Tenant
from .forms import TenantForm

@login_required
def tenant_dashboard(request):
    tenant_obj = request.user.tenant_profile
    contracts = tenant_obj.contracts.all()
    
    all_payments = []
    for contract in contracts:
        all_payments.extend(list(contract.payments.all()))

    context = {
        'tenant': tenant_obj,
        'contracts': contracts,
        'payments': all_payments,
    }
    return render(request, 'core/tenant_list.html', context)


@login_required
def tenant_list(request):
    tenants = Tenant.objects.all().order_by('name')    
    context = {
        'tenants': tenants,
        'page_title': 'Lista de Inquilinos',
    }
    return render(request, 'core/tenant_list.html', context)


@login_required
def tenant_create(request):
    if request.method == 'POST':
        form = TenantForm(request.POST)
        if form.is_valid():
            tenant = form.save(commit=False)
            tenant.owner = request.user
            tenant.save()
            messages.success(request, 'Inquilino cadastrado com sucesso!')
            return redirect('Tenant:tenant_list')
        else:
            messages.error(request,'Houve um erro ao cadastrar o inquilino. Verifique os dados.')
    else:
        form = TenantForm()

    context = {
        'form': form,
        'page_title':'Cadastrar Novo Inquilino'
    }
    return render(request, 'core/tenant_form.html',context)


@login_required
def tenant_update(request,pk):
    tenant = get_object_or_404(Tenant,pk=pk)
    if request.method == 'POST':
        form = TenantForm(request.POST,instance=tenant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inquilino atualizado com sucesso!')
            return redirect('Tenant:tenant_list')
        else:
            messages.error(request,'Houve um erro ao atualizar o inquilino. Verifique os dados.')
    else:
        form= TenantForm(instance=tenant)

    context ={
        'form':form,
        'page_title':'Editar Inquilino',
    }
    return render(request,'core/tenant_form.html', context)


@login_required
def tenant_delete(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    if request.method == 'POST':
        tenant.delete()
        messages.success(request,'Inquilino excluído com sucesso!')
        return redirect('Tenant:tenant_list')
    context ={
        'tenant':tenant,
        'page_title':'Confirmar Exclusão',
    }
    return render(request,'core/tenant_confirm_delete.html',context)


def tenant_list_ajax(request):
    tenants = Tenant.objects.all()
    return render(request,'core/tenant_list_settings.html',{'tenants': tenants})


