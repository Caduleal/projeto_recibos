from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required # is_locador/user_passes_test já no seu utils ou views
from django.contrib import messages
from .models import Payment 
from .forms import PaymentForm 
@login_required
def payment_list(request):
    payments = Payment.objects.filter(owner=request.user).order_by('-payment_date', '-reference_period')
    context = {
        'payments': payments,
        'page_title': 'Lista de Pagamentos',
    }
    return render(request, 'rental_app/payment_list.html', context)


@login_required
def payment_create(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.owner = request.user
            payment.save()
            messages.success(request, 'Pagamento registrado com sucesso!')
            return redirect('rental_app:payment_list')
        else:
            messages.error(request, 'Houve um erro ao registrar o pagamento. Verifique os dados.')
    else:
        form = PaymentForm(user=request.user) 

    context = {
        'form': form,
        'page_title': 'Registrar Novo Pagamento',
    }
    return render(request, 'rental_app/payment_form.html', context)


@login_required
def payment_update(request, pk):
    payment = get_object_or_404(Payment, pk=pk, owner=request.user) 
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES, instance=payment, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pagamento atualizado com sucesso!')
            return redirect('rental_app:payment_list')
        else:
            messages.error(request, 'Houve um erro ao atualizar o pagamento. Verifique os dados.')
    else:
        form = PaymentForm(instance=payment, user=request.user)

    context = {
        'form': form,
        'page_title': 'Editar Pagamento',
    }
    return render(request, 'rental_app/payment_form.html', context)


@login_required
def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk, owner=request.user)
    if request.method == 'POST':
        payment.delete()
        messages.success(request, 'Pagamento excluído com sucesso!')
        return redirect('rental_app:payment_list')
    return redirect('rental_app:payment_list') 
