from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm, OwnerProfileForm
from .forms import UserUpdateForm
from properties.models import Owner
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse

def settings_view_page(request):
    return render(request, 'core/settings.html')

def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Sua conta foi criada com sucesso! Por favor, complete seu perfil.')
            return redirect('accounts:complete_owner_profile')
        else:
            print("Formulário inválido")
            print(form.errors)
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

@login_required
def settings_view(request):
    user = request.user
    owner_instance = None
    try:
        owner_instance = user.owner_profile
    except ObjectDoesNotExist:
        pass

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        owner_form = OwnerProfileForm(request.POST, instance=owner_instance)

        if user_form.is_valid() and owner_form.is_valid():
            user_form.save()
            if owner_instance is None:
                owner_obj = owner_form.save(commit=False)
                owner_obj.user = user 
            else:
                owner_obj = owner_form.save(commit=False) 
            owner_obj.name = f"{user.first_name} {user.last_name}".strip()

            owner_obj.email = user.email

            owner_obj.save()

            messages.success(request, 'Suas configurações foram atualizadas com sucesso!')
            return redirect('settings') 
        else:
            messages.error(request, 'Houve um erro ao atualizar suas configurações. Verifique os dados.')
    else:
        user_form = UserUpdateForm(instance=user)
        owner_form = OwnerProfileForm(instance=owner_instance)

    context = {
        'user_form': user_form,
        'owner_form': owner_form,
        'page_title': 'Configurações de Perfil',
        'is_new_owner': owner_instance is None, 
    }
    return render(request, 'core/settings.html', context)

def password_reset_local(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_url = reverse('accounts:password_reset_confirm', kwargs={
                'uidb64': uid,
                'token': token
            })
            return redirect(reset_url)

        except User.DoesNotExist:
            return render(request, 'registration/password_reset_form.html', {
                'error': 'E-mail não encontrado.'
            })

    return render(request, 'registration/password_reset_form.html')

def password_reset_complete_local(request):
    return render(request, 'registration/password_reset_complete.html')