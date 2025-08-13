from django.contrib import admin
from django.urls import path, include
from pharmacy_private import  views

urlpatterns = [
    path('', views.login_request, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.index, name='index'),
    
    path('Customer-entry/', views.customer_entry, name='customer_entry'),
    path('Customer-service/', views.customer_service, name='customer_service'),
    path('customer-update/<getdata>/action/', views.customer_update, name='customerUpdate'),
    path('customer-delete/<getdata>/action/Delete', views.customer_delete, name='customerUpdate'),


    path('Employee-service/', views.employee_service, name='employee_service'),
    path('employee-entry/', views.employee_entry, name='employee_entry'),
    path('employee-update/<getdata>/action/', views.employee_update, name='employeeUpdate'),
    path('employee-delete/<getdata>/action/Delete', views.employee_delete, name='employeeDelete'),

    
    path('supplier-entry/', views.supplier_entry, name='supplier_entry'),
    path('supplier-service/', views.supplier_service, name='supplier_service'),
    path('supplier-update/<getdata>/action/', views.suplierUpdate, name='suplierUpdate'),
    path('supplier-delete/<getdata>/action/Delete/', views.supplierDelete, name='suplierDelete'),

    path('medicine-entry/', views.medicine_entry, name='medicine'),
    path('medicine-search/', views.medicine_search, name='medicine_search'),
    path('medicine-update/<getdata>/action/', views.medicine_update, name='MedicineUpdate'),
    path('medicine-delete/<getdata>/action/Delete', views.medicine_delete, name='MedicineUpdate'),

    path('Purchase-details/', views.purchase_details, name='purchase_details'),
    path('Purchase-service/', views.purchase_service, name='purchase_service'),

    path('Employee-payment/', views.emp_payment, name='emp_payment'),
    path('Employee-payment-service/', views.emp_payment_service, name='emp_payment_service'),

    path('Order-details/', views.order_details, name='order_details'),
    path('Order-service/', views.order_service, name='order_service'),

    path('stock-details/', views.stock_details, name='stock'),

]

