from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages

from .forms import (
    ClientForm, ContractForm, EmployeeForm, ImmobileForm, MaintenanceRequestForm,
    OwnerForm, PaymentForm, RegisterLocationForm, VisitScheduleForm
)

from .models import (
    Contract, Employee, Immobile, ImmobileImage, MaintenanceRequest, Owner,
    Payment, VisitSchedule, Client, RegisterLocation
)

# Repositórios para injeção de dependência

class ImmobileRepository:
    def list_available(self):
        return Immobile.objects.filter(is_locate=False)

    def save(self, immobile):
        immobile.save()

    def get_by_id(self, id):
        return Immobile.objects.get(id=id)


class RegisterLocationRepository:
    def get(self, id):
        return get_object_or_404(RegisterLocation, id=id)

    def delete(self, loc):
        loc.delete()


# Views com DI

def list_location(request, immobile_repo=ImmobileRepository()):
    immobiles = immobile_repo.list_available()
    context = {'immobiles': immobiles}
    return render(request, 'list-location.html', context)


def delete_register_location(
    request,
    id,
    loc_repo=RegisterLocationRepository(),
    immobile_repo=ImmobileRepository()
):
    loc = loc_repo.get(id)
    immobile = loc.immobile
    immobile.is_locate = False
    immobile_repo.save(immobile)

    loc_repo.delete(loc)

    messages.success(request, 'Registro de locação excluído com sucesso e imóvel liberado.')
    return redirect('reports')


# Outras views 

def location_report(request):
    owners = Owner.objects.all()
    selected_owner_id = request.GET.get('owner')

    if selected_owner_id:
        locations = RegisterLocation.objects.filter(
            immobile__owner__id=selected_owner_id
        )
    else:
        locations = RegisterLocation.objects.all()

    context = {
        'locations': locations,
        'owners': owners,
        'selected_owner_id': int(selected_owner_id) if selected_owner_id else None,
        'owners': Owner.objects.all(),
    }
    return render(request, 'location_report.html', context)


def reports_view(request):
    owner_id = request.GET.get('owner')
    immobiles = Immobile.objects.prefetch_related('reg_location')

    if owner_id:
        immobiles = immobiles.filter(owner_id=owner_id)

    context = {
        'immobiles': immobiles,
        'owners': Owner.objects.all(),
    }
    return render(request, 'reports.html', context)


def client_create(request):
    form = ClientForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('client-list')
    return render(request, 'form-client.html', {
        'form': form,
        'form_action': reverse('client-create')
    })


def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client_list.html', {'clients': clients})


def client_update(request, id):
    client = get_object_or_404(Client, id=id)
    form = ClientForm(request.POST or None, instance=client)
    if form.is_valid():
        form.save()
        return redirect('client-list')
    return render(request, 'form-client.html', {
        'form': form,
        'form_action': reverse('client-update', args=[id])
    })


def client_delete(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == 'POST':
        client.delete()
        return redirect('client-list')
    return render(request, 'client_confirm_delete.html', {'client': client})


def form_immobile(request):
    form = ImmobileForm()
    if request.method == 'POST':
        form = ImmobileForm(request.POST, request.FILES)
        if form.is_valid():
            immobile = form.save()
            files = request.FILES.getlist('immobile')
            if files:
                for f in files:
                    ImmobileImage.objects.create(
                        immobile=immobile,
                        image=f
                    )
            return redirect('list-location')
    return render(request, 'form-immobile.html', {'form': form})


def form_location(request, id):
    get_locate = Immobile.objects.get(id=id)
    form = RegisterLocationForm()
    if request.method == 'POST':
        form = RegisterLocationForm(request.POST)
        if form.is_valid():
            location_form = form.save(commit=False)
            location_form.immobile = get_locate
            location_form.save()

            immo = Immobile.objects.get(id=id)
            immo.is_locate = True
            immo.save()
            return redirect('list-location')

    context = {'form': form, 'location': get_locate}
    return render(request, 'form-location.html', context)


def edit_immobile(request, id):
    immobile = get_object_or_404(Immobile, id=id)
    form = ImmobileForm(request.POST or None, request.FILES or None, instance=immobile)

    if request.method == 'POST':
        if form.is_valid():
            form.save()

            files = request.FILES.getlist('immobile')
            if files:
                immobile.immobile_images.all().delete()

                for f in files:
                    ImmobileImage.objects.create(immobile=immobile, image=f)

            return redirect('list-location')

    return render(request, 'edit-immobile.html', {'form': form, 'immobile': immobile})


def delete_immobile(request, id):
    immobile = Immobile.objects.get(id=id)
    if request.method == 'POST':
        immobile.delete()
        return redirect('list-location')
    return render(request, 'confirm_delete.html', {'object': immobile})


def reports(request):
    immobile = Immobile.objects.all()

    get_client = request.GET.get('client')
    get_locate = request.GET.get('is_locate')
    get_type_item = request.GET.get('type_item')
    get_dt_start = request.GET.get('dt_start')
    get_dt_end = request.GET.get('dt_end')
    get_owner = request.GET.get('owner')

    if get_client:
        immobile = immobile.filter(
            Q(reg_location__client__name__icontains=get_client) |
            Q(reg_location__client__email__icontains=get_client)
        )

    if get_dt_start and get_dt_end:
        immobile = immobile.filter(
            reg_location__create_at__range=[get_dt_start, get_dt_end]
        )

    if get_locate:
        immobile = immobile.filter(is_locate=get_locate)

    if get_type_item:
        immobile = immobile.filter(type_item=get_type_item)

    if get_owner:
        immobile = immobile.filter(owner_id=get_owner)

    return render(request, 'reports.html', {
        'immobiles': immobile,
        'owners': Owner.objects.all(),
    })


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


# Funcionários
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


# Visitas
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


# Proprietários
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
