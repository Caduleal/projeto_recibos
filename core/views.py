from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import CustomUserCreationForm, OwnerProfileForm
from .forms import CustomUserCreationForm, OwnerProfileForm
from properties.models import Owner
from django.contrib import messages

@login_required
def home(request):
    return render(request, 'core/home.html')

def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:complete_owner_profile')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def complete_owner_profile(request):
    try:
        owner = request.user.owner_profile
    except Owner.DoesNotExist:
        owner = Owner.objects.create(user=request.user)

    if request.method == 'POST':
        form = OwnerProfileForm(request.POST, instance=owner) 
        if form.is_valid():
            form.save()
            messages.success(request,'Seu Perfil foi atualizado com sucesso!')

        return redirect('core:home')
    else:
        form = OwnerProfileForm(instance=owner)

    return render(request, 'core/complete_owner.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        owner_form = OwnerProfileForm(request.POST)
        if user_form.is_valid() and owner_form.is_valid():
            user = user_form.save()

            owner = owner_form.save(commit=False)
            owner.user = user
            owner.save()

            login(request,user)
            return redirect('core/home.html')
    else:
        user_form = CustomUserCreationForm()
        owner_form = OwnerProfileForm()

        context = {
            'user_form': user_form,
            'owner_form': owner_form,
        }
    return render(request,'registration/register.html',context)