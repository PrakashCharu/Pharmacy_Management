from django.db import models

# Create your models here.

#autogenrate
class autogenerate(models.Model):
    supid = models.CharField(max_length=50, default=0)
    pid = models.CharField(max_length=50, default=0)
    cid = models.CharField(max_length=50, default=0)
    empid = models.CharField(max_length=50, default=0)
    oid = models.CharField(max_length=50, default=0)
    mid = models.CharField(max_length=50, default=0)
    payid = models.CharField(max_length=50, default=0)


#SUPPLIER

class Supplier(models.Model):
    supplier_id=models.CharField(max_length=50,unique=True)
    supplier_name=models.CharField(max_length=50)
    contact_person=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=15)
    email_address=models.CharField(max_length=30)
    company_address=models.CharField(max_length=100)
    gst_number=models.CharField(max_length=20)
    pan_number=models.CharField(max_length=20)
    bank_account_number=models.CharField(max_length=20)
    ifsc_code=models.CharField(max_length=15)
    medicine_categories=models.CharField(max_length=50)
    lience_number=models.CharField(max_length=20)
    status=models.BooleanField()

# MEDICINE

class Medicine(models.Model):
    medicine_id = models.CharField(max_length=20, unique=True)        
    medicine_name = models.CharField(max_length=100)                  
    description = models.CharField(max_length=255)                   
    category = models.CharField(max_length=50)                       
    unit_type = models.CharField(max_length=200)
    composition = models.CharField(max_length=100)                 
    manufacturer = models.CharField(max_length=100)                  

#EMPLOYEE

class Employee(models.Model):
    emp_id = models.CharField(max_length=20, unique=True)      
    emp_name = models.CharField(max_length=100)                      
    dob = models.DateField()                                           
    gender = models.CharField(max_length=100)
    marital_status = models.CharField(max_length=100)
    nationality = models.CharField(max_length=50)                     
    blood_group = models.CharField(max_length=50)
    emp_phone = models.CharField(max_length=15)                      
    email = models.EmailField(max_length=50)                           
    present_address = models.CharField(max_length=200)                
    emp_position = models.CharField(max_length=300)
    emp_salary = models.DecimalField(max_digits=10, decimal_places=2)  
    education = models.CharField(max_length=100)                       
    emergency_contact = models.CharField(max_length=15)                
    emp_photo = models.ImageField(upload_to='employee_photos/', null=True) 
    date_joined = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=True)  

# PURCHASE DETAILS

class Purchase(models.Model):
    purchase_id = models.CharField(max_length=20, unique=True)        
    supplier_id = models.ForeignKey(Supplier,to_field='supplier_id', on_delete=models.CASCADE)  
    invoice_no = models.CharField(max_length=50)                        
    purchase_date = models.DateField()                                  
    payment_mode = models.CharField(max_length=200) 
    gross_total = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    tax = models.DecimalField(max_digits=5, decimal_places=2, null=True, )
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.CharField(max_length=255, null=True)   


#PURCHASE ITEMS
  
class PurchaseItem(models.Model):
    purchase_item = models.CharField(max_length=20)  
    purchhase_id=models.ForeignKey(Purchase,to_field='purchase_id', on_delete=models.CASCADE)
    medicine_id = models.ForeignKey(Medicine,to_field='medicine_id', on_delete=models.CASCADE)   
    batch_no = models.CharField(max_length=50)                          
    mfg_date = models.DateField()                                        
    expiry_date = models.DateField()                                     
    quantituy = models.PositiveIntegerField()                                  
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)   
    line_amount = models.DecimalField(max_digits=10, decimal_places=2) 
    sellingPrice=models.DecimalField(max_digits=10, decimal_places=2, default=0) 
  

                            
#CUSTOMER

class Customer(models.Model):
    cust_id = models.CharField(max_length=20, unique=True) 
    cust_name = models.CharField(max_length=100)           
    cust_dob = models.DateField()                           
    cust_gender = models.CharField(max_length=10)
    cust_phone = models.CharField(max_length=15)           
    cust_email = models.EmailField(max_length=50)           
    cust_address = models.CharField(max_length=200)         
    cust_blood_group = models.CharField(max_length=50)
    doctor_name = models.CharField(max_length=100)      


#SALES

class Sales(models.Model):
    order_id = models.CharField(max_length=20, primary_key=True)
    customer_id = models.ForeignKey(Customer,to_field='cust_id', on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    gross_total = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=200)
    payment_status = models.CharField(max_length=20)
    order_status = models.CharField(max_length=20)
    


#SALES ITEM

class SaleItem(models.Model):

    order_id = models.ForeignKey(Sales,to_field='order_id', on_delete=models.CASCADE)
    medicine_id = models.ForeignKey(Medicine,to_field='medicine_id', on_delete=models.CASCADE)
    batch_no = models.CharField(max_length=30)
    quantity = models.PositiveIntegerField()
    selling_price = models.DecimalField(max_digits=8, decimal_places=2)
    line_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True) 
     


#STOCK TABLE

class Stock(models.Model):
    medicine_id = models.ForeignKey(Medicine,to_field='medicine_id', on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=500, null=True)
    batch_no = models.CharField(max_length=30)
    expiry_date = models.DateField()
    sPrice=models.DecimalField(max_digits=8, decimal_places=2 , null=True)
    current_qty = models.PositiveIntegerField()


#EMPLOYEE PAYMENT

class EmployeePayment(models.Model):
    payment_id = models.CharField(max_length=20)
    emp_id = models.ForeignKey(Employee,to_field='emp_id', on_delete=models.CASCADE)
    payment_date = models.DateField()
    payment_month = models.CharField(max_length=7) 
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=200)
    remarks = models.TextField(blank=True, null=True)
    
