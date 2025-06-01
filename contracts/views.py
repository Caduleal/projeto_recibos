from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import RentalContract, Tenant, Property
from .forms import ContractForm
from properties.models import Owner
from django.http import HttpResponse, HttpResponseForbidden 
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from dateutil.relativedelta import relativedelta 
from datetime import date 
from num2words import num2words



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
def contract_list(request):
    try:
        current_owner_profile = request.user.owner_profile
    except Owner.DoesNotExist:
        messages.error(request, "Seu perfil de proprietário não está completo. Por favor, complete seu perfil para ver contratos.")
        return redirect('accounts:create_owner_profile') 

    contracts = RentalContract.objects.filter(owner=current_owner_profile).select_related('tenant','property').order_by('-start_date')
    context ={
        'contracts': contracts,
        'page_title':'Lista de Contratos'
    }
    return render(request,'core/contract_list.html',context)


@login_required
def contract_create(request):
    try:
        current_owner_profile = request.user.owner_profile
    except Owner.DoesNotExist:
        messages.error(request, "Seu perfil de proprietário não está completo. Por favor, complete seu perfil para cadastrar contratos.")
        return redirect('accounts:create_owner_profile') 

    if request.method =='POST':
        form = ContractForm(request.POST) 
        if form.is_valid():
            contract = form.save(commit=False)
            contract.owner = current_owner_profile 
            contract.save()
            messages.success(request,"Contrato cadastrado com sucesso!")
            return redirect('Contracts:contract_list') 

        else:
            messages.error(request,'Houve um erro ao cadastrar o contrato. Verifique os dados.')
    else:
        if request.method == 'GET':
            form = ContractForm(user=request.user)
            form.fields['tenant'].queryset = Tenant.objects.all()

            form.fields['property'].queryset = Property.objects.filter(owner=current_owner_profile)

    context = {
        'form':form,
        'page_title':'Cadastrar Novo Contrato',
    }
    return render(request, 'core/contract_form.html', context)

@login_required
def contract_update(request, pk):
    try:
        current_owner_profile = request.user.owner_profile
    except Owner.DoesNotExist:
        messages.error(request, "Seu perfil de proprietário não está completo. Por favor, complete seu perfil para atualizar contratos.")
        return redirect('accounts:create_owner_profile') 

    contract = get_object_or_404(RentalContract, pk=pk, property__owner=current_owner_profile)

    if request.method == 'POST':
        form = ContractForm(request.POST, instance=contract, user=request.user) 
        if form.is_valid():
            form.save()
            messages.success(request, 'Contrato atualizado com sucesso!')
            return redirect('Contracts:contract_list') 
        messages.error(request, 'Houve um erro ao atualizar o contrato. Verifique os dados.')
    else:
        form = ContractForm(instance=contract, user=request.user) 
        form.fields['tenant'].queryset = Tenant.objects.filter(rental_contracts__owner=current_owner_profile).distinct()
        form.fields['property'].queryset = Property.objects.filter(owner=current_owner_profile)

    context = {
        'form': form,
        'page_title': 'Editar Contrato',
    }
    return render(request, 'core/contract_form.html', context)


@login_required
def contract_delete(request, pk):
    try:
        current_owner_profile = request.user.owner_profile
    except Owner.DoesNotExist:
        messages.error(request, "Seu perfil de proprietário não está completo. Por favor, complete seu perfil para excluir contratos.")
        return redirect('accounts:create_owner_profile') 
    contract = get_object_or_404(RentalContract, pk=pk, property__owner=current_owner_profile)

    if request.method == 'POST':
        contract.delete()
        messages.success(request, 'Contrato excluído com sucesso!')
        return redirect('Contracts:contract_list')

    context = {
        'contract': contract,
        'page_title': 'Confirmar Exclusão',
    }
    return render(request, 'core/contract_confirm_delete.html', context)


@login_required
def generate_contract_pdf(request, pk):
    contract = get_object_or_404(RentalContract, pk=pk)

    is_locador = False
    is_locatario_for_this_contract = False

    try:
        if hasattr(request.user, 'owner_profile') and request.user.owner_profile == contract.property.owner:
            is_locador = True
    except Owner.DoesNotExist:
        pass

    if hasattr(contract.tenant, 'user') and contract.tenant.user == request.user:
        is_locatario_for_this_contract = True

    if not is_locador and not is_locatario_for_this_contract:
        raise HttpResponseForbidden("Você não tem permissão para visualizar este contrato. Você não é o locador associado ou o locatário deste contrato.")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="contrato_{contract.id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    elements = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(name='Title', fontSize=14, leading=18, alignment=TA_CENTER, fontName='Helvetica-Bold')
    normal_text_style = ParagraphStyle(name='NormalText', fontSize=10, leading=14, alignment=TA_JUSTIFY, spaceAfter=6)
    signature_line_style = ParagraphStyle(name='SignatureLine', fontSize=9, leading=12, alignment=TA_CENTER, spaceBefore=20)
    footer_date_style = ParagraphStyle(name='FooterDate', fontSize=9, leading=12, alignment=TA_CENTER, spaceBefore=10)


    elements.append(Paragraph("CONTRATO DE ALUGUEL", title_style))
    elements.append(Spacer(1, 0.5*cm))

    owner_instance = contract.property.owner

    locador_nome = owner_instance.user.get_full_name() or owner_instance.user.username
    locador_cpf = format_cpf_cnpj(owner_instance.cpf_cnpj) if hasattr(owner_instance, 'cpf_cnpj') and owner_instance.cpf_cnpj else ''
    
    locador_address_parts = []
    if hasattr(owner_instance, 'address') and owner_instance.address:
        locador_address_parts.append(owner_instance.address)
    if hasattr(owner_instance, 'city') and owner_instance.city:
        locador_address_parts.append(owner_instance.city)
    locador_address_full = ", ".join(locador_address_parts)
    
    locador_zip_code = getattr(owner_instance, 'zip_code', '')
    locador_state = getattr(owner_instance, 'state', '')
    locador_phone = getattr(owner_instance, 'phone_number', '')

    locador_address_line = f"residente e domiciliado a {locador_address_full}"
    if locador_zip_code:
        locador_address_line += f", C.E.P. {locador_zip_code}"
    if locador_state:
        locador_address_line += f", Estado - {locador_state}"
    if locador_phone:
        locador_address_line += f", Fone {locador_phone}"
    
    locador_info_text = f"NESTE ATO denominado(s) LOCADOR(ES) {locador_nome}, CPF {locador_cpf}, {locador_address_line}."

    elements.append(Paragraph(locador_info_text, normal_text_style))
    elements.append(Spacer(1, 0.2*cm))

    locatario_nome = contract.tenant.name
    locatario_cpf = contract.tenant.cpf or ''
    locatario_phone = getattr(contract.tenant, 'phone_number', '')

    locatario_info_text = f"DE OUTRO LADO, denominado (s) LOCATÁRIO (S) {locatario_nome}, CPF – {locatario_cpf}"
    if locatario_phone:
        locatario_info_text += f", Telefone – {locatario_phone}"
    locatario_info_text += ", considerado capaz."

    elements.append(Paragraph(locatario_info_text, normal_text_style))
    elements.append(Spacer(1, 0.5*cm))

    imovel_address = contract.property.address
    imovel_city = contract.property.city
    imovel_zip_code = contract.property.zip_code or ''
    imovel_state = contract.property.state

    # Lógica para a descrição do imóvel (quantidade de cômodos)
    num_rooms = getattr(contract.property, 'num_rooms', 0)
    room_details = getattr(contract.property, 'room_details', "")

    imovel_description_text = ""
    if num_rooms > 0 and room_details:
        imovel_description_text = f"com {num_rooms} dependências, tais como; {room_details}."
    elif contract.property.description:
        imovel_description_text = contract.property.description
    else:
        imovel_description_text = "sem descrição detalhada."
    
    elements.append(Paragraph(
        f"O IMÓVEL de propriedade do LOCADOR, situa-se na {imovel_address} - {imovel_city}, C.E.P {imovel_zip_code}, Estado - {imovel_state}, {imovel_description_text}",
        normal_text_style
    ))
    elements.append(Spacer(1, 0.5*cm))

    formatted_start_date = contract.start_date.strftime('%d/%m/%Y') if contract.start_date else ""
    formatted_end_date = contract.end_date.strftime('%d/%m/%Y') if contract.end_date else ""
    
    duration_text_contract = "indeterminado"
    if contract.start_date and contract.end_date:
        delta = relativedelta(contract.end_date, contract.start_date)
        years = delta.years
        months = delta.months
        
        if years > 0 and months > 0:
            duration_text_contract = f"{years} ano(s) e {months} mes(es)"
        elif years > 0:
            duration_text_contract = f"{years} ano(s)"
        elif months > 0:
            duration_text_contract = f"{months} mes(es)"
        else:
            duration_text_contract = f"{delta.days} dia(s)"

    elements.append(Paragraph(
        f"O PRAZO da locação do imóvel mencionado acima terá validade de {duration_text_contract}, e sendo renovado de ano em ano por acordo das partes.",
        normal_text_style
    ))
    elements.append(Spacer(1, 0.5*cm))

    elements.append(Paragraph(
        "A presente LOCAÇÃO destina-se ao uso do imóvel somente para fins residenciais, estando o LOCATÁRIO proibido de sublocá-lo ou usá-lo de forma diferente do previsto, sem a devida autorização do PROPRIETÁRIO ou LOCADOR.",
        normal_text_style
    ))
    elements.append(Spacer(1, 0.5*cm))

    rent_value_extenso = numero_por_extenso(float(contract.rent_amount))
    
    elements.append(Paragraph(
        f"LOCATÁRIO pagará o valor de R$ {contract.rent_amount:.2f} ({rent_value_extenso}) a ser efetuado diretamente ao LOCADOR, ou na sua ausência, seu CÔNJUGE Pagamento no valor acima, deverá ser feito até o dia {contract.due_day:02d} de cada mês. Será cobrada multa de 10% para pagamento feito após prazo de tolerância de 10 dias úteis da data de vencimento OU, além de correções e outras despesas previstas por lei.",
        normal_text_style
    ))
    elements.append(Spacer(1, 0.5*cm))

    elements.append(Paragraph(
        f"DEPÓSITO no valor de 1(um) mês de aluguel será cobrado como garantia para retenção do imóvel, na mesma data do pagamento do aluguel.",
        normal_text_style
    ))
    elements.append(Spacer(1, 0.5*cm))

    elements.append(Paragraph(
        "LOCATÁRIO responsabiliza-se de pagar todos os serviços públicos e despesas ligadas à conservação do imóvel, tais como; imposto predial (IPTU), seguro de incêndio e enchente, taxa de luz, saneamento, esgoto, gás, telefone, condomínio etc.",
        normal_text_style
    ))
    elements.append(Spacer(1, 0.5*cm))

    elements.append(Paragraph(
        "Construções, Modificações ou contribuições de melhoria que sejam destinadas ao imóvel deverão de imediato, ser submetidas a autorização expressa do LOCADOR/PROPRIETÁRIO.",
        normal_text_style
    ))
    elements.append(Spacer(1, 0.5*cm))

    elements.append(Paragraph(
        "Caso uma RESCISÃO do contrato de aluguel for necessária, ambas as partes concordam em dar um prazo de 30 dias de aviso.",
        normal_text_style
    ))
    elements.append(Spacer(1, 0.2*cm))
    elements.append(Paragraph(
        "RESCISÃO imediata do presente contrato, sem prejuízo dos numerários previstos neste, ocorrerá caso aconteça qualquer sinistro que venha a impossibilitar o uso do imóvel, também em caso de desapropriação do mesmo.",
        normal_text_style
    ))
    elements.append(Spacer(1, 0.5*cm))

    elements.append(Paragraph(
        "O valor do aluguel será REAJUSTADO a cada período de 12 meses de acordo com a variação do índice do percentual do aumento do salário mínimo nacional.",
        normal_text_style
    ))
    elements.append(Spacer(1, 0.5*cm))

    elements.append(Paragraph(
        "O LOCADOR concorda que objeto de locação será entregue limpo e em condições de perfeito funcionamento, tais como instalações elétricas e hidráulicas, portas, portões e acessórios, paredes pintadas, cômodos em bom estado e com todas as despesas e tributos pagos. O LOCATÁRIO assume responsabilidade em manter o imóvel locado desta forma e o restituirá nas mesmas condições.",
        normal_text_style
    ))
    elements.append(Spacer(1, 0.5*cm))

    elements.append(Paragraph(
        "O LOCATÁRIO permitirá ao LOCADOR, realizar inspeções no imóvel em data e horário a ser combinados, com propósito de averiguar o funcionamento das instalações e acessórios. O LOCATÁRIO deve realizar os consertos no prazo de 15 dias, se algum vício que possa afetar a estrutura física ou prejudicar as condições estéticas e de segurança do imóvel for constatado nas vistorias realizadas. O LOCADOR ficará facultado a RESCINDIR O CONTRATO DE ALUGUEL, se dito conserto não for efetuado no prazo determinado, sem multa ou indenização previstos neste.",
        normal_text_style
    ))
    elements.append(Spacer(1, 0.5*cm))

    elements.append(Paragraph(
        "Os herdeiros, cessionários ou sucessores das partes vinculadas neste contrato de aluguel se obrigam desde já ao teor completo deste contrato.",
        normal_text_style
    ))
    elements.append(Spacer(1, 0.5*cm))
    
    elements.append(Paragraph(
        "De maneira acordada e justa, LOCATÁRIO e LOCADOR, assinam o presente INSTRUMENTO PARTICULAR DE LOCAÇÃO RESIDENCIAL, que passa a vigorar e fica desde agora aceito, pelas cláusulas acima descritas.",
        normal_text_style
    ))
    elements.append(Spacer(1, 0.5*cm))

    local_signature = "Rio de Janeiro"
    current_day = date.today().day
    current_month_pt_name = {
        1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril", 5: "maio", 6: "junho",
        7: "julho", 8: "agosto", 9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"
    }[date.today().month]
    current_year = date.today().year

    elements.append(Paragraph(f"LOCAL, {local_signature}, DATA {current_day:02d}/{date.today().month:02d}/{current_year}.", normal_text_style))
    elements.append(Spacer(1, 1.5*cm))

    elements.append(Paragraph("____________________________________", signature_line_style))
    elements.append(Paragraph(f"Locatário (a): {locatario_nome}", signature_line_style))
    elements.append(Spacer(1, 1.0*cm))

    elements.append(Paragraph("____________________________________", signature_line_style))
    elements.append(Paragraph(f"Locador (a): {locador_nome}", signature_line_style))
    elements.append(Spacer(1, 1.0*cm))

    elements.append(Paragraph("____________________________________", signature_line_style))
    elements.append(Paragraph("Testemunha 1", signature_line_style))
    elements.append(Spacer(1, 0.5*cm))

    elements.append(Paragraph("____________________________________", signature_line_style))
    elements.append(Paragraph("Testemunha 2", signature_line_style))
    elements.append(Spacer(1, 0.5*cm))

    elements.append(Paragraph(f"Contrato gerado eletronicamente em: {date.today().strftime('%d/%m/%Y')}", footer_date_style))


    doc.build(elements)

    return response
