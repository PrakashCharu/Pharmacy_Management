from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import http
from pharmacy_private import models
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def login_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Please Check Your Credintials !')
            return redirect('login')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def index(request):
    data ={
        'title' : 'Pharmacy Management'
    }
    try:
        models.autogenerate.objects.get(id=1)
    except models.autogenerate.DoesNotExist:
        obj = models.autogenerate.objects.create()
        obj.save()

    total_Employee  = models.Employee.objects.all().count()
    total_medicine  = models.Medicine.objects.all().count()
    print(total_Employee)
    print(total_medicine)
    return render(request,'index.html', {'data':data})

@login_required
def customer_entry(request):
    data={
            'title' : 'Customer Entry'
        }
    try:
        cid=models.autogenerate.objects.get(id=1).cid
        if int(cid)<10:
            cust_id='CUST-00'+ str(int(cid)+1)
        elif int(cid)<100:
            cust_id='CUST-0' + str(int(cid)+1)
        else:
            cust_id='CUST-' + str(int(cid)+1)
        data['cid'] = cust_id
    except models.autogenerate.DoesNotExist:
        print("data not found")

    if request.method=="POST":
        obj=models.Customer()
        obj.cust_id=request.POST.get('custId')
        obj.cust_name=request.POST.get('custName')
        obj.cust_dob=request.POST.get('custDob')
        obj.cust_gender=request.POST.get('custGender')
        obj.cust_phone=request.POST.get('custPhone')
        obj.cust_email=request.POST.get('custEmail')
        obj.cust_address=request.POST.get('custAddress')
        obj.cust_blood_group=request.POST.get('custBloodGroup')
        obj.doctor_name=request.POST.get('doctorName')
        obj.save()
        if obj.pk is not None:
            try:
                cid=models.autogenerate.objects.get(id=1)
                cid.cid=int(cid.cid)+1
                cid.save()
            except Exception as error:
                print(error )
            messages.success(request, "Customer Created Successfully !")
            return redirect('customer_service')

    return render(request, 'customer_entry.html' , {'data': data})


@login_required
def customer_service(request):
    if request.method=='GET':
        custInfo=models.Customer.objects.values('cust_id','cust_name','cust_phone','doctor_name')
        data = {
            'cust_id' : custInfo.values('cust_id').distinct(),
            'cust_name' : custInfo.values('cust_name').distinct(),
            'cust_phone' : custInfo.values('cust_phone').distinct(),
            'doctor_name' : custInfo.values('doctor_name').distinct(),
        }

        return render(request, 'customer_service.html', {'custInfo':custInfo,'data':data})

    elif request.method=='POST':
        cust_id=request.POST.get('custId')
        cust_name=request.POST.get('custName')
        cust_phone=request.POST.get('custPhone')
        doctor_name=request.POST.get('doctorName')
    
        condition ={}
        if cust_id is not None and cust_id != "":
            condition['cust_id'] = cust_id
        if cust_name is not None and cust_name!="":
            condition['cust_name'] = cust_name
        if cust_phone is not None and cust_phone!="":
            condition['cust_phone'] = cust_phone
        if doctor_name is not None and doctor_name!="":
            condition['doctor_name'] = doctor_name
        
        if condition:
            filter_data=models.Customer.objects.filter(**condition)
            if filter_data.exists():
                table_data = f'''
                            <table class="table">
                                <thead class="bg-dark">
                                     <th class="text-white p-3">S.No.</th>
                                     <th class="text-white p-3">Customer ID</th>
                                     <th class="text-white p-3">Customer Name</th>
                                     <th class="text-white p-3">Gender</th>
                                     <th class="text-white p-3">Phone number</th>
                                     <th class="text-white p-3">Date  of  Birth</th>
                                     <th class="text-white p-3">Address</th>
                                     <th class="text-white p-3">E-mail.</th>
                                     <th class="text-white p-3">Blood Group</th>
                                     <th class="text-white p-3">Referring doctor's name</th>
                                     <th colspan="2" class="text-white p-3">Action</th>
                                 </thead>
                                <tbody>
                        '''
                sno = 0
                for x in filter_data:
                    sno += 1
                    table_data += '<tr>'
                    table_data += f'<td>{str(sno)}</td>'
                    table_data += f'<td>{x.cust_id}</td>'
                    table_data += f'<td>{x.cust_name}</td>'
                    table_data += f'<td>{x.cust_gender}</td>'
                    table_data += f'<td>{x.cust_phone}</td>'
                    table_data += f'<td>{x.cust_dob}</td>'
                    table_data += f'<td>{x.cust_email}</td>'
                    table_data += f'<td>{x.cust_address}</td>'
                    table_data += f'<td>{x.cust_blood_group}</td>'
                    table_data += f'<td>{x.doctor_name}</td>'

                    table_data+=f"<td><a href='\customer-update/{x.id}/action/'><button>Edit</button></a></td>"
                    table_data += f'<td><a onclick="deleteit(\'/customer-delete/{x.id}/action/Delete\')"><button>Delete</button></a></td>'
                    table_data += '</tr>'
                table_data += '</tbody></table>'

                success_data = {
                    'table_data' :table_data
                }
                return http.JsonResponse(success_data, safe=False)
            else:
                table_data = f'''
                <div class="alert alert-warning fs-4">No Records Found !</div>
                '''   
                success_data = {
                    'table_data' :table_data
                }
                return http.JsonResponse(success_data, safe=False) 
        else:
            table_data = f'''
                <div class="alert alert-warning fs-4">At Least Select One Condition !</div>
                '''   
            success_data = {
                'table_data' :table_data
            }
            return http.JsonResponse(success_data, safe=False)


@login_required
def customer_update(request,getdata):
    updateData=models.Customer.objects.get(id=getdata)
    if request.method=='POST':
        obj=models.Customer.objects.get(id=getdata)
        obj.cust_id=request.POST.get("custId")
        obj.cust_name=request.POST.get("custName")
        obj.cust_dob=request.POST.get("custDob")
        obj.cust_gender=request.POST.get("custGender")
        obj.cust_phone=request.POST.get("custPhone")
        obj.cust_email=request.POST.get("custEmail")
        obj.cust_address=request.POST.get("custAddress")
        obj.cust_blood_group=request.POST.get("custBloodGroup")
        obj.doctor_name=request.POST.get("doctorName")
        obj.save()
        if obj.pk is not None:
            messages.success(request, "Customer Information updated Successfully !")
            return redirect('customer_service')
    return render(request,'customer_update.html', {'updateData':updateData})

@login_required
def customer_delete(request, getdata):
    deleteData= models.Customer.objects.get(id=getdata)
    deleteData.delete()
    return http.JsonResponse(200, safe=False)


@login_required
def employee_entry(request):
    data={
        'title' : 'Employee Entry'
    }
    try:
        eid=models.autogenerate.objects.get(id=1).empid
        if int(eid)<10:
            emp_id='EMP-00' + str(int(eid)+1)
        elif int(eid)<100:
            emp_id='EMP-0' + str(int(eid)+1)
        else:
            emp_id='EMP-' + str(int(eid)+1)
        data['eid']=emp_id
    except models.autogenerate.DoesNotExist:
        print('data not found')

    if request.method=="POST":
        obj=models.Employee()
        obj.emp_id=request.POST.get('empId')
        obj.emp_name=request.POST.get('empName')
        obj.dob=request.POST.get('dob')
        obj.gender=request.POST.get('gender')
        obj.marital_status=request.POST.get('maritalStatus')
        obj.nationality=request.POST.get('nationality')
        obj.blood_group=request.POST.get('bloodGroup')
        obj.emp_phone=request.POST.get('empPhone')
        obj.email=request.POST.get('email')
        obj.present_address=request.POST.get('presentAddress')
        obj.emp_position=request.POST.get('empPosition')
        obj.emp_salary=request.POST.get('empSalary')
        obj.education=request.POST.get('education')
        obj.emergency_contact=request.POST.get('emergencyContact')
        obj.emp_photo=request.POST.get('empPhoto')
        password=request.POST.get('password')
        # obj.date_joined=request.POST.get('empId')
        # obj.status=request.POST.get('empId')

        usercreation = User.objects.create_user(username=request.POST.get('empId'), email=request.POST.get('email'), password=password)
        usercreation.first_name = request.POST.get('empName')
        usercreation.save()
        obj.save()
        if obj.pk is not None:
            try:
                eid=models.autogenerate.objects.get(id=1)
                eid.empid=int(eid.empid)+1
                eid.save()
            except Exception as error:
                print(error)
            
            messages.success(request, "Employee Created Successfully !")
            return redirect('employee_service')         

    return render(request, 'employee_entry.html' , {'data': data})


@login_required
def employee_service(request):
    if request.method=='GET':
        empInfo=models.Employee.objects.values('emp_id','emp_name','emp_phone','emp_position')
        data={
            'emp_id': empInfo.values('emp_id').distinct(),
            'emp_name': empInfo.values('emp_name').distinct(),
            'emp_phone': empInfo.values('emp_phone').distinct(),
            'emp_position': empInfo.values('emp_position').distinct(),    
        }
        return render(request, 'employee_service.html', {'data':data})
    
    elif request.method=='POST':
        emp_id=request.POST.get('empId')
        emp_name=request.POST.get('empName')
        emp_phone=request.POST.get('empPhone')
        emp_position=request.POST.get('position')

        condition ={}
        if emp_id is not None and emp_id != "":
            condition['emp_id'] = emp_id
        if emp_name is not None and emp_name!="":
            condition['emp_name'] = emp_name
        if emp_phone is not None and emp_phone!="":
            condition['emp_phone'] = emp_phone
        if emp_position is not None and emp_position!="":
            condition['emp_position'] = emp_position

        if condition:
            filter_data=models.Employee.objects.filter(**condition)
            if filter_data.exists():
                table_data = f'''
                            <table class="table">
                               <thead class="bg-dark">
                                    <th class="text-white p-3">S.No.</th>
                                    <th class="text-white p-3">Employee ID</th>
                                    <th class="text-white p-3">Joining Date</th>
                                    <th class="text-white p-3">Employee Name</th>
                                    <th class="text-white p-3">Date  of  Birth</th>
                                    <th class="text-white p-3">Gender</th>
                                    <th class="text-white p-3">Maritial Status</th>
                                    <th class="text-white p-3">Nationality</th>
                                    <th class="text-white p-3">Blood Group</th>
                                    <th class="text-white p-3">Phone number</th>
                                    <th class="text-white p-3">E-mail.</th>
                                    <th class="text-white p-3">Address</th>
                                    <th class="text-white p-3">Position</th>
                                    <th class="text-white p-3">Monthly Salary</th>
                                    <th class="text-white p-3">Educational qualifications</th>
                                    <th class="text-white p-3">Emergency Contact Number</th>
                                    <th colspan="2" class="text-white p-3">Action</th>
                              </thead>
                              <tbody>
                        '''
                sno = 0
                for x in filter_data:
                    sno += 1
                    table_data += '<tr>'
                    table_data += f'<td>{str(sno)}</td>'
                    table_data += f'<td>{x.emp_id}</td>'
                    table_data += f'<td>{x.date_joined}</td>'
                    table_data += f'<td>{x.emp_name}</td>'
                    table_data += f'<td>{x.dob}</td>'
                    table_data += f'<td>{x.gender}</td>'
                    table_data += f'<td>{x.marital_status}</td>'
                    table_data += f'<td>{x.nationality}</td>'
                    table_data += f'<td>{x.blood_group}</td>'
                    table_data += f'<td>{x.emp_phone}</td>'
                    table_data += f'<td>{x.email}</td>'
                    table_data+= f'<td>{x.present_address}</td>'
                    table_data += f'<td>{x.emp_position}</td>'
                    table_data += f'<td>{x.emp_salary}</td>'
                    table_data += f'<td>{x.education}</td>'
                    table_data += f'<td>{x.emergency_contact}</td>'

                    table_data+=f"<td><a href='\employee-update/{x.id}/action/'><button>Edit</button></a></td>"
                    table_data+=f"<td><a href='\employe-delete/{x.id}/action/Delete'><button>Delete</button></a></td>"
                    table_data += '</tr>'
                table_data += '</tbody></table>'

                success_data = {
                    'table_data' :table_data
                }
                return http.JsonResponse(success_data, safe=False)
            else:
                table_data = f'''
                <div class="alert alert-warning fs-4">No Records Found !</div>
                '''   
                success_data = {
                    'table_data' :table_data
                }
                return http.JsonResponse(success_data, safe=False) 
        else:
            table_data = f'''
                <div class="alert alert-warning fs-4">At Least Select One Condition !</div>
                '''   
            success_data = {
                'table_data' :table_data
            }
            return http.JsonResponse(success_data, safe=False) 
        

@login_required    
def employee_update(request,getdata):
    updateData=models.Employee.objects.get(id=getdata) 
    if request.method == 'POST':
        obj=models.Employee.objects.get(id=getdata)
        obj.emp_name=request.POST.get("empName")
        obj.dob=request.POST.get("dob")
        obj.gender=request.POST.get("gender")
        obj.marital_status=request.POST.get("maritalStatus")
        obj.nationality=request.POST.get("nationality")
        obj.blood_group=request.POST.get("bloodGroup")
        obj.emp_phone=request.POST.get("empPhone")
        obj.email=request.POST.get("email")
        obj.present_address=request.POST.get("presentAddress")
        obj.emp_position=request.POST.get("empPosition")
        obj.emp_salary=request.POST.get("empSalary")
        obj.education=request.POST.get("education")
        obj.emergency_contact=request.POST.get("emergencyContact")
        obj.emp_photo=request.POST.get("empPhoto")
        obj.save()
        if obj.pk is not None:
            messages.success(request, "Employee Information Updted Successfully !")
            return redirect('employee_service')
    return render(request,'employee_update.html', {'updateData':updateData})

@login_required
def employee_delete(request, getdata):
    deleteData= models.Employee.objects.get(id=getdata)
    deleteData.delete()
    return redirect('employee_service')



@login_required
def supplier_entry(request):
    data ={
        'title' : 'Supplier Entry'
    }
    try:
        sid = models.autogenerate.objects.get(id=1).supid
        if int(sid) < 10:
            sup_id = 'SUP-00' + str(int(sid) +1)
        elif int(sid) < 100:
            sup_id = 'SUP-0' + str(int(sid) +1)
        else:
            sup_id = 'SUP-' + str(int(sid) +1)
        data['supid'] = sup_id
    except models.autogenerate.DoesNotExist:
        print('Data not found')

    if request.method == "POST":
        obj = models.Supplier()
        obj.supplier_id = request.POST.get('supplierId')
        obj.supplier_name = request.POST.get('supplierName')
        obj.contact_person=request.POST.get('contactPerson')
        obj.phone_number=request.POST.get('phone')
        obj.email_address=request.POST.get('email')
        obj.company_address=request.POST.get('address')
        obj.gst_number=request.POST.get('gstNumber')
        obj.pan_number=request.POST.get('panNumber')
        obj.bank_account_number=request.POST.get('accountNumber')
        obj.ifsc_code=request.POST.get('ifsc')
        obj.medicine_categories=request.POST.get('categories')
        obj.lience_number=request.POST.get('licenseNumber')
        obj.status=request.POST.get('status')
        obj.save()
        if obj.pk is not None:
            try:
                sid = models.autogenerate.objects.get(id=1)
                sid.supid = int(sid.supid) +1
                sid.save()
            except Exception as error:
                print(error)
            messages.success(request, "Supplier Created Successfully !")
            return redirect('supplier_service')

    return render(request,'supplier_entry.html', {'data':data})


@login_required
def supplier_service(request):
    if request.method == 'GET':
        supplierInfo = models.Supplier.objects.values('supplier_id','supplier_name','contact_person','phone_number','medicine_categories','lience_number')
        data={
            'supplier_id': supplierInfo.values('supplier_id').distinct(),
            'supplier_name': supplierInfo.values('supplier_name').distinct(),
            'contact_person': supplierInfo.values('contact_person').distinct(),
            'phone_number': supplierInfo.values('phone_number').distinct(),
            'medicine_categories': supplierInfo.values('medicine_categories').distinct(),
            'lience_number': supplierInfo.values('lience_number').distinct(),
        }
       
        # id_Options = '<option value="" selected disabled >Select Supplier id</option>'
        # for x in supplierId:
        #     id_Options += "<option value='"+str(x['supplier_id'])+"'>"+str(x['supplier_id'])+"</option>"  
   
        return render(request,'supplier_service.html' , {'data':data})
    elif request.method=='POST':
        supplier_id=request.POST.get('supplierId')
        supplier_name=request.POST.get('supplierName')
        contact_person=request.POST.get('contactPerson')
        phone_number=request.POST.get('supplierPhone')
        medicine_categories=request.POST.get('medicineCategories')
        lience_number=request.POST.get('licenseNumber')

        condition ={}
        if supplier_id is not None and supplier_id != "":
            condition['supplier_id'] = supplier_id
        if supplier_name is not None and supplier_name!="":
            condition['supplier_name'] = supplier_name
        if contact_person is not None and contact_person!="":
            condition['contact_person'] = contact_person
        if phone_number is not None and phone_number!="":
            condition['phone_number'] = phone_number
        if medicine_categories is not None and medicine_categories!="":
            condition['medicine_categories'] = medicine_categories
        if lience_number is not None and lience_number!="":
            condition['lience_number'] = lience_number
        if condition:
            filter_data=models.Supplier.objects.filter(**condition)
            if filter_data.exists():
                table_data = f'''
                            <table class="table">
                                <thead class="bg-dark">
                                    <th class="text-white p-3">S.No.</th>
                                    <th class="text-white p-3">Supplier&nbsp;ID</th>
                                    <th class="text-white p-3">Supplier&nbsp;Name</th>
                                    <th class="text-white p-3">Contact&nbsp;Person&nbsp;Name</th>
                                    <th class="text-white p-3">Contact&nbsp;No.</th>
                                    <th class="text-white p-3">E&nbsp;Mail&nbsp;ID</th>
                                    <th class="text-white p-3">Address</th>
                                    <th class="text-white p-3">GST&nbsp;NO.</th>
                                    <th class="text-white p-3">Pan&nbsp;No.</th>
                                    <th class="text-white p-3">Bank&nbsp;Account&nbsp;NO.</th>
                                    <th class="text-white p-3">IFSC&nbsp;Code</th>
                                    <th class="text-white p-3">Medicine&nbsp;Category</th>
                                    <th class="text-white p-3">License&nbsp;No.</th>
                                    <th class="text-white p-3">Staus</th>
                                    <th colspan="2" class="text-white p-3">Action</th>
                                </thead>
                                <tbody>
                        '''
                sno = 0
                for x in filter_data:
                    sno += 1
                    table_data += '<tr>'
                    table_data += f'<td>{str(sno)}</td>'
                    table_data += f'<td>{x.supplier_id}</td>'
                    table_data += f'<td>{x.supplier_name}</td>'
                    table_data += f'<td>{x.contact_person}</td>'
                    table_data += f'<td>{x.phone_number}</td>'
                    table_data += f'<td>{x.email_address}</td>'
                    table_data += f'<td>{x.company_address}</td>'
                    table_data += f'<td>{x.gst_number}</td>'
                    table_data += f'<td>{x.pan_number}</td>'
                    table_data += f'<td>{x.bank_account_number}</td>'
                    table_data += f'<td>{x.ifsc_code}</td>'
                    table_data += f'<td>{x.medicine_categories}</td>'
                    table_data += f'<td>{x.lience_number}</td>'
                    if x.status:
                        table_data += f'<td style="min-width:8rem;"><li class="text-success">Active</li></td>'
                    else:
                        table_data += f'<td style="min-width:8rem;"><li class="text-danger">Inactive</li></td>'

                    table_data += f"<td><a href='\supplier-update/{x.id}/action/'><button>Edit</button></a></td>"
                    table_data += f"<td><a href='\supplier-delete/{x.id}/action/Delete/'><button>Delete</button></a></td>"
                    table_data += '</tr>'
                table_data += '</tbody></table>'

                success_data = {
                    'table_data' :table_data
                }
                return http.JsonResponse(success_data, safe=False)
            success_data = {
                    'table_data' :table_data
                }

@login_required
def suplierUpdate(request, getdata):
    updateData = models.Supplier.objects.get(id=getdata)
    if request.method == 'POST':
        obj = models.Supplier.objects.get(id=getdata)
        obj.supplier_name = request.POST.get('supplierName')
        obj.contact_person=request.POST.get('contactPerson')
        obj.phone_number=request.POST.get('phone')
        obj.email_address=request.POST.get('email')
        obj.company_address=request.POST.get('address')
        obj.gst_number=request.POST.get('gstNumber')
        obj.pan_number=request.POST.get('panNumber')
        obj.bank_account_number=request.POST.get('accountNumber')
        obj.ifsc_code=request.POST.get('ifsc')
        obj.medicine_categories=request.POST.get('categories')
        obj.lience_number=request.POST.get('licenseNumber')
        obj.status=request.POST.get('status')
        obj.save()
        if obj.pk is not None:
            messages.success(request, "Supplier Updted Successfully !")
            return redirect('supplier_service')
    return render(request, 'supplier_update.html', {'updateData':updateData})

@login_required
def supplierDelete(request, getdata):
    updateData = models.Supplier.objects.get(id=getdata)
    updateData.delete()
    return redirect('supplier_service')



@login_required
def medicine_entry(request):
    data={
        'title' : 'Medicine Entry'
    }
    try:
        medid=models.autogenerate.objects.get(id=1).mid
        if int(medid)<10:
            med_id='MED-00' + str(int(medid) +1)
        elif int(medid)<100:
            med_id='MED-0'+ str(int(medid)+1)
        else:
            med_id='MED-'+ str(int(medid)+1)
        data['mid'] = med_id
    except models.autogenerate.DoesNotExist:
        print("Data not found")

    if request.method == "POST":
        obj=models.Medicine()
        obj.medicine_id=request.POST.get("medicineId")
        obj.medicine_name=request.POST.get("medicineName")
        obj.description=request.POST.get("description")
        obj.category=request.POST.get("category")
        obj.unit_type=request.POST.get("unitType")
        obj.composition=request.POST.get("composition")
        obj.manufacturer=request.POST.get("manufacturer")
        obj.save()
        if obj.pk is not None:
            try:
                medid=models.autogenerate.objects.get(id=1)
                medid.mid=int(medid.mid)+1
                medid.save()
            except Exception as error:
                print(error)
            messages.success(request, "Medicine Created Successfully !")
            return redirect('medicine_search')
    
    return render(request,'medicine.html' , {'data':data})


@login_required
def medicine_search(request):
    if request.method=='GET':
        medicineInfo=models.Medicine.objects.values('medicine_id','medicine_name','category','manufacturer','unit_type')
        data = {
            'medicine_id' : medicineInfo.values('medicine_id').distinct(),
            'medicine_name' : medicineInfo.values('medicine_name').distinct(),
            'category' : medicineInfo.values('category').distinct(),
            'manufacturer' : medicineInfo.values('manufacturer').distinct(),
            'unit_type' : medicineInfo.values('unit_type').distinct()
        }
        return render(request,'medicine_search.html' , {'data':data})
    
    elif request.method=='POST':
        med_id=request.POST.get('medicineId')
        med_name=request.POST.get('medicineName')
        med_category=request.POST.get('category')
        mfg_name=request.POST.get('manufacturer')
        unit=request.POST.get('unitType')

        condition={}
        if med_id is not None and med_id !="":
            condition['medicine_id']= med_id
        if med_name is not None and med_name != "":
            condition['medicine_name'] = med_name
        if med_category is not None and med_category!="":
            condition['category'] = med_category
        if mfg_name is not None and mfg_name!="":
            condition['manufacturer'] = mfg_name
        if unit is not None and unit!="":
            condition['unit_type'] = unit
        
        if condition:
            filter_data=models.Medicine.objects.filter(**condition)
            if filter_data.exists():
                table_data = f'''
                            <table class="table">
                              <thead class="bg-dark">
                                 <th class="text-white p-3">S.No.</th>
                                 <th class="text-white p-3">Medicine ID</th>
                                 <th class="text-white p-3">Medicine Name</th>
                                 <th class="text-white p-3">Description</th>
                                 <th class="text-white p-3">Category</th>
                                 <th class="text-white p-3">Unit Type</th>
                                 <th class="text-white p-3">Composition</th>
                                 <th class="text-white p-3">Manufacturer Name</th>
                                 <th colspan="2" class="text-white p-3">Action</th>
                             </thead>
                            <tbody>
                    '''
                sno = 0
                for x in filter_data:
                    sno += 1
                    table_data += '<tr>'
                    table_data += f'<td>{str(sno)}</td>'
                    table_data += f'<td>{x.medicine_id}</td>'
                    table_data += f'<td>{x.medicine_name}</td>'
                    table_data += f'<td>{x.description}</td>'
                    table_data += f'<td>{x.category}</td>'
                    table_data += f'<td>{x.unit_type}</td>'
                    table_data += f'<td>{x.composition}</td>'
                    table_data += f'<td>{x.manufacturer}</td>'
                    
                    table_data+=f"<td><a href='\medicine-update/{x.id}/action/'><button>Edit</button></a></td>"
                    table_data+=f"<td><a href='\medicine-delete/{x.id}/action/Delete'><button>Delete</button></a></td>"
                    table_data += '</tr>'
                table_data += '</tbody></table>'

                success_data = {
                    'table_data' :table_data
                }
                return http.JsonResponse(success_data, safe=False)
            else:
                table_data = f'''
                <div class="alert alert-warning fs-4">No Records Found !</div>
                '''   
                success_data = {
                    'table_data' :table_data
                }
                return http.JsonResponse(success_data, safe=False) 
        else:
            table_data = f'''
                <div class="alert alert-warning fs-4">At Least Select One Condition !</div>
                '''   
            success_data = {
                'table_data' :table_data
            }
            return http.JsonResponse(success_data, safe=False)

@login_required
def medicine_update(request,getdata):
    updateData=models.Medicine.objects.get(id=getdata) 
    if request.method == 'POST':
        obj=models.Medicine.objects.get(id=getdata)
        obj.medicine_id=request.POST.get("medicineName")
        obj.medicine_name=request.POST.get("medicineName")
        obj.description=request.POST.get("description")
        obj.category=request.POST.get("category")
        obj.unit_type=request.POST.get("unitType")
        obj.composition=request.POST.get("composition")
        obj.manufacturer=request.POST.get("manufacturer")
        obj.save()
        if obj.pk is not None:
            messages.success(request, "Medicine Updated Successfully !")
            return redirect('medicine_search')
    return render(request,'medicine_update.html', {'updateData':updateData})


@login_required
def medicine_delete(request, getdata):
    deleteData= models.Medicine.objects.get(id=getdata)
    deleteData.delete()
    return redirect('medicine_search')
    


@login_required
def emp_payment(request):
    if request.user.is_superuser:
        emp_details = models.Employee.objects.values('emp_id', 'emp_name')
        if request.method == "POST":
            emp_id = request.POST.get('employeeId')
            obj = models.EmployeePayment()
            obj.payment_id=request.POST.get("paymentId")
            obj.emp_id = models.Employee.objects.get(emp_id=emp_id)
            obj.payment_date=request.POST.get("paymentDate")
            obj.payment_month=request.POST.get("paymentMonth")
            obj.net_salary=request.POST.get("netSalary")
            obj.payment_mode=request.POST.get("paymentMode")
            obj.remarks=request.POST.get("remarks")
            obj.save()
            if obj.pk is not None:
                messages.success(request, "Employee Payment Successful !")
                return redirect('emp_payment_service')

        return render(request,'emp_payment.html', {'emp_details':emp_details})
    else:
        messages.warning(request, 'You are not the Authorized Person to access this page')
        return redirect('index')


@login_required
def emp_payment_service(request):
    if request.user.is_superuser:
        if request.method=='GET':
            paymentInfo=models.EmployeePayment.objects.values('payment_id','emp_id','payment_date','payment_month')
            data = {
                'payment_id' : paymentInfo.values('payment_id').distinct(),
                'emp_id' : paymentInfo.values('emp_id').distinct(),
                'paydate' : paymentInfo.values('payment_date').distinct(),
                'month' : paymentInfo.values('payment_month').distinct()
            }
            
            return render(request,'employee_payment_service.html' , {'data':data})
    else:
        messages.warning(request, 'You are not the Authorized Person to access this page')
        return redirect('index')


@login_required
def purchase_details(request):
    if request.method == 'GET':
        supplierName = models.Supplier.objects.values('supplier_id','supplier_name')
        MedicineName=models.Medicine.objects.values('medicine_id','medicine_name')
        med_options = '<option value="" selected disabled >Select Medicine Name</option>'
        for x in MedicineName:
           med_options += "<option value='"+str(x['medicine_id'])+"'>"+str(x['medicine_name'])+"</option>"  
        medicineID = request.GET.get('medID')
        if medicineID is not None:
            medicineDetails = models.Medicine.objects.get(medicine_id=medicineID)
            row_data = f'<tr>'
            row_data += f'<td ><input readonly type="text" name="medicine_id" id="medicine_id" class="form-control p-2" placeholder="Medicine ID" value="{medicineDetails.medicine_id}" required></td>'
            row_data += f'<td>{medicineDetails.medicine_name}</td>'
            row_data += f'<td><input type="text" name="batch_no" id="batch_no" class="form-control p-2" placeholder="Batch No." required></td>'
            row_data += f'<td><input type="date" name="mfgDate" id="mfgDate" class="form-control p-2" required></td>'
            row_data += f'<td><input type="date" name="expDate" id="expDate" class="form-control p-2" required></td>'
            row_data += f'<td><input type="text" name="uPrice" id="uPrice" class="form-control p-2" oninput="unitCalculation(this)" placeholder="Unit Price" required></td>'
            row_data += f'<td><input type="text" name="sellingPrice" id="salePrice" class="form-control p-2"  placeholder="Selling Price" required></td>'
            row_data += f'<td><input type="text" name="qty" id="qty" class="form-control p-2" placeholder="Quantity" oninput="unitCalculation(this)" required></td>'
            row_data += f'<td><input type="text" readonly name="total" id="total" class="form-control p-2" value="00" placeholder="Total" required></td>'
            row_data += f'</tr>'
            return http.JsonResponse(row_data, safe=False)
        return render(request,'purchase_details.html', {'supplierName':supplierName, 'med_options':med_options})
    elif request.method == "POST":
        print(request.POST)
        purchase_id=request.POST.get("purchaseId")
        purchase_date=request.POST.get("purchaseDate")
        supplier=request.POST.get("suppliername")
        invoice=request.POST.get("invoiceNumber")
        medicine_id=request.POST.getlist("medicine_id")
        batch=request.POST.getlist("batch_no")
        mfgDate=request.POST.getlist("mfgDate")
        expDate=request.POST.getlist("expDate")
        uPrice=request.POST.getlist("uPrice")
        sPrice=request.POST.getlist("sellingPrice")
        qty=request.POST.getlist("qty")
        total=request.POST.getlist("total")
        totalCost=request.POST.get("totalCost")
        tax=request.POST.get("tax")
        finalAmount=request.POST.get("finalAmount")
        paymentMode=request.POST.get("paymentMode")
        remarks=request.POST.get("remarks")

        obj = models.Purchase()
        obj.purchase_id=purchase_id
        obj.supplier_id=models.Supplier.objects.get(supplier_id=supplier)
        obj.invoice_no=invoice
        obj.purchase_date=purchase_date
        obj.gross_total=totalCost
        obj.tax=tax
        obj.final_amount=finalAmount
        obj.remarks=remarks
        obj.payment_mode = paymentMode
        obj.save()
        sno = 0
        for x in medicine_id:
            obj2 = models.PurchaseItem()
            try:
                stock_data = models.Stock.objects.get(batch_no=batch[sno], medicine_id=medicine_id[sno])
                stock_data.current_qty = int(stock_data.current_qty) + qty[sno]
                stock_data.save()
            except models.Stock.DoesNotExist:
                obj3 = models.Stock()
                obj3.medicine_id = models.Medicine.objects.get(medicine_id=medicine_id[sno])
                obj3.medicine_name = models.Medicine.objects.get(medicine_id=medicine_id[sno]).medicine_name
                obj3.batch_no = batch[sno]
                obj3.expiry_date = expDate[sno]
                obj3.sPrice = sPrice[sno]
                obj3.current_qty = qty[sno]
                obj3.save()
                pass
            obj3=models.Stock()
            obj2.purchhase_id = models.Purchase.objects.get(purchase_id=purchase_id)
            obj2.medicine_id = models.Medicine.objects.get(medicine_id=medicine_id[sno])
            obj2.batch_no = batch[sno]
            obj2.mfg_date = mfgDate[sno]
            obj2.expiry_date = expDate[sno]
            obj2.unit_cost = uPrice[sno]
            obj2.sellingPrice = sPrice[sno]
            obj2.quantituy = qty[sno]
            obj2.line_amount = total[sno]
            obj2.save()
            sno += 1
        messages.success(request, "Purchase Successful !")
        return redirect('purchase_service')
    

@login_required
def purchase_service(request):
    if request.method=='GET':
      purchase_details = models.Purchase.objects.values('purchase_id', 'supplier_id', 'invoice_no')
      itemDetails = models.PurchaseItem.objects.values('medicine_id','batch_no')
      data = {
            'purchase_id': purchase_details.values('purchase_id').distinct(),
            'supplier_id': purchase_details.values('supplier_id', 'supplier_id__supplier_name').distinct(),
            'invoice_no': purchase_details.values('invoice_no').distinct(),
            'medicine_id': itemDetails.values('medicine_id' , 'medicine_id__medicine_name').distinct(),
            'batch_no': itemDetails.values('batch_no').distinct()     
        }
      return render(request,'purchase_service.html' , {'data':data})
    
    elif request.method=='POST':
        purchase_id=request.POST.get('purchaseId')
        supplier_id=request.POST.get('supplierName')
        invoice_no=request.POST.get('invoiceNumber')
        medicine_id=request.POST.get('medicineName')
        batch_no=request.POST.get('batchNumber')

        condition={}
        if purchase_id is not None and purchase_id !="":
            condition['purchhase_id__purchase_id']=purchase_id
        if supplier_id is not None and supplier_id !="":
            condition['purchhase_id__supplier_id']=supplier_id
        if invoice_no is not None and invoice_no !="":
            condition['purchhase_id__invoice_no']=invoice_no
        if medicine_id is not None and medicine_id !="":
            condition['medicine_id']=medicine_id
        if batch_no is not None and batch_no !="":
            condition['batch_no']=batch_no
        
        if condition:
            filtered_items = models.PurchaseItem.objects.filter(**condition).select_related(
                'purchhase_id', 'purchhase_id__supplier_id', 'medicine_id'
            )

            unique_purchases = {}
            for item in filtered_items:
                pid = item.purchhase_id.purchase_id
                if pid not in unique_purchases:
                    unique_purchases[pid] = {
                        "purchase": item.purchhase_id,
                        "items": []
                    }
                unique_purchases[pid]["items"].append(item)

            table_data = '''
                <table class="table">
                <thead class="bg-dark">
                    <th class="text-white p-3">S.No.</th>
                    <th class="text-white p-3">Purchase&nbsp;ID</th>
                    <th class="text-white p-3">Purchase&nbsp;Date</th>
                    <th class="text-white p-3">Supplier&nbsp;Name</th>
                    <th class="text-white p-3">Invoice&nbsp;Number</th>
                    <th class="text-white p-3">Purchase&nbsp;Details</th>
                    <th class="text-white p-3">Gross&nbsp;Total</th>
                    <th class="text-white p-3">Tax&nbsp;%</th>
                    <th class="text-white p-3">Final&nbsp;Amount</th>
                    <th class="text-white p-3">Payment&nbsp;Mode</th>
                </thead>
                <tbody>
            '''

            for sno, (pid, data) in enumerate(unique_purchases.items(), 1):
                p = data["purchase"]
                table_data += '<tr>'
                table_data += f'<td>{sno}</td>'
                table_data += f'<td>{p.purchase_id}</td>'
                table_data += f'<td>{p.purchase_date}</td>'
                table_data += f'<td>{p.supplier_id.supplier_name}</td>'
                table_data += f'<td>{p.invoice_no}</td>'
                
                # Item details (inner table)
                table_data += '<td>'
                for item in data["items"]:
                    table_data += '<div style="width:28rem;">'
                    table_data += '<ul style="display:grid; grid-template-columns:auto auto;">'
                    table_data += f'<li>Medicine - {item.medicine_id.medicine_name}</li>'
                    table_data += f'<li>Batch - {item.batch_no}</li>'
                    table_data += f'<li>Qty - {item.quantituy}</li>'
                    table_data += f'<li>MFG - {item.mfg_date}</li>'
                    table_data += f'<li>EXP - {item.expiry_date}</li>'
                    table_data += f'<li>Unit - {item.unit_cost}</li>'
                    table_data += f'<li>Selling - {item.sellingPrice}</li>'
                    table_data += f'<li>Total - {item.line_amount}</li>'
                    table_data += '</ul></div>'
                table_data += '</td>'

                table_data += f'<td>{p.gross_total}</td>'
                table_data += f'<td>{p.tax}</td>'
                table_data += f'<td>{p.final_amount}</td>'
                table_data += f'<td>{p.payment_mode}</td>'
                table_data += '</tr>'

            table_data += '</tbody></table>'

            success_data = {
                    'table_data' :table_data
                }
        return http.JsonResponse(success_data, safe=False) 
    success_data = {
                    'table_data' :table_data
                }


@login_required
def order_details(request):
      if request.method == 'GET':
        customerName = models.Customer.objects.values('cust_id','cust_name')
        MedicineName=models.Stock.objects.values('medicine_id', 'medicine_name').distinct()
        medicineID = request.GET.get('medID')
        if medicineID is not None:
            stockDetails = models.Stock.objects.filter(medicine_id=medicineID)
            batchopt ='<option selected disabled value=""> Select Batch No. </option>'
            for x in stockDetails:
                print(x.current_qty)
                if x.current_qty == 0 or x.current_qty == 00:
                    pass
                else:
                    batchopt += f'<option value="{x.batch_no}">{x.batch_no} - {x.expiry_date}</option>'
            ajaxdata = {
                'batchopt' :batchopt
            }
            return http.JsonResponse(ajaxdata, safe=False)
        
        batchId=request.GET.get('batch')
        medicine=request.GET.get('medicine')
        if batchId is not None and medicine is not None:
            try:
                medicineDetails = models.Stock.objects.get(medicine_id=medicine,batch_no=batchId )
                row_data = f'<tr>'
                row_data += f'<td hidden ><input readonly type="text" name="medicine_id" id="medicine_id" class="form-control p-2" placeholder="Medicine ID" value="{medicineDetails.medicine_id.medicine_id}" required></td>'
                row_data += f'<td>{medicineDetails.medicine_id.medicine_name}</td>'
                row_data += f'<td><input readonly type="text" name="batch_no" id="batch_no" class="form-control p-2" placeholder="Batch No." value="{medicineDetails.batch_no}" required></td>'
                row_data += f'<td><input readonly type="text" name="available" id="available" class="form-control p-2" placeholder="Available Quantity" value="{medicineDetails.current_qty}" required></td>'
                row_data += f'<td><input type="text" name="qty" id="qty" class="form-control p-2" placeholder="Quantity" oninput="unitCalculation(this)" required></td>'
                row_data += f'<td><input readonly type="text" name="sPrice" id="sPrice" class="form-control p-2" oninput="unitCalculation(this)" placeholder="Unit Price" value="{medicineDetails.sPrice}" required></td>'
                row_data += f'<td><input type="text" readonly name="total" id="total" class="form-control p-2" value="00" placeholder="Total" required></td>'
                row_data += f'</tr>'
                return http.JsonResponse(row_data, safe=False)
            except models.PurchaseItem.DoesNotExist:
                responsedata = {
                    'success' : False,
                    'icon': 'info',
                    'title' : 'Item Dose no exist !',
                    'message' : 'Medicine is not in the stock !'
                }
                return http.JsonResponse(responsedata, safe=False)
        return render(request,'order_details.html', {'customerName':customerName, 'med_options':MedicineName})
      elif request.method == "POST":
        #   print(request.POST)
          order_id=request.POST.get("orderId")
          cust_name=request.POST.get("customername")
          order_date=request.POST.get("orderDate")
          medicine_id=request.POST.getlist("medicine_id")
          batch_no=request.POST.getlist("batch_no")
          gross_amount=request.POST.get("totalCost")
          discount=request.POST.get("discount")
          final_amount=request.POST.get("finalAmount")
          payment_mode=request.POST.get("paymentMode")
          payment_status=request.POST.get("paymentStatus")
          order_status=request.POST.get("orderStatus")
          qty=request.POST.getlist("qty")
          sPrice=request.POST.getlist("sPrice")
          total=request.POST.getlist("total")
          print(qty)
          obj=models.Sales()
          obj.order_id=order_id
          obj.customer_id=models.Customer.objects.get(cust_id=cust_name)
          obj.order_date=order_date
          obj.discount=discount
          obj.gross_total=gross_amount
          obj.total_amount=final_amount
          obj.payment_method=payment_mode
          obj.payment_status=payment_status
          obj.order_status=order_status
          obj.save()
          sno = 0
          for x in medicine_id:
            obj2 = models.SaleItem()
            stock_data = models.Stock.objects.get(batch_no=batch_no[sno], medicine_id=medicine_id[sno])

            stock_data.current_qty = int(stock_data.current_qty) - int(qty[sno])
            stock_data.save()

            obj2.order_id=models.Sales.objects.get(order_id=order_id)
            obj2.medicine_id=models.Medicine.objects.get(medicine_id=medicine_id[sno])
            obj2.batch_no=batch_no[sno]
            obj2.quantity=qty[sno]
            obj2.selling_price=sPrice[sno]
            obj2.line_amount=total[sno]
            obj2.save()
            sno+= 1
          return redirect('order_service')
            
          

    

@login_required
def order_service(request):
    return render(request,'order_service.html')


@login_required
def stock_details(request):
    if request.method=='GET':
        stockInfo=models.Stock.objects.values('medicine_id','medicine_name','batch_no','expiry_date','sPrice','current_qty')
        data = {
            'medicine_id' : stockInfo.values('medicine_id').distinct(),
            'medicine_name' : stockInfo.values('medicine_name').distinct(),
            'batch_no' : stockInfo.values('batch_no').distinct(),
            'expiry_date' : stockInfo.values('expiry_date').distinct(),
            'sPrice' : stockInfo.values('sPrice').distinct(),
            'current_qty' : stockInfo.values('current_qty').distinct(),
        }
        return render(request,'stock.html' , {'data':data})
    
    elif request.method=='POST':
        med_id=request.POST.get('medicineId')
        med_name=request.POST.get('medicineName')
        batch_no=request.POST.get('batch')
      
        condition={}
        if med_id is not None and med_id !="":
            condition['medicine_id']= med_id
        if med_name is not None and med_name != "":
            condition['medicine_name'] = med_name
        if batch_no is not None and batch_no!="":
            condition['batch_no'] = batch_no
      
       
        if condition:
            filter_data=models.Stock.objects.filter(**condition)
            if filter_data.exists():
                table_data = f'''
                            <table class="table">
                              <thead class="bg-dark">
                                 <th class="text-white p-3">S.No.</th>
                                 <th class="text-white p-3">Medicine ID</th>
                                 <th class="text-white p-3">Medicine Name</th>
                                 <th class="text-white p-3">Batch Number</th>
                                 <th class="text-white p-3">Expiry date</th>
                                 <th class="text-white p-3">Selling Price</th>
                                 <th class="text-white p-3">Current Quantity</th>
                             </thead>
                            <tbody>
                    '''
                sno = 0
                for x in filter_data:
                    sno += 1
                    table_data += '<tr>'
                    table_data += f'<td>{str(sno)}</td>'
                    table_data += f'<td>{x.medicine_id.medicine_id}</td>'
                    table_data += f'<td>{x.medicine_name}</td>'
                    table_data += f'<td>{x.batch_no}</td>'
                    table_data += f'<td>{x.expiry_date}</td>'
                    table_data += f'<td>{x.sPrice}</td>'
                    table_data += f'<td>{x.current_qty}</td>'
                    table_data += '</tr>'
                table_data += '</tbody></table>'

                success_data = {
                    'table_data' :table_data
                }
                return http.JsonResponse(success_data, safe=False)
            else:
                table_data = f'''
                <div class="alert alert-warning fs-4">No Records Found !</div>
                '''   
                success_data = {
                    'table_data' :table_data
                }
                return http.JsonResponse(success_data, safe=False) 
        else:
            table_data = f'''
                <div class="alert alert-warning fs-4">At Least Select One Condition !</div>
                '''   
            success_data = {
                'table_data' :table_data
            }
            return http.JsonResponse(success_data, safe=False)


    



   

 