from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import ClientForm, ContractForm, EmployeeForm, ImmobileForm, MaintenanceRequestForm, OwnerForm, PaymentForm, RegisterLocationForm, VisitScheduleForm
from .models import Contract, Employee, Immobile, ImmobileImage, MaintenanceRequest, Owner, Payment, VisitSchedule
from .models import Contract  # Verifique se isso está no topo do seu arquivo de views



# Create your views here.
def list_location(request):
    immobiles = Immobile.objects.filter(is_locate=False)
    context = {'immobiles': immobiles}
    return render(request, 'list-location.html', context)


def form_client(request):
    form = ClientForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list-location')   
    return render(request, 'form-client.html', {'form': form})


def form_immobile(request):
    form = ImmobileForm() 
    if request.method == 'POST':
        form = ImmobileForm(request.POST, request.FILES)
        if form.is_valid():
            immobile = form.save()
            files = request.FILES.getlist('immobile') ## pega todas as imagens
            if files:
                for f in files:
                    ImmobileImage.objects.create( # cria instance para imagens
                        immobile=immobile, 
                        image=f)
            return redirect('list-location')   
    return render(request, 'form-immobile.html', {'form': form})


def form_location(request, id):
    get_locate = Immobile.objects.get(id=id) ## pega objeto
    form = RegisterLocationForm()  
    if request.method == 'POST':
        form = RegisterLocationForm(request.POST)
        if form.is_valid():
            location_form = form.save(commit=False)
            location_form.immobile = get_locate ## salva id do imovel 
            location_form.save()  
            
            ## muda status do imovel para "Alugado"
            immo = Immobile.objects.get(id=id)
            immo.is_locate = True ## passa ser True
            immo.save() 
            return redirect('list-location') # Retorna para lista

    context = {'form': form, 'location': get_locate}
    return render(request, 'form-location.html', context)


## Relatório
def reports(request): ## Relatórios   
    immobile = Immobile.objects.all()
    
    get_client = request.GET.get('client') 
    get_locate = request.GET.get('is_locate')
    get_type_item = request.GET.get('type_item') 

    get_dt_start = request.GET.get('dt_start')
    get_dt_end = request.GET.get('dt_end')
    print(get_dt_start, get_dt_end)

    if get_client: ## Filtra por nome e email do cliente
        immobile = Immobile.objects.filter(
					Q(reg_location__client__name__icontains=get_client) | 
					Q(reg_location__client__email__icontains=get_client))
    
    if get_dt_start and get_dt_end: ## Por data
        immobile = Immobile.objects.filter(
						reg_location__create_at__range=[get_dt_start,get_dt_end])

    if get_locate:
        immobile = Immobile.objects.filter(is_locate=get_locate)

    if get_type_item:
        immobile = Immobile.objects.filter(type_item=get_type_item)

    return render(request, 'reports.html', {'immobiles':immobile})


# Contratos
def contract_list(request):
    contracts = Contract.objects.all()
    return render(request, 'contract-list.html', {'contracts': contracts})

def contract_create(request):
    form = ContractForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('contract-list')
    return render(request, 'contract-form.html', {'form': form})

def contract_update(request, pk):
    contract = Contract.objects.get(id=pk)
    form = ContractForm(request.POST or None, request.FILES or None, instance=contract)
    if form.is_valid():
        form.save()
        return redirect('contract-list')
    return render(request, 'contract-form.html', {'form': form})

def contract_delete(request, pk):
    contract = Contract.objects.get(id=pk)
    if request.method == 'POST':
        contract.delete()
        return redirect('contract-list')
    return render(request, 'confirm-delete.html', {'object': contract, 'title': 'Contrato'})



#Pagamento
# Pagamentos
def payment_list(request):
    payments = Payment.objects.all()
    return render(request, 'payment-list.html', {'payments': payments})

def payment_create(request):
    form = PaymentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('payment-list')
    return render(request, 'payment-form.html', {'form': form})

def payment_update(request, pk):
    payment = Payment.objects.get(id=pk)
    form = PaymentForm(request.POST or None, instance=payment)
    if form.is_valid():
        form.save()
        return redirect('payment-list')
    return render(request, 'payment-form.html', {'form': form})

def payment_delete(request, pk):
    payment = Payment.objects.get(id=pk)
    if request.method == 'POST':
        payment.delete()
        return redirect('payment-list')
    return render(request, 'confirm-delete.html', {'object': payment, 'title': 'Pagamento'})

#Funcionario
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee-list.html', {'employees': employees})


def employee_create(request):
    form = EmployeeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('employee-list')
    return render(request, 'employee-form.html', {'form': form})


def employee_update(request, pk):
    employee = Employee.objects.get(id=pk)
    form = EmployeeForm(request.POST or None, instance=employee)
    if form.is_valid():
        form.save()
        return redirect('employee-list')
    return render(request, 'employee-form.html', {'form': form})


def employee_delete(request, pk):
    employee = Employee.objects.get(id=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee-list')
    return render(request, 'confirm-delete.html', {'object': employee, 'title': 'Funcionário'})


#VISTAS
def visit_list(request):
    visits = VisitSchedule.objects.all()
    return render(request, 'visit-list.html', {'visits': visits})

def visit_create(request):
    form = VisitScheduleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('visit-list')
    return render(request, 'visit-form.html', {'form': form})

def visit_update(request, pk):
    visit = VisitSchedule.objects.get(id=pk)
    form = VisitScheduleForm(request.POST or None, instance=visit)
    if form.is_valid():
        form.save()
        return redirect('visit-list')
    return render(request, 'visit-form.html', {'form': form})

def visit_delete(request, pk):
    visit = VisitSchedule.objects.get(id=pk)
    if request.method == 'POST':
        visit.delete()
        return redirect('visit-list')
    return render(request, 'confirm-delete.html', {'object': visit, 'title': 'Visita'})


#Manuetebção
# Manutenções
def maintenance_list(request):
    maintenances = MaintenanceRequest.objects.all()
    return render(request, 'maintenance-list.html', {'maintenances': maintenances})

def maintenance_create(request):
    form = MaintenanceRequestForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('maintenance-list')
    return render(request, 'maintenance-form.html', {'form': form})

def maintenance_update(request, pk):
    maintenance = MaintenanceRequest.objects.get(id=pk)
    form = MaintenanceRequestForm(request.POST or None, instance=maintenance)
    if form.is_valid():
        form.save()
        return redirect('maintenance-list')
    return render(request, 'maintenance-form.html', {'form': form})

def maintenance_delete(request, pk):
    maintenance = MaintenanceRequest.objects.get(id=pk)
    if request.method == 'POST':
        maintenance.delete()
        return redirect('maintenance-list')
    return render(request, 'confirm-delete.html', {'object': maintenance, 'title': 'Manutenção'})


#Proprietario
def owner_list(request):
    owners = Owner.objects.all()
    return render(request, 'owner-list.html', {'owners': owners})


def owner_create(request):
    form = OwnerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('owner-list')
    return render(request, 'owner-form.html', {'form': form})


def owner_update(request, pk):
    owner = Owner.objects.get(id=pk)
    form = OwnerForm(request.POST or None, instance=owner)
    if form.is_valid():
        form.save()
        return redirect('owner-list')
    return render(request, 'owner-form.html', {'form': form})


def owner_delete(request, pk):
    owner = Owner.objects.get(id=pk)
    if request.method == 'POST':
        owner.delete()
        return redirect('owner-list')
    return render(request, 'confirm-delete.html', {'object': owner, 'title': 'Proprietário'})








