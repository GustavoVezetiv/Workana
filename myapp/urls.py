from django.urls import path 
from myapp import views

urlpatterns = [
    path('', views.list_location, name='list-location'), 

    path('form-client/', views.client_create, name='client-create'),

    path('form-immobile/', views.form_immobile, name='immobile-create'),  

    path('form-location/<int:id>/', views.form_location, name='location-create'), 

    path('reports/', views.reports, name='reports'),

    path('reports/delete/<int:id>/', views.delete_register_location, name='delete-location'),




    path('clients/', views.client_list, name='client-list'),

    path('clients/edit/<int:id>/', views.client_update, name='client-update'),

    path('clients/delete/<int:id>/', views.client_delete, name='client-delete'),




    path('form-immobile/edit/<int:id>/', views.edit_immobile, name='immobile-edit'),


    path('form-immobile/<int:id>/', views.edit_immobile, name='immobile-edit'),

    path('delete-immobile/<int:id>/', views.delete_immobile, name='immobile-delete'),


    # Contratos
    path('contracts/', views.contract_list, name='contract-list'),

    path('contracts/create/', views.contract_create, name='contract-create'),

    path('contracts/edit/<int:pk>/', views.contract_update, name='contract-update'),

    path('contracts/delete/<int:pk>/', views.contract_delete, name='contract-delete'),


    #Pagamentoss
    path('payments/', views.payment_list, name='payment-list'),

    path('payments/create/', views.payment_create, name='payment-create'),

    path('payments/edit/<int:pk>/', views.payment_update, name='payment-update'),

    path('payments/delete/<int:pk>/', views.payment_delete, name='payment-delete'),


    #Funcionario
    path('employees/', views.employee_list, name='employee-list'),

    path('employees/create/', views.employee_create, name='employee-create'),

    path('employees/edit/<int:pk>/', views.employee_update, name='employee-update'),

    path('employees/delete/<int:pk>/', views.employee_delete, name='employee-delete'),

    #VISITAS AGENDADAS
    path('visits/', views.visit_list, name='visit-list'),

    path('visits/create/', views.visit_create, name='visit-create'),
    
    path('visits/edit/<int:pk>/', views.visit_update, name='visit-update'),

    path('visits/delete/<int:pk>/', views.visit_delete, name='visit-delete'),

    #Manutenção
    path('maintenances/', views.maintenance_list, name='maintenance-list'),

    path('maintenances/create/', views.maintenance_create, name='maintenance-create'),

    path('maintenances/edit/<int:pk>/', views.maintenance_update, name='maintenance-update'),

    path('maintenances/delete/<int:pk>/', views.maintenance_delete, name='maintenance-delete'),


    # PROPRIETÁRIO
    path('owners/', views.owner_list, name='owner-list'),

    path('owners/create/', views.owner_create, name='owner-create'),

    path('owners/edit/<int:pk>/', views.owner_update, name='owner-update'),

    path('owners/delete/<int:pk>/', views.owner_delete, name='owner-delete'),








 
]