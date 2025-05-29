from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .forms import CustomUserCreationForm, OwnerProfileForm
from properties.models import Owner

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
    
    return render(request, 'core/register_user.html', {'form': form})

@login_required
def complete_owner_profile(request):
    try:
        owner = request.user.owner_profile
    except Owner.DoesNotExist:
        owner = None

    if request.method == 'POST':
        form = OwnerProfileForm(request.POST, instance=owner) 
        if form.is_valid():
            owner_instance = form.save(commit=False)
            owner_instance.user = request.user
        owner_instance.save() # 
        return redirect('core:home')
    else:
        form = OwnerProfileForm(instance=owner)

    return render(request, 'core/complete_owner.html', {'form': form})
