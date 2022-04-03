from ast import ExceptHandler
from django.shortcuts import render,redirect,reverse
from django.contrib import messages
from hospitalmanagement.settings import LOG_PATH
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models import Q

import logging
import os

#log files
logFileName= os.path.join(LOG_PATH, str(datetime.now().strftime("%m_%d_%Y") + ".log"))
logging.basicConfig(filename=logFileName,  format='%(asctime)s %(message)s', level=logging.ERROR)

# Create your views here.
def home_view(request):
    try:
        if request.user.is_authenticated:
            return HttpResponseRedirect('afterlogin')
        return render(request,'hospital/index.html')
    except Exception as e:
        logging.error("error in home_view, error is {}".format(e)) 
        return render(request,'hospital/index.html')   

def adminclick_view(request):
    try:
        if request.user.is_authenticated:
            return HttpResponseRedirect('afterlogin')
        return render(request,'hospital/adminclick.html')
    except Exception as e:
        logging.error("error in adminclick_view, error is {}".format(e)) 
        return render(request,'hospital/adminclick.html')  

def doctorclick_view(request):
    try:
        if request.user.is_authenticated:
            return HttpResponseRedirect('afterlogin')
        return render(request,'hospital/doctorclick.html')
    except Exception as e:
        logging.error("error in doctorclick_view, error is {}".format(e))    
        return render(request,'hospital/doctorclick.html')

def patientclick_view(request):
    try:
        if request.user.is_authenticated:
            return HttpResponseRedirect('afterlogin')
        return render(request,'hospital/patientclick.html')
    except Exception as e:
        logging.error("error in patientclick_view,error is {}".format(e)) 
        return render(request,'hospital/patientclick.html')   

def labstaffclick_view(request):
    try:
        if request.user.is_authenticated:
            return HttpResponseRedirect('afterlogin')
        return render(request,'hospital/labstaffclick.html')
    except Exception as e:
        logging.error("error in labstaffclick,error is {}".format(e)) 
        return render(request,'hospital/labstaffclick.html')   

#--------------------for showing signup/login button for insurance-----------
def insuranceclick_view(request):
    try:
        if request.user.is_authenticated:
            return HttpResponseRedirect('afterlogin')
        return render(request,'hospital/insuranceclick.html')
    except Exception as e:
        logging.error("error in insuranceclick,error is {}".format(e)) 
        return render(request,'hospital/insuranceclick.html')   



def admin_signup_view(request):
    try:
        form=forms.AdminSigupForm()
        if request.method=='POST':
            form=forms.AdminSigupForm(request.POST)
            if form.is_valid():
                user=form.save()
                user.set_password(user.password)
                user.save()
                my_admin_group = Group.objects.get_or_create(name='ADMIN')
                my_admin_group[0].user_set.add(user)
                return HttpResponseRedirect('adminlogin')
            else:
                messages.error(request,"Admin User Exist.")
                logging.error("error in admin_signup_view with data already exist.")    
    except Exception as e:
        logging.error("error in admin_signup_view, error is {}".format(e))
        return HttpResponseRedirect('adminlogin')
    return render(request,'hospital/adminsignup.html',{'form':form})




def doctor_signup_view(request):
    try:
        userForm=forms.DoctorUserForm()
        doctorForm=forms.DoctorForm()
        mydict={'userForm':userForm,'doctorForm':doctorForm}
        if request.method=='POST':
            userForm=forms.DoctorUserForm(request.POST)
            doctorForm=forms.DoctorForm(request.POST,request.FILES)
            if userForm.is_valid() and doctorForm.is_valid():
                user=userForm.save()
                user.set_password(user.password)
                user.save()
                doctor=doctorForm.save(commit=False)
                doctor.user=user
                doctor=doctor.save()
                my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
                my_doctor_group[0].user_set.add(user)
                return HttpResponseRedirect('doctorlogin')
            else:
                messages.error(request,"Doctor User Exist.")
                logging.error("error in doctor_signup_view with data already exist.")    
    except Exception as e:
        logging.error("error in doctor_signup_view, error is {}".format(e))
        return HttpResponseRedirect('doctorlogin')

    return render(request,'hospital/doctorsignup.html',context=mydict)


def patient_signup_view(request):
    try:
        userForm=forms.PatientUserForm()
        patientForm=forms.PatientForm()
        mydict={'userForm':userForm,'patientForm':patientForm}
        if request.method=='POST':
            userForm=forms.PatientUserForm(request.POST)
            patientForm=forms.PatientForm(request.POST,request.FILES)
            if userForm.is_valid() and patientForm.is_valid():
                user=userForm.save()
                user.set_password(user.password)
                user.save()
                patient=patientForm.save(commit=False)
                patient.user=user
                patient.assignedDoctorId=request.POST.get('assignedDoctorId')
                patient=patient.save()
                my_patient_group = Group.objects.get_or_create(name='PATIENT')
                my_patient_group[0].user_set.add(user)
                return HttpResponseRedirect('patientlogin')
            else:
                messages.error(request,"Patient User Exist.")
                logging.error("error in patient_signup_view with data already exist.")    
    except Exception as e:
        logging.error("error in patient_signup_view, error is {}".format(e))
        return HttpResponseRedirect('patientlogin')

    return render(request,'hospital/patientsignup.html',context=mydict)



#---------------------creating insurance signup view
def insurance_signup_view(request):
    userForm=forms.InsuranceUserForm()
    insuranceForm=forms.InsuranceForm()
    mydict={'userForm':userForm,'insuranceForm':insuranceForm}
    if request.method=='POST':
        userForm=forms.InsuranceUserForm(request.POST)
        insuranceForm=forms.InsuranceForm(request.POST,request.FILES)
        if userForm.is_valid() and insuranceForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            insurance=insuranceForm.save(commit=False)
            insurance.user=user
            insurance=insurance.save()
            my_insurance_group = Group.objects.get_or_create(name='INSURANCE')
            my_insurance_group[0].user_set.add(user)
        return HttpResponseRedirect('insurancelogin')
    return render(request,'hospital/insurancesignup.html',context=mydict)




def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()
def is_labstaff(user):
    return user.groups.filter(name='LABSTAFF').exists()
#-----------for checking user is insurance agent
def is_insurance(user):
    return user.groups.filter(name='INSURANCE').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        accountapproval=models.Doctor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('doctor-dashboard')
        else:
            return render(request,'hospital/doctor_wait_for_approval.html')
    elif is_patient(request.user):
        accountapproval=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('patient-dashboard')
        else:
            return render(request,'hospital/patient_wait_for_approval.html')
    elif is_labstaff(request.user):
        accountapproval=models.LabStaff.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('labstaff-dashboard')
        else:
            return render(request,'hospital/labstaff_wait_for_approval.html')
#------Similarly writing code for the insurance credentials checking
    elif is_insurance(request.user):
        accountapproval=models.Insurance.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('insurance-dashboard')
        else:
            return render(request,'hospital/insurance_wait_for_approval.html')

#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    doctors=models.Doctor.objects.all().order_by('-id')
    labstaff = models.LabStaff.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    insurance=models.Insurance.objects.all().order_by('-id')

    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'doctors':doctors,
    'labstaff':labstaff,
    'patients':patients,
    'insurance':insurance,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'hospital/admin_dashboard.html',context=mydict)

# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request,'hospital/admin_doctor.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor.html',{'doctors':doctors})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request,pk):
    try:
        doctor=models.Doctor.objects.get(id=pk)
        user=models.User.objects.get(id=doctor.user_id)
        user.delete()
        doctor.delete()
        return redirect('admin-view-doctor')
    except Exception as e:
        logging.error("error in delete doctor view from hospital, error is {}".format(e))
        return redirect('admin-view-doctor')    

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_doctor_view(request,pk):
    try:
        doctor=models.Doctor.objects.get(id=pk)
        
        user=models.User.objects.get(id=doctor.user_id)

        userForm=forms.DoctorUserForm(instance=user)
        doctorForm=forms.DoctorForm(request.FILES,instance=doctor)
        mydict={'userForm':userForm,'doctorForm':doctorForm}
        if request.method=='POST':
            userForm=forms.DoctorUserForm(request.POST,instance=user)
            doctorForm=forms.DoctorForm(request.POST,request.FILES,instance=doctor)
            if userForm.is_valid() and doctorForm.is_valid():
                user=userForm.save()
                user.set_password(user.password)
                user.save()
                doctor=doctorForm.save(commit=False)
                doctor.status=True
                doctor.save()
                
                return redirect('admin-view-doctor')
    except Exception as e:
        logging.error("error in update_doctor_view, error is {}".format(e))
        return redirect('admin-view-doctor')
    return render(request,'hospital/admin_update_doctor.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    try:
        userForm=forms.DoctorUserForm()
        doctorForm=forms.DoctorForm()
        mydict={'userForm':userForm,'doctorForm':doctorForm}
        if request.method=='POST':
            userForm=forms.DoctorUserForm(request.POST)
            doctorForm=forms.DoctorForm(request.POST, request.FILES)
            if userForm.is_valid() and doctorForm.is_valid():
                user=userForm.save()
                user.set_password(user.password)
                user.save()

                doctor=doctorForm.save(commit=False)
                doctor.user=user
                doctor.status=True
                doctor.save()

                my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
                my_doctor_group[0].user_set.add(user)
                return HttpResponseRedirect('admin-view-doctor')
            else:
                logging.error("invalid form with data exist in admin doctor view")
                return HttpResponseRedirect('admin-add-doctor')
    except Exception as e:
        logging.error("error in admin add doctor view, error is {}".format(e))
        return redirect('admin-view-doctor')        
    return render(request,'hospital/admin_add_doctor.html',context=mydict)

# approving doctor
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    #those whose approval are needed
    try:
        doctors=models.Doctor.objects.all().filter(status=False)
        return render(request,'hospital/admin_approve_doctor.html',{'doctors':doctors})

    except Exception as e:
        logging.error("error in admin_approve_doctor_view,error is {}".format(e))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_doctor_view(request,pk):
    #those whose approval are needed
    try:
        doctors=models.Doctor.objects.all().filter(status=False)
        return render(request,'hospital/admin_approve_doctor.html',{'doctors':doctors})
    except Exception as e:
        logging.error("error in admin_approve_doctor_view,error is {}".format(e))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_specialisation_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor_specialisation.html',{'doctors':doctors})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request,'hospital/admin_patient.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_patient.html',{'patients':patients})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)

    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('admin-view-patient')
    return render(request,'hospital/admin_update_patient.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    try:
        userForm=forms.PatientUserForm()
        patientForm=forms.PatientForm()
        mydict={'userForm':userForm,'patientForm':patientForm}
        if request.method=='POST':
            userForm=forms.PatientUserForm(request.POST)
            patientForm=forms.PatientForm(request.POST,request.FILES)
            if userForm.is_valid() and patientForm.is_valid():
                user=userForm.save()
                user.set_password(user.password)
                user.save()

                patient=patientForm.save(commit=False)
                patient.user=user
                patient.status=True
                patient.assignedDoctorId=request.POST.get('assignedDoctorId')
                patient.save()

                my_patient_group = Group.objects.get_or_create(name='PATIENT')
                my_patient_group[0].user_set.add(user)

                return HttpResponseRedirect('admin-view-patient')

            else:
            
                logging.error("invalid form with data exist in admin view patient")
                return HttpResponseRedirect('admin-add-patient')
    except Exception as e: 
        logging.error("error in add admin patient view, error is {}".format(e))  
        return redirect('admin-view-patient')        
    return render(request,'hospital/admin_add_patient.html',context=mydict)

# ------- Admin--LabStaff--Views ------- #

# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_labstaff_view(request):
    return render(request,'hospital/admin_labstaff.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_labstaff_view(request):
    labstaff=models.LabStaff.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_labstaff.html',{'labstaff':labstaff})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_labstaff_from_hospital_view(request,pk):
    labstaff=models.LabStaff.objects.get(id=pk)
    user=models.User.objects.get(id=labstaff.user_id)
    user.delete()
    labstaff.delete()
    return redirect('admin-view-labstaff')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_labstaff_view(request,pk):
    labstaff=models.LabStaff.objects.get(id=pk)
    user=models.User.objects.get(id=labstaff.user_id)

    userForm=forms.LabStaffUserForm(instance=user)
    labstaffForm=forms.LabStaffForm(request.FILES,instance=labstaff)
    mydict={'userForm':userForm,'labstaffForm':labstaffForm}
    if request.method=='POST':
        userForm=forms.LabStaffUserForm(request.POST,instance=user)
        labstaffForm=forms.LabStaffForm(request.POST,request.FILES,instance=labstaff)
        if userForm.is_valid() and labstaffForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            labstaff=labstaffForm.save(commit=False)
            labstaff.status=True
            labstaff.save()
            return redirect('admin-view-labstaff')
    return render(request,'hospital/admin_update_labstaff.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_labstaff_view(request):
    userForm=forms.LabStaffUserForm()
    labstaffForm=forms.LabStaffForm()
    mydict={'userForm':userForm,'labstaffForm':labstaffForm}
    if request.method=='POST':
        userForm=forms.LabStaffUserForm(request.POST)
        labstaffForm=forms.LabStaffForm(request.POST, request.FILES)
        if userForm.is_valid() and labstaffForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            labstaff=labstaffForm.save(commit=False)
            labstaff.user=user
            labstaff.status=True
            labstaff.save()

            my_labstaff_group = Group.objects.get_or_create(name='LABSTAFF')
            my_labstaff_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-labstaff')
    return render(request,'hospital/admin_add_labstaff.html',context=mydict)

#------------------FOR APPROVING PATIENT BY ADMIN----------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    #those whose approval are needed
    patients=models.Patient.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_patient.html',{'patients':patients})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    patient.status=True
    patient.save()
    return redirect(reverse('admin-approve-patient'))

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-approve-patient')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_labstaff_view(request):
    #those whose approval are needed
    labstaff=models.LabStaff.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_labstaff.html',{'labstaff':labstaff})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_labstaff_view(request,pk):
    labstaff=models.LabStaff.objects.get(id=pk)
    labstaff.status=True
    labstaff.save()
    return redirect(reverse('admin-approve-labstaff'))

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_labstaff_view(request,pk):
    labstaff=models.LabStaff.objects.get(id=pk)
    user=models.User.objects.get(id=labstaff.user_id)
    user.delete()
    labstaff.delete()
    return redirect('admin-approve-labstaff')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_labstaff_specialisation_view(request):
    labstaff=models.LabStaff.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_labstaff_specialisation.html',{'labstaff':labstaff})

# ------ End ------ #

 #patient

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request,'hospital/admin_patient.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_patient.html',{'patients':patients})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request,pk):
    try:
        patient=models.Patient.objects.get(id=pk)
        user=models.User.objects.get(id=patient.user_id)
        user.delete()
        patient.delete()
        return redirect('admin-view-patient')
    except Exception as e:
        logging.error("error in delete patient view from hospital, error is {}".format(e))
        return redirect('admin-view-patient')    

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_patient_view(request,pk):
    try:

        patient=models.Patient.objects.get(id=pk)
        user=models.User.objects.get(id=patient.user_id)

        userForm=forms.PatientUserForm(instance=user)
        patientForm=forms.PatientForm(request.FILES,instance=patient)
        mydict={'userForm':userForm,'patientForm':patientForm}
        if request.method=='POST':
            userForm=forms.PatientUserForm(request.POST,instance=user)
            patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
            if userForm.is_valid() and patientForm.is_valid():
                user=userForm.save()
                user.set_password(user.password)
                user.save()
                patient=patientForm.save(commit=False)
                patient.status=True
                patient.assignedDoctorId=request.POST.get('assignedDoctorId')
                patient.save()
                return redirect('admin-view-patient')
    except Exception as e: 
        logging.error("error in update patient view, error is {}".format(e))  
        return redirect('admin-view-patient')             
    return render(request,'hospital/admin_update_patient.html',context=mydict)





@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    try:
        userForm=forms.PatientUserForm()
        patientForm=forms.PatientForm()
        mydict={'userForm':userForm,'patientForm':patientForm}
        if request.method=='POST':
            userForm=forms.PatientUserForm(request.POST)
            patientForm=forms.PatientForm(request.POST,request.FILES)
            if userForm.is_valid() and patientForm.is_valid():
                user=userForm.save()
                user.set_password(user.password)
                user.save()

                patient=patientForm.save(commit=False)
                patient.user=user
                patient.status=True
                patient.assignedDoctorId=request.POST.get('assignedDoctorId')
                patient.save()

                my_patient_group = Group.objects.get_or_create(name='PATIENT')
                my_patient_group[0].user_set.add(user)

                return HttpResponseRedirect('admin-view-patient')

            else:
            
                logging.error("invalid form with data exist in admin view patient")
                return HttpResponseRedirect('admin-add-patient')
    except Exception as e: 
        logging.error("error in add admin patient view, error is {}".format(e))  
        return redirect('admin-view-patient')        
    return render(request,'hospital/admin_add_patient.html',context=mydict)


#------------------FOR APPROVING PATIENT BY ADMIN----------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    #those whose approval are needed
    try:
        patients=models.Patient.objects.all().filter(status=False)
        return render(request,'hospital/admin_approve_patient.html',{'patients':patients})
    except Exception as e:
        logging.error("error in admin approve patient view from hospital, error is {}".format(e))
        return render(request,'hospital/admin_approve_patient.html',{'patients':patients})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_patient_view(request,pk):
    try:
        patient=models.Patient.objects.get(id=pk)
        patient.status=True
        patient.save()
        return redirect(reverse('admin-approve-patient'))
    except Exception as e:   
        logging.error("error in approve patient view from hospital, error is {}".format(e))
        return redirect(reverse('admin-approve-patient'))
        
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_patient_view(request,pk):
    try:
        patient=models.Patient.objects.get(id=pk)
        user=models.User.objects.get(id=patient.user_id)
        user.delete()
        patient.delete()
        return redirect('admin-approve-patient')
    except Exception as e:
        logging.error("error in reject_patient_view,error is {}".format(e))
        return redirect('admin-approve-patient')      

#--------------------- FOR DISCHARGING PATIENT BY ADMIN START-------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin_discharge_patient.html',{'patients':patients})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def discharge_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    days=(date.today()-patient.admitDate) #2 days, 0:00:00
    assignedDoctor=models.User.objects.all().filter(id=patient.assignedDoctorId)
    d=days.days # only how many day that is 2
    patientDict={
        'patientId':pk,
        'name':patient.get_name,
        'mobile':patient.mobile,
        'InsuranceProvider': patient.patientInsuranceProvider,
        'PolicyNumber': patient.patientPolicyNumber,
        'address':patient.address,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'todayDate':date.today(),
        'day':d,
        'assignedDoctorName':assignedDoctor[0].first_name,
    }
    if request.method == 'POST':
        feeDict ={
            'roomCharge':int(request.POST['roomCharge'])*int(d),
            'doctorFee':request.POST['doctorFee'],
            'medicineCost' : request.POST['medicineCost'],
            'OtherCharge' : request.POST['OtherCharge'],
            'total':(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        }
        patientDict.update(feeDict)
        #for updating to database patientDischargeDetails (pDD)
        pDD=models.PatientDischargeDetails()
        pDD.patientId=pk
        pDD.patientName=patient.get_name
        pDD.assignedDoctorName=assignedDoctor[0].first_name
        pDD.address=patient.address
        pDD.mobile=patient.mobile
        pDD.patientInsuranceProvider=patient.patientInsuranceProvider
        pDD.patientPolicyNumber=patient.patientPolicyNumber
        pDD.symptoms=patient.symptoms
        pDD.admitDate=patient.admitDate
        pDD.releaseDate=date.today()
        pDD.daySpent=int(d)
        pDD.medicineCost=int(request.POST['medicineCost'])
        pDD.roomCharge=int(request.POST['roomCharge'])*int(d)
        pDD.doctorFee=int(request.POST['doctorFee'])
        pDD.OtherCharge=int(request.POST['OtherCharge'])
        pDD.total=(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        pDD.save()
        return render(request,'hospital/patient_final_bill.html',context=patientDict)
    return render(request,'hospital/patient_generate_bill.html',context=patientDict)


#--------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return

def download_pdf_view(request,pk):
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict={
        'patientName':dischargeDetails[0].patientName,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'symptoms':dischargeDetails[0].symptoms,
        'patientInsuranceProvider':dischargeDetails[0].patientInsuranceProvider,
        'patientPolicyNumber':dischargeDetails[0].patientPolicyNumber,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('hospital/download_bill.html',dict)



#-----------------APPOINTMENT START--------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'hospital/admin_appointment.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    try:

        appointments=models.Appointment.objects.all().filter(status=True)
        return render(request,'hospital/admin_view_appointment.html',{'appointments':appointments})
    except Exception as e:
        logging.error("error in admin-view-appointment-view , error is {}".format(e))
        return render(request,'hospital/admin_view_appointment.html',{'appointments':appointments})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm=forms.AppointmentForm()
    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.POST.get('patientId')
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    return render(request,'hospital/admin_add_appointment.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    try:
        appointments=models.Appointment.objects.all().filter(status=False)
        return render(request,'hospital/admin_approve_appointment.html',{'appointments':appointments})
    except Exception as e:
        logging.error("error in admin-approve-appointment-view , error is {}".format(e))
        return render(request,'hospital/admin_approve_appointment.html',{'appointments':appointments})
    
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment_view(request,pk):
    try:
        appointment=models.Appointment.objects.get(id=pk)
        appointment.status=True
        appointment.save()
        return redirect(reverse('admin-approve-appointment'))
    except Exception as e:
        logging.error("error in admin-approve-appointment,error is {}".format) 
        return redirect('admin-approve-appointment')
        
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request,pk):
    try:
        appointment=models.Appointment.objects.get(id=pk)
        appointment.delete()
        return redirect('admin-approve-appointment')
    except Exception as e:
        logging.error("error in reject-appointment-view,error is {}".format) 
        return redirect('admin-approve-appointment')

#insurance admin views

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_insurance_view(request):
    return render(request,'hospital/admin_insurance.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_insurance_view(request):
    insurance=models.Insurance.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_insurance.html',{'insurance':insurance})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_insurance_from_hospital_view(request,pk):
    insurance=models.Insurance.objects.get(id=pk)
    user=models.User.objects.get(id=insurance.user_id)
    user.delete()
    insurance.delete()
    return redirect('admin-view-insurance')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_insurance_view(request,pk):
    insurance=models.Insurance.objects.get(id=pk)
    user=models.User.objects.get(id=insurance.user_id)

    userForm=forms.InsuranceUserForm(instance=user)
    InsuranceForm=forms.InsuranceForm(request.FILES,instance=insurance)
    mydict={'userForm':userForm,'insuranceForm':insuranceForm}
    if request.method=='POST':
        userForm=forms.InsuranceUserForm(request.POST,instance=user)
        insuranceForm=forms.InsuranceForm(request.POST,request.FILES,instance=insurance)
        if userForm.is_valid() and insuranceForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            insurance=insuranceForm.save(commit=False)
            insurance.status=True
            insurance.save()
            return redirect('admin-view-insurance')
    return render(request,'hospital/admin_update_insurance.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_insurance_view(request):
    userForm=forms.InsuranceUserForm()
    insuranceForm=forms.InsuranceForm()
    mydict={'userForm':userForm,'insuranceForm':insuranceForm}
    if request.method=='POST':
        userForm=forms.InsuranceUserForm(request.POST)
        insuranceForm=forms.InsuranceForm(request.POST, request.FILES)
        if userForm.is_valid() and insuranceForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            insurance=insuranceForm.save(commit=False)
            insurance.user=user
            insurance.status=True
            insurance.save()

            my_insurance_group = Group.objects.get_or_create(name='INSURANCE')
            my_insurance_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-insurance')
    return render(request,'hospital/admin_add_insurance.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_insurance_view(request):
    #those whose approval are needed
    insurance=models.Insurance.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_insurance.html',{'insurance':insurance})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_insurance_view(request,pk):
    insurance=models.Insurance.objects.get(id=pk)
    insurance.status=True
    insurance.save()
    return redirect(reverse('admin-approve-insurance'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_insurance_view(request,pk):
    insurance=models.Insurance.objects.get(id=pk)
    user=models.User.objects.get(id=pk)
    user.delete()
    insurance.delete()
    return redirect('admin-approve-insurance')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_insurance_team_view(request):
    insurance=models.Insurance.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_insurance_team.html',{'insurance':insurance})

#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    #for three cards
    patientcount=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
    patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    #for  table in doctor dashboard
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    appointments=zip(appointments,patients)
    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'patientdischarged':patientdischarged,
    'appointments':appointments,
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_dashboard.html',context=mydict)

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict={
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_patient.html',context=mydict)

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_update_patient_view(request,pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)

    userForm = forms.PatientUserForm(instance=user)
    patientForm = forms.PatientForm(request.FILES, instance=patient)
    mydict = {'userForm': userForm, 'patientForm': patientForm}
    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST, instance=user)
        patientForm = forms.PatientForm(request.POST, request.FILES, instance=patient)

        if patientForm.is_valid():
            # user = userForm.save()
            # user.set_password(user.password)
            # user.save()
            patient = patientForm.save(commit=False)
            patient.status = True
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('doctor-view-patient')
    return render(request, 'hospital/doctor_view_patient.html', context=mydict)

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def search_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    # whatever user write in search box we get in query
    query = request.GET['query']
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).filter(Q(symptoms__icontains=query)|Q(user__first_name__icontains=query))
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_prescription_view(request):
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_prescription.html',{'patients':patients,'doctor':doctor})

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_appointment.html',{'doctor':doctor})

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor})

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})


#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
#------------------------ LABSTAFF RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='labstafflogin')
@user_passes_test(is_labstaff)
def labstaff_dashboard_view(request):
    #for three cards
    patientcount=models.Patient.objects.all().filter(status=True, assignedDoctorId=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True, doctorId=request.user.id).count()
    patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()
    labtestcount=models.LabTests.objects.all().distinct().count()
    patient_labtests_inprogress = models.Patient_LabTest_Records.objects.all().filter(status='InProgress').count()
    patient_labtests_done = models.Patient_LabTest_Records.objects.all().filter(status='Done').count()
    patient_labtests_incomplete = models.Patient_LabTest_Records.objects.all().filter(status='Incomplete').count()

    #for  table in doctor dashboard
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True, user_id__in=patientid).order_by('-id')
    appointments=zip(appointments,patients)
    labtests=models.LabTests.objects.all()
    patient_labtests_records=models.Patient_LabTest_Records.objects.all().order_by('-id')[:5]



    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'patientdischarged':patientdischarged,
    'appointments':appointments,
    'labtestcount':labtestcount,
    'labtests':labtests,
    'patient_labtests_inprogress':patient_labtests_inprogress,
    'patient_labtests_done':patient_labtests_done,
    'patient_labtests_incomplete': patient_labtests_incomplete,
    'patient_labtests_records':patient_labtests_records,
    'labstaff':models.LabStaff.objects.get(user_id=request.user.id),  # for profile picture of labstaff in sidebar
    }
    return render(request,'hospital/labstaff_dashboard.html',context=mydict)



@login_required(login_url='labstafflogin')
@user_passes_test(is_labstaff)
def labstaff_patient_view(request):
    mydict={
    'labstaff':models.LabStaff.objects.get(user_id=request.user.id), #for profile picture of labstaff in sidebar
    }
    return render(request,'hospital/labstaff_patient.html',context=mydict)



@login_required(login_url='labstafflogin')
@user_passes_test(is_labstaff)
def labstaff_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    patient_labtest_records=models.Patient_LabTest_Records.objects.all()
    labstaff = models.LabStaff.objects.get(user_id=request.user.id)  # for profile picture of labstaff in sidebar
    context = {'patients':patients,'labstaff':labstaff,'patient_labtest_records':patient_labtest_records}
    return render(request,'hospital/labstaff_view_patient.html',context=context)


@login_required(login_url='labstafflogin')
@user_passes_test(is_labstaff)
def search_view(request):
    labstaff=models.LabStaff.objects.get(user_id=request.user.id) #for profile picture of labstaff in sidebar
    # whatever user write in search box we get in query
    query = request.GET['query']
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).filter(Q(symptoms__icontains=query)|Q(user__first_name__icontains=query))
    return render(request,'hospital/labstaff_view_patient.html',{'patients':patients,'labstaff':labstaff})



@login_required(login_url='labstafflogin')
@user_passes_test(is_labstaff)
def labstaff_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    labstaff=models.LabStaff.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/labstaff_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'labstaff':labstaff})


@login_required(login_url='labstafflogin')
@user_passes_test(is_labstaff)
def labstaff_labtests_view(request):
    labstaff=models.LabStaff.objects.get(user_id=request.user.id) #for profile picture of labstaff in sidebar
    return render(request,'hospital/labstaff_labtests.html',{'labstaff':labstaff})


@login_required(login_url='labstafflogin')
@user_passes_test(is_labstaff)
def labstaff_appointment_view(request):
    labstaff=models.LabStaff.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/labstaff_appointment.html',{'labstaff':labstaff})




@login_required(login_url='labstafflogin')
@user_passes_test(is_labstaff)
def labstaff_view_appointment_view(request):
    labstaff=models.LabStaff.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/labstaff_view_appointment.html',{'appointments':appointments,'labstaff':labstaff})


@login_required(login_url='labstafflogin')
@user_passes_test(is_labstaff)
def labstaff_create_labtests_view(request):
    labstaff=models.LabStaff.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    labtests=models.LabTests.objects.all()
    return render(request,'hospital/labstaff_create_labtests.html',{'labtests':labtests,'labstaff':labstaff})


@login_required(login_url='labstafflogin')
@user_passes_test(is_labstaff)
def labstaff_update_delete_labtests(request):
    labstaff = models.LabStaff.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    labtests = models.LabTests.objects.all()
    return render(request, 'hospital/labstaff_update_delete_labtests.html', {'labtests': labtests, 'labstaff': labstaff})



def labstaff_delete_appointment_view(request):
    labstaff=models.LabStaff.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/labstaff_delete_appointment.html',{'appointments':appointments,'labstaff':labstaff})



@login_required(login_url='labstafflogin')
@user_passes_test(is_labstaff)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    labstaff=models.LabStaff.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/labstaff_delete_appointment.html',{'appointments':appointments,'labstaff':labstaff})


@login_required(login_url='labstafflogin')
@user_passes_test(is_labstaff)
def create_labtest_records(request):
    labstaff = models.LabStaff.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    labtestrecordform = forms.LabTestRecordUserForm()
    if request.method=='POST':
        labtestrecordform = forms.LabTestRecordUserForm(request.POST)
        if labtestrecordform.is_valid():
            labtestrecordform.save()
            return redirect('labstaff-view-patient')
    context = {'labtestrecordform':labtestrecordform,'labstaff':labstaff}
    return render(request, 'hospital/create_labtest_records.html',context=context)


@login_required(login_url='labstafflogin')
@user_passes_test(is_labstaff)
def labstaff_update_delete_lab_records(request):
    labstaff = models.LabStaff.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    labrecords = models.Patient_LabTest_Records.objects.all()
    return render(request, 'hospital/labstaff_update_delete_lab_records.html', {'labrecords': labrecords, 'labstaff': labstaff})


@login_required(login_url='labstafflogin')
@user_passes_test(is_labstaff)
def delete_lab_record_view(request,pk):
    labrecords=models.Patient_LabTest_Records.objects.get(id=pk)
    labrecords.delete()
    return redirect('labstaff-update-delete-lab-records')


@login_required(login_url='labstafflogin')
@user_passes_test(is_labstaff)
def update_lab_record_view(request,pk):
    labstaff = models.LabStaff.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    labrecords = models.Patient_LabTest_Records.objects.get(id=pk)
    labrecordsforms = forms.LabTestRecordUserForm(instance=labrecords)
    if request.method == 'POST':
        labrecordsforms = forms.LabTestRecordUserForm(request.POST, instance=labrecords)
        if labrecordsforms.is_valid():
            labrecordsforms.save()
            return redirect('labstaff-update-delete-lab-records')
    context = {'labrecordsforms': labrecordsforms, 'labstaff': labstaff}
    return render(request, 'hospital/labstaff_update_lab_record.html', context=context)


@login_required(login_url='labstafflogin')
@user_passes_test(is_labstaff)
def create_labtests(request):
    labstaff = models.LabStaff.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    labtestsform = forms.LabTestsUserForm()
    if request.method=='POST':
        labtestsform = forms.LabTestsUserForm(request.POST)
        if labtestsform.is_valid():
            labtestsform.save()
            return redirect('labstaff-create-labtests')
    context = {'labtestsform':labtestsform,'labstaff':labstaff}
    return render(request, 'hospital/create_labtests.html', context=context)


@login_required(login_url='labstafflogin')
@user_passes_test(is_labstaff)
def delete_labtest_view(request,pk):
    labtests=models.LabTests.objects.get(id=pk)
    labtests.delete()
    return redirect('labstaff-update-delete-labtests')


@login_required(login_url='labstafflogin')
@user_passes_test(is_labstaff)
def update_labtest_view(request,pk):
    labstaff = models.LabStaff.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    labtests = models.LabTests.objects.get(id=pk)
    labtestsform = forms.LabTestsUserForm(instance=labtests)
    if request.method == 'POST':
        labtestsform = forms.LabTestsUserForm(request.POST,instance=labtests)
        if labtestsform.is_valid():
            labtestsform.save()
            return redirect('labstaff-update-delete-labtests')
    context = {'labtestsform': labtestsform, 'labstaff': labstaff}
    return render(request, 'hospital/labstaff_update_labtest.html', context=context)


@login_required(login_url='labstafflogin')
@user_passes_test(is_labstaff)
def labstaff_diagnosis_reports_view(request):
    labstaff = models.LabStaff.objects.get(user_id=request.user.id)
    diagnosis_reports = models.Patient_LabTest_Records.objects.all()
    context = {'labstaff':labstaff,'diagnosis_reports':diagnosis_reports}
    return render(request, 'hospital/labstaff_view_diagnosis_report.html', context=context)

@login_required(login_url='labstafflogin')
@user_passes_test(is_labstaff)
def labstaff_lab_test_requests_view(request):
    labstaff = models.LabStaff.objects.get(user_id=request.user.id)
    test_requests = models.Patient_LabTest_Records.objects.all()
    context = {'labstaff':labstaff,'test_requests':test_requests}
    return render(request, 'hospital/labstaff_approve_patient_lab_tests.html', context=context)


@login_required(login_url='labstafflogin')
@user_passes_test(is_labstaff)
def approve_lab_test_view(request,pk):
    report=models.Patient_LabTest_Records.objects.get(id=pk)
    report.status=True
    report.save()
    return redirect(reverse('labstaff-lab-test-requests'))


@login_required(login_url='labstafflogin')
@user_passes_test(is_labstaff)
def reject_lab_test_view(request,pk):
    report=models.Patient_LabTest_Records.objects.get(id=pk)
    user=models.User.objects.get(id=report.user_id)
    user.delete()
    report.delete()
    return redirect('labstaff-lab-test-requests')


#--------------------- FOR CREATING PATIENT LAB REPORTS BY LABSTAFF START-------------------------
@login_required(login_url='labstafflogin')
@user_passes_test(is_labstaff)
def labstaff_create_patient_lab_reports_view(request, pk):
    labstaff = models.LabStaff.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    records=models.Patient_LabTest_Records.objects.get(id=pk)
    context = {'records':records,

               'labstaff':labstaff,
               'patient_name':records.patient.get_name,
                'test_name':records.labtest.testname,
               'date':records.date_created}
    if request.method=='POST':
        feeDict = {
            'roomCharge': int(request.POST['roomCharge']),
            'doctorFee': request.POST['doctorFee'],
            'medicineCost': request.POST['medicineCost'],
            'OtherCharge': request.POST['OtherCharge'],
            'total': (int(request.POST['roomCharge'])) + int(request.POST['doctorFee']) + int(
                request.POST['medicineCost']) + int(request.POST['OtherCharge'])
        }
        context.update(feeDict)
        lab_report = models.Patient_Lab_Reports()
        lab_report.patient_name = records.patient.get_name
        lab_report.test_name = records.labtest.testname
        lab_report.date_created = records.date_created

        lab_report.medicineCost = int(request.POST['medicineCost'])
        lab_report.roomCharge = int(request.POST['roomCharge'])
        lab_report.doctorFee = int(request.POST['doctorFee'])
        lab_report.OtherCharge = int(request.POST['OtherCharge'])
        lab_report.total = (int(request.POST['roomCharge'])+ int(request.POST['doctorFee']) + int(request.POST['medicineCost']) + int(request.POST['OtherCharge']))
        lab_report.save()
        return render(request, 'hospital/labstaff_final_patient_lab_reports.html',context=context)
    return render(request,'hospital/labstaff_create_patient_lab_reports.html', context=context)


@login_required(login_url='labstafflogin')
@user_passes_test(is_labstaff)
def labstaff_update_patient_lab_reports(request, pk):
    labstaff = models.LabStaff.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    records=models.Patient_LabTest_Records.objects.get(id=pk)
    context = {'records':records,
               'labstaff':labstaff,
               'patient_name':records.patient.get_name,
                'test_name':records.labtest.testname,
               'date':records.date_created}

    if request.method=='POST':
        feeDict = {
            'roomCharge': int(request.POST['roomCharge']),
            'doctorFee': request.POST['doctorFee'],
            'medicineCost': request.POST['medicineCost'],
            'OtherCharge': request.POST['OtherCharge'],
            'total': (int(request.POST['roomCharge'])) + int(request.POST['doctorFee']) + int(
                request.POST['medicineCost']) + int(request.POST['OtherCharge'])
        }
        context.update(feeDict)
        lab_report = models.Patient_Lab_Reports()
        lab_report.patient_name = records.patient.get_name
        lab_report.test_name = records.labtest.testname
        lab_report.date_created = records.date_created

        lab_report.medicineCost = int(request.POST['medicineCost'])
        lab_report.roomCharge = int(request.POST['roomCharge'])
        lab_report.doctorFee = int(request.POST['doctorFee'])
        lab_report.OtherCharge = int(request.POST['OtherCharge'])
        lab_report.total = (int(request.POST['roomCharge'])+ int(request.POST['doctorFee']) + int(request.POST['medicineCost']) + int(request.POST['OtherCharge']))
        lab_report.save()
        return render(request,'hospital/labstaff_final_patient_lab_reports.html', context=context)
    return render(request,'hospital/labstaff_update_delete_patient_lab_reports.html', context=context)


#--------------for discharge patient bill (pdf) download and printing



def lab_report_download_pdf_view(request,pk):
    # lab_reports=models.Patient_Lab_Reports.objects.all().filter(recordId=pk).order_by('-id')[:1]
    labstaff = models.LabStaff.objects.get(user_id=request.user.id)
    lab_reports = models.Patient_Lab_Reports.objects.get(id=pk)
    dict={
        'patientName':lab_reports.patient_name,
        'date':lab_reports.date_created,
        'test_name':lab_reports.test_name,
        'medicineCost':lab_reports.medicineCost,
        'roomCharge':lab_reports.roomCharge,
        'doctorFee':lab_reports.doctorFee,
        'OtherCharge':lab_reports.OtherCharge,
        'total':lab_reports.total,
        'labstaff':labstaff
    }
    return render_to_pdf('hospital/download_lab_report.html', dict)
#---------------------------------------------------------------------------------
#------------------------ LABSTAFF RELATED VIEWS END ------------------------------
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_create_diagnosis_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    diagnosis=models.Diagnosis.objects
    days=date.today()
    assignedDoctor=models.User.objects.all().filter(id=patient.assignedDoctorId)
    patientDict={
        'patientId':pk,
        'name':patient.get_name,
        'mobile':patient.mobile,
        'address':patient.address,
        'symptoms':patient.symptoms,
        'todayDate':date.today(),
        'assignedDoctorName':assignedDoctor[0].first_name,
        # 'labtests': diagnosis.labtests,
        # 'lab_work_required' : diagnosis.lab_work_required,

    }
    if request.method == 'POST':

        #for updating to database patientDischargeDetails (pDD)
        pDR=models.Diagnosis()
        pDR.patientId=pk
        pDR.patientName=patient.get_name
        pDR.assignedDoctorName=assignedDoctor[0].first_name
        pDR.address=patient.address
        pDR.mobile=patient.mobile
        pDR.symptoms=patient.symptoms
        # pDR.labtests = diagnosis.labtests
        pDR.lab_work_required = diagnosis.lab_work_required
        pDR.save()

        return render(request,'hospital/doctor_create_diagnosis.html',context=patientDict)

    return render(request,'hospital/doctor_create_diagnosis.html',context=patientDict)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_create_prescription_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    diagnosis=models.Diagnosis.objects
    prescription=models.Prescription.objects
    days=date.today()
    assignedDoctor=models.User.objects.all().filter(id=patient.assignedDoctorId)
    patientDict={
        'patientId':pk,
        'name':patient.get_name,
        'mobile':patient.mobile,
        'address':patient.address,
        'symptoms':patient.symptoms,
        'todayDate':date.today(),
        'assignedDoctorName':assignedDoctor[0].first_name,
        'medicineName':  prescription.medicineName,
        'description': prescription.description,
        # 'lab_work_required' : diagnosis.lab_work_required,

    }
    if request.method == 'POST':

        #for updating to database patientPrescriptionDetails (pPD)
        pPD=models.Diagnosis()
        pPD.patientId=pk
        pPD.patientName=patient.get_name
        pPD.assignedDoctorName=assignedDoctor[0].first_name
        pPD.address=patient.address
        pPD.mobile=patient.mobile
        pPD.symptoms=patient.symptoms
        # pDR.labtests = diagnosis.labtests
        pPD.lab_work_required = diagnosis.lab_work_required
        pPD.medicineName = prescription.medicineName
        pPD.description = prescription.description
        pPD.save()

        return render(request,'hospital/doctor_create_prescription.html',context=patientDict)

    return render(request,'hospital/doctor_create_prescription.html',context=patientDict)


def download_diagnosis_pdf_view(request,pk):
    diagnosisDetails=models.Diagnosis.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dischargeDetails = models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict={
        'patientName':dischargeDetails[0].patientName,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'symptoms':dischargeDetails[0].symptoms,
        'lab_work_required': diagnosisDetails[0].lab_work_required,
    }
    return render_to_pdf('hospital/download_bill.html',dict)
#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#------------------------ PATIENT RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id)
    doctor=models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict={
    'patient':patient,
    'doctorName':doctor.get_name,
    'patientMobile':patient.mobile,
    'patientAddress':patient.address,
    'symptoms':patient.symptoms,
    'doctorDepartment':doctor.department,
    'admitDate':patient.admitDate,
    'InsuranceProvider':patient.patientInsuranceProvider,
    'PolicyNumber':patient.patientPolicyNumber,
    'patientId':patient.id
    }
    return render(request,'hospital/patient_dashboard.html',context=mydict)



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'hospital/patient_appointment.html',{'patient':patient})

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm=forms.PatientAppointmentForm()
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    message=None
    mydict={'appointmentForm':appointmentForm,'patient':patient,'message':message}
    if request.method=='POST':
        appointmentForm=forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('doctorId'))
            desc=request.POST.get('description')

            doctor=models.Doctor.objects.get(user_id=request.POST.get('doctorId'))
            
            if doctor.department == 'Cardiologist':
                if 'heart' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            if doctor.department == 'Dermatologists':
                if 'skin' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            if doctor.department == 'Emergency Medicine Specialists':
                if 'fever' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            if doctor.department == 'Allergists/Immunologists':
                if 'allergy' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            if doctor.department == 'Anesthesiologists':
                if 'surgery' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            if doctor.department == 'Colon and Rectal Surgeons':
                if 'cancer' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.user.id #----user can choose any patient but only their info will be stored
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=request.user.first_name #----user can choose any patient but only their info will be stored
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('patient-view-appointment')
    return render(request,'hospital/patient_book_appointment.html',context=mydict)

def patient_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'hospital/patient_view_doctor.html',{'patient':patient,'doctors':doctors})

def search_doctor_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    # whatever user write in search box we get in query
    query = request.GET['query']
    doctors=models.Doctor.objects.all().filter(status=True).filter(Q(department__icontains=query)| Q(user__first_name__icontains=query))
    return render(request,'hospital/patient_view_doctor.html',{'patient':patient,'doctors':doctors})

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request,'hospital/patient_view_appointment.html',{'appointments':appointments,'patient':patient})

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'hospital/patient_discharge.html',context=patientDict)


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_insurance(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request,'hospital/patient_insurance.html',{'appointments':appointments,'patient':patient})

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def update_patient_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)

    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('patient-dashboard')
    return render(request,'hospital/admin_update_patient.html',context=mydict)

#------------------------ PATIENT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
#------------------------ INSURANCE RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='insurancelogin')
@user_passes_test(is_insurance)
def insurance_dashboard_view(request):
    # for three cards
    # patientcount=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    # appointmentcount=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
    # patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    #for  table in doctor dashboard
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    appointments=zip(appointments,patients)
    mydict={
    # 'patientcount':patientcount,
    # 'appointmentcount':appointmentcount,
    # 'patientdischarged':patientdischarged,
    # 'appointments':appointments,
    # 'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    'insurance':models.Insurance.objects.get(user_id=request.user.id),
    } 
    return render(request,'hospital/insurance_dashboard.html',context=mydict)

# didnt change ends
@login_required(login_url='insurancelogin')
@user_passes_test(is_insurance)
def insurance_patient_view(request):
    mydict={
    'insurance':models.Insurance.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/insurance_patient.html',context=mydict)

#this view is used for creating for opening requests
@login_required(login_url='insurancelogin')
@user_passes_test(is_insurance)
def insurance_requests_view(request):
    mydict={
    'insurance':models.Insurance.objects.get(user_id=request.user.id), #for profile picture of insurance agent in sidebar
    }
    return render(request,'hospital/insurance_requests.html',context=mydict)

#this view is used for creating new records
@login_required(login_url='insurancelogin')
@user_passes_test(is_insurance)
def insurance_new_view(request):
    mydict={
    'insurance':models.Insurance.objects.get(user_id=request.user.id), #for profile picture of insurance agent in sidebar
    }
    return render(request,'hospital/insurance_new.html',context=mydict)

#this view is used for creating new records
@login_required(login_url='insurancelogin')
@user_passes_test(is_insurance)
def insurance_fund_dispersal_view(request):
    mydict={
    'insurance':models.Insurance.objects.get(user_id=request.user.id), #for profile picture of insurance agent in sidebar
    }
    return render(request,'hospital/insurance_fund_dispersal.html',context=mydict)

#this view is used for new requests
@login_required(login_url='insurancelogin')
@user_passes_test(is_insurance)
def insurance_new_requests_view(request):
    mydict={
    'insurance':models.Insurance.objects.get(user_id=request.user.id),
    # 'patients':models.Insurance.objects.filter(status='new-requests'),
     #for profile picture of insurance agent in sidebar
    }
    return render(request,'hospital/insurance_new_requests.html',context=mydict)

#this view is used for under review
@login_required(login_url='insurancelogin')
@user_passes_test(is_insurance)
def insurance_under_review_view(request):
    mydict={
    'insurance':models.Insurance.objects.get(user_id=request.user.id), #for profile picture of insurance agent in sidebar
    }
    return render(request,'hospital/insurance_under_review.html',context=mydict)

#this view is used for validate requests
@login_required(login_url='insurancelogin')
@user_passes_test(is_insurance)
def insurance_validate_requests_view(request):
    mydict={
    'insurance':models.Insurance.objects.get(user_id=request.user.id), #for profile picture of insurance agent in sidebar
    }
    return render(request,'hospital/insurance_validate_requests.html',context=mydict)

@login_required(login_url='insurancelogin')
@user_passes_test(is_insurance)
def insurance_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True,assignedInsuranceId=request.user.id)
    insurance=models.Insurance.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/insurance_view_patient.html',{'patients':patients,'insurance':insurance})

@login_required(login_url='insurancelogin')
@user_passes_test(is_insurance)
def insurance_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedInsuranceName=request.user.first_name)
    insurance=models.Insurance.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/insurance_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'insurance':insurance})

@login_required(login_url='insurancelogin')
@user_passes_test(is_insurance)
def insurance_appointment_view(request):
    insurance=models.Insurance.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/insurance_appointment.html',{'insurance':insurance})

@login_required(login_url='insurancelogin')
@user_passes_test(is_insurance)
def insurance_view_appointment_view(request):
    insurance=models.Insurance.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,docterId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/insurance_view_appointment.html',{'appointments':appointments,'insurance':insurance})

@login_required(login_url='insurancelogin')
@user_passes_test(is_insurance)
def insurance_delete_appointment_view(request):
    insurance=models.Insurance.objects.get(user_id=request.user.id) #for profile picture of insurance in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,insuranceId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/insurance_delete_appointment.html',{'appointments':appointments,'insurance':insurance})

@login_required(login_url='insurancelogin')
@user_passes_test(is_insurance)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    insurance=models.Insurance.objects.get(user_id=request.user.id) #for profile picture of insurance agent in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,insuranceId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/insurance_delete_appointment.html',{'appointments':appointments,'insurance':insurance})

#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'hospital/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'hospital/contactussuccess.html')
    return render(request, 'hospital/contactus.html', {'form':sub})
