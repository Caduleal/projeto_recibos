from django.shortcuts import render 
from django.contrib.auth.decorators import login_required 

@login_required
def home(request):
    """
    Esta é a única view que deve permanecer em core/views.py.
    """
    return render(request, 'core/home.html')