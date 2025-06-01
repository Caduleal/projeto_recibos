from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Property 
from .forms import PropertyForm 
from .models import Owner
@login_required

def property_list(request):
    owner = request.user.owner_profile   
    properties = Property.objects.filter(owner=owner).order_by('address')
    context = {
        'properties': properties,
        'page_title': 'Lista de Imóveis',
    }
    return render(request, 'core/property_list.html', context)


@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property_obj = form.save(commit=False) 
            property_obj.owner = Owner.objects.get(user=request.user) 
            property_obj.save()
            messages.success(request, 'Imóvel cadastrado com sucesso!')
            return redirect('Properties:property_list')
        else:
            messages.error(request, 'Houve um erro ao cadastrar o imóvel. Verifique os dados.')
    else:
        form = PropertyForm()

    context = {
        'form': form,
        'page_title': 'Cadastrar Novo Imóvel',
    }
    return render(request, 'core/property_form.html', context)


@login_required
def property_update(request,pk):
    property_obj = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Imóvel atualizado com sucesso!')
            return redirect('Properties:property_list')
        else:
            messages.error(request, 'Houve um erro ao atualizar o imóvel. Verifique os dados.')
    else:
        form = PropertyForm(instance=property_obj)

    context = {
        'form': form,
        'page_title': 'Editar Imóvel',
    }
    return render(request,'core/property_form.html',context)


@login_required
def property_delete(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)

    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, 'Imóvel excluído com sucesso!')
        return redirect('Properties:property_list')

    context = {
        'property': property_obj, 
        'page_title': 'Confirmar Exclusão',
    }
    return render(request, 'core/property_confirm_delete.html', context)

