from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm, OwnerProfileForm
from properties.models import Owner

def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Sua conta foi criada com sucesso! Por favor, complete seu perfil.')
            return redirect('accounts:complete_owner_profile')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def complete_owner_profile(request):
    try:
        owner = request.user.owner_profile
    except Owner.DoesNotExist:
        owner = None

    if request.method == 'POST':
        form = OwnerProfileForm(request.POST, instance=owner)
        if form.is_valid():
            owner = form.save(commit=False)
            owner.user = request.user
            owner.name = request.user.first_name 
            owner.email = request.user.email
            owner.save()
            messages.success(request,'Seu perfil foi atualizado com sucesso!')
            return redirect('core:home')
        else:
            messages.error(request, 'Erro ao atualizar seu perfil. Verifique os dados.')
    else:
        form = OwnerProfileForm(instance=owner)

    return render(request, 'core/complete_owner.html', {'form': form})

