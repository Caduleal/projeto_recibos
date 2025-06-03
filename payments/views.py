from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from .models import Payment, RentalContract
from properties.models import Owner
from .forms import PaymentForm
import calendar
from datetime import date
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT

def numero_por_extenso(valor):
    try:
        from num2words import num2words
        return num2words(valor, lang='pt_BR', to='currency').replace('euro', 'real').replace('euros', 'reais').replace('cent', 'centavo').replace('cents', 'centavos')
    except Exception:
        return f"{valor:.2f}".replace('.', ',')
    
def format_cpf_cnpj(value):
    digits = ''.join(filter(str.isdigit, str(value)))
    if len(digits) == 11:  # CPF
        return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"
    elif len(digits) == 14:  # CNPJ
        return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:]}"
    else:
        return value

@login_required
def payment_list(request):
    owner = Owner.objects.get(user=request.user)
    payments = Payment.objects.filter(contract__property__owner=owner)
    context = {
        'payments': payments,
        'page_title': 'Lista de Pagamentos',
    }
    return render(request, 'core/payment_list.html', context)


@login_required
def payment_create(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.save()
            messages.success(request, 'Pagamento registrado com sucesso!')
            return redirect('Payments:payment_list')
        else:
            messages.error(request, 'Houve um erro ao registrar o pagamento. Verifique os dados.')
    else:
        form = PaymentForm(user=request.user) 

    context = {
        'form': form,
        'page_title': 'Registrar Novo Pagamento',
    }
    return render(request, 'core/payment_form.html', context)


@login_required
def payment_update(request, pk):
    owner = get_object_or_404(Owner, user=request.user)
    payment = get_object_or_404(Payment, pk=pk, contract__property__owner=owner) 
    
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES, instance=payment, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pagamento atualizado com sucesso!')
            return redirect('Payments:payment_list')
        else:
            messages.error(request, 'Houve um erro ao atualizar o pagamento. Verifique os dados.')
    else:
        form = PaymentForm(instance=payment, user=request.user)

    context = {
        'form': form,
        'page_title': 'Editar Pagamento',
    }
    return render(request, 'core/payment_form.html', context)


@login_required
def payment_delete(request, pk):
    owner = get_object_or_404(Owner, user=request.user)
    payment = get_object_or_404(Payment, pk=pk, contract__property__owner=owner)

    payment.delete()
    messages.success(request, 'Pagamento excluído com sucesso!')
    return redirect('Payments:payment_list')

@login_required
def generate_payment_receipt_pdf(request, pk):
    payment = get_object_or_404(Payment, pk=pk)

    # Verifica se o usuário logado é o dono do imóvel
    if request.user != payment.contract.property.owner.user:
        return HttpResponseForbidden("Você não tem permissão para visualizar este recibo.")
    
    contract = payment.contract
    tenant = contract.tenant
    property_obj = contract.property
    owner_user = property_obj.owner.user
    owner_instance = property_obj.owner

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="recibo_aluguel_{str(payment.id).zfill(4)}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4,
                            rightMargin=1.5*cm, leftMargin=1.5*cm,
                            topMargin=1.5*cm, bottomMargin=1*cm)

    styles = getSampleStyleSheet()

    # Estilos personalizados
    header_title_style = ParagraphStyle(name='HeaderTitle', fontSize=18, alignment=TA_CENTER, fontName='Helvetica-Bold')
    label_style = ParagraphStyle(name='LabelStyle', fontSize=10, fontName='Helvetica-Bold')
    info_style = ParagraphStyle(name='InfoStyle', fontSize=10)
    status_styles = {
        'pago': ParagraphStyle(name='StatusOnTime', fontSize=10, fontName='Helvetica-Bold', textColor=colors.green),
        'atrasado': ParagraphStyle(name='StatusDelayed', fontSize=10, fontName='Helvetica-Bold', textColor=colors.red),
        'parcial': ParagraphStyle(name='StatusPartial', fontSize=10, fontName='Helvetica-Bold', textColor=colors.orange),
        'pendente': ParagraphStyle(name='StatusPending', fontSize=10, fontName='Helvetica-Bold', textColor=colors.grey),
    }
    footer_style = ParagraphStyle(name='FooterStyle', fontSize=9, alignment=TA_CENTER)
    small_footer_style = ParagraphStyle(name='SmallFooter', fontSize=7, alignment=TA_CENTER, textColor=colors.grey)
    total_label_style = ParagraphStyle(name='TotalLabelStyle', fontSize=12, fontName='Helvetica-Bold')
    total_info_style = ParagraphStyle(name='TotalInfoStyle', fontSize=12, fontName='Helvetica-Bold', alignment=TA_RIGHT)
    extenso_style = ParagraphStyle(name='ExtensoStyle', fontSize=10, spaceBefore=4)
    receipt_num_style = ParagraphStyle(name='ReceiptNumStyle', fontSize=10, alignment=TA_RIGHT)

    elements = []

    # Cabeçalho
    elements.append(Paragraph("RECIBO DE ALUGUEL", header_title_style))
    elements.append(Paragraph(f"Nº: {str(payment.id).zfill(4)}", receipt_num_style))
    elements.append(Spacer(1, 0.4*cm))

    # Dados do Locador
    locador_data = [
        [Paragraph("Nome:", label_style), Paragraph(owner_user.get_full_name() or owner_user.username, info_style)],
        [Paragraph("CPF:", label_style), Paragraph(format_cpf_cnpj(owner_instance.cpf_cnpj) if hasattr(owner_instance, 'cpf_cnpj') and owner_instance.cpf_cnpj else '[CPF não informado]', info_style)],
    ]
    elements.append(Table(locador_data, colWidths=[3.5*cm, doc.width - 3.5*cm],
                        style=[('VALIGN', (0,0), (-1,-1), 'TOP')]))
    elements.append(Spacer(1, 0.3*cm))

    # Linha separadora
    elements.append(Table([[None]], colWidths=[doc.width], style=[('LINEBELOW', (0,0), (-1,0), 0.5, colors.lightgrey)]))
    elements.append(Spacer(1, 0.3*cm))

    # Dados do Locatário
    locatario_data = [
        [Paragraph("Nome:", label_style), Paragraph(tenant.name, info_style)],
        [Paragraph("CPF:", label_style), Paragraph(tenant.cpf or "[Inserir CPF do Locatário]", info_style)],
    ]
    elements.append(Table(locatario_data, colWidths=[3.5*cm, doc.width - 3.5*cm],
                        style=[('VALIGN', (0,0), (-1,-1), 'TOP')]))
    elements.append(Spacer(1, 0.3*cm))

    # Linha separadora
    elements.append(Table([[None]], colWidths=[doc.width], style=[('LINEBELOW', (0,0), (-1,0), 0.5, colors.lightgrey)]))
    elements.append(Spacer(1, 0.3*cm))

    # Imóvel e pagamento
    imovel_description = property_obj.description or "Nenhuma descrição disponível."
    formatted_period_display = f"{payment.reference_month:02d}/{payment.reference_year}"
    try:
        last_day = calendar.monthrange(payment.reference_year, payment.reference_month)[1]
        due_day = min(contract.due_day, last_day)
        formatted_due_date = date(payment.reference_year, payment.reference_month, due_day).strftime("%d/%m/%Y")
    except Exception:
        formatted_due_date = f"Dia {contract.due_day} de cada mês"

    # Usa o método get_payment_status() para determinar status do pagamento
    status_info = payment.get_payment_status()
    status_text = status_info.get('text', 'Status Indisponível')
    # Ajuste o estilo de acordo com a chave do status (mapeie 'style_key' para seu dict)
    status_key = status_info.get('style_key', '')

    # Mapeia estilo do status para os estilos definidos
    style_mapping = {
        'status_on_time': status_styles['pago'],
        'status_delayed': status_styles['atrasado'],
        'status_invalid': info_style,
    }
    status_style = style_mapping.get(status_key, info_style)

    imovel_data = [
        [Paragraph("Tipo:", label_style), Paragraph(property_obj.get_property_type_display(), info_style)],
        [Paragraph("Endereço:", label_style), Paragraph(f"{property_obj.address}, {property_obj.city} - {property_obj.state} {property_obj.zip_code or ''}", info_style)],
        [Paragraph("Descrição:", label_style), Paragraph(imovel_description, info_style)],
        [Paragraph("Valor Aluguel:", label_style), Paragraph(f"R$ {contract.rent_amount:.2f}", info_style)],
        [Paragraph("Referente ao período:", label_style), Paragraph(formatted_period_display, info_style)],
        [Paragraph("Vencimento:", label_style), Paragraph(formatted_due_date, info_style)],
        [Paragraph("Status do Pagamento:", label_style), Paragraph(status_text, status_style)],
    ]
    elements.append(Table(imovel_data, colWidths=[3.5*cm, doc.width - 3.5*cm],
                        style=[('VALIGN', (0,0), (-1,-1), 'TOP')]))
    elements.append(Spacer(1, 0.3*cm))

    # Total
    total = payment.amount_paid
    total_data = [[Paragraph("TOTAL:", total_label_style), Paragraph(f"R$ {total:.2f}", total_info_style)]]
    elements.append(Table(total_data, colWidths=[doc.width - 3.5*cm, 3.5*cm]))
    elements.append(Paragraph(f"({numero_por_extenso(total)})", extenso_style))
    elements.append(Spacer(1, 0.5*cm))

    # Observação final
    elements.append(Paragraph(f"Recebemos de {tenant.name} o valor de R$ {total:.2f} referente ao aluguel do imóvel localizado em {property_obj.address}, {property_obj.city}.", info_style))
    elements.append(Spacer(1, 0.5*cm))

    meses_pt = {1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho",
                7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}
    data_formatada_pt = f"{payment.payment_date.day} de {meses_pt[payment.payment_date.month]} de {payment.payment_date.year}"
    elements.append(Paragraph(f"Recebido em: {data_formatada_pt}.", info_style))
    elements.append(Spacer(1, 1.5*cm))

    # Assinatura
    elements.append(Paragraph("___________________________________", footer_style))
    elements.append(Paragraph(f"Assinatura do Locador ({owner_user.get_full_name() or owner_user.username})", footer_style))
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph("Este recibo é gerado eletronicamente e não necessita de assinatura física.", small_footer_style))

    doc.build(elements)
    return response