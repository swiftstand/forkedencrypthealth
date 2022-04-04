from django.contrib import admin
from django.urls import path
from hospital import views
from django.contrib.auth.views import LoginView,LogoutView


#-------------FOR ADMIN RELATED URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),


    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),


    path('adminclick', views.adminclick_view),
    path('doctorclick', views.doctorclick_view),
    path('hospitalstaffclick', views.hospitalstaffclick_view),
    path('patientclick', views.patientclick_view),
    path('insuranceclick', views.insuranceclick_view),

    path('adminsignup', views.admin_signup_view),
    path('doctorsignup', views.doctor_signup_view,name='doctorsignup'),
    path('hospitalstaffsignup', views.hospitalstaff_signup_view,name='hospitalstaffsignup'),
    path('patientsignup', views.patient_signup_view),

    path('adminlogin', LoginView.as_view(template_name='hospital/adminlogin.html')),
    path('doctorlogin', LoginView.as_view(template_name='hospital/doctorlogin.html')),
    path('hospitalstafflogin', LoginView.as_view(template_name='hospital/hospitalstafflogin.html')),
    path('patientlogin', LoginView.as_view(template_name='hospital/patientlogin.html')),


    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='hospital/index.html'),name='logout'),


    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-doctor', views.admin_doctor_view,name='admin-doctor'),
    path('admin-view-doctor', views.admin_view_doctor_view,name='admin-view-doctor'),
    path('delete-doctor-from-hospital/<int:pk>', views.delete_doctor_from_hospital_view,name='delete-doctor-from-hospital'),
    path('update-doctor/<int:pk>', views.update_doctor_view,name='update-doctor'),
    path('admin-add-doctor', views.admin_add_doctor_view,name='admin-add-doctor'),
    path('admin-approve-doctor', views.admin_approve_doctor_view,name='admin-approve-doctor'),
    path('approve-doctor/<int:pk>', views.approve_doctor_view,name='approve-doctor'),
    path('reject-doctor/<int:pk>', views.reject_doctor_view,name='reject-doctor'),
    path('admin-view-doctor-specialisation',views.admin_view_doctor_specialisation_view,name='admin-view-doctor-specialisation'),


    path('admin-patient', views.admin_patient_view,name='admin-patient'),
    path('admin-view-patient', views.admin_view_patient_view,name='admin-view-patient'),
    path('delete-patient-from-hospital/<int:pk>', views.delete_patient_from_hospital_view,name='delete-patient-from-hospital'),
    path('update-patient/<int:pk>', views.update_patient_view,name='update-patient'),
    path('update-patient-patient/<int:pk>', views.update_patient_patient_view,name='update-patient-patient'),
    path('admin-add-patient', views.admin_add_patient_view,name='admin-add-patient'),
    path('admin-approve-patient', views.admin_approve_patient_view,name='admin-approve-patient'),
    path('approve-patient/<int:pk>', views.approve_patient_view,name='approve-patient'),
    path('reject-patient/<int:pk>', views.reject_patient_view,name='reject-patient'),
    path('admin-discharge-patient', views.admin_discharge_patient_view,name='admin-discharge-patient'),
    path('discharge-patient/<int:pk>', views.discharge_patient_view,name='discharge-patient'),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),


    path('admin-appointment', views.admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),

    path('admin-hospitalstaff', views.admin_hospitalstaff_view,name='admin-hospitalstaff'),
    path('admin-view-hospitalstaff', views.admin_view_hospitalstaff_view,name='admin-view-hospitalstaff'),
    path('delete-hospitalstaff-from-hospital/<int:pk>', views.delete_hospitalstaff_from_hospital_view,name='delete-hospitalstaff-from-hospital'),
    path('update-hospitalstaff/<int:pk>', views.update_hospitalstaff_view,name='update-hospitalstaff'),
    path('admin-add-hospitalstaff', views.admin_add_hospitalstaff_view,name='admin-add-hospitalstaff'),
    path('admin-approve-hospitalstaff', views.admin_approve_hospitalstaff_view,name='admin-approve-hospitalstaff'),
    path('approve-hospitalstaff/<int:pk>', views.approve_hospitalstaff_view,name='approve-hospitalstaff'),
    path('reject-hospitalstaff/<int:pk>', views.reject_hospitalstaff_view,name='reject-hospitalstaff')
]


#---------FOR DOCTOR RELATED URLS-------------------------------------
urlpatterns +=[
    path('doctor-dashboard', views.doctor_dashboard_view,name='doctor-dashboard'),

    path('doctor-patient', views.doctor_patient_view,name='doctor-patient'),
    path('doctor-view-patient', views.doctor_view_patient_view,name='doctor-view-patient'),
    path('doctor-view-discharge-patient',views.doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),

    path('doctor-appointment', views.doctor_appointment_view,name='doctor-appointment'),
    path('doctor-view-appointment', views.doctor_view_appointment_view,name='doctor-view-appointment'),
    path('doctor-delete-appointment',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
]


#----------FOR HOSPITAL STAFF RELATED URLS---------------------------------
urlpatterns +=[
    path('hospitalstaff-dashboard', views.hospitalstaff_dashboard_view,name='hospitalstaff-dashboard'),

    path('hospitalstaff-doctor', views.hospitalstaff_doctor_view,name='hospitalstaff-doctor'),
    path('hospitalstaff-view-doctor', views.hospitalstaff_view_doctor_view,name='hospitalstaff-view-doctor'),
    path('hospitalstaff-view-doctor-specialisation',views.hospitalstaff_view_doctor_specialisation_view,name='hospitalstaff-view-doctor-specialisation'),
    path('hospitalstaff-patient', views.hospitalstaff_patient_view,name='hospitalstaff-patient'),
    path('hospitalstaff-view-patient', views.hospitalstaff_view_patient_view,name='hospitalstaff-view-patient'),
    path('update-patient/<int:pk>', views.update_patient_view,name='update-patient'),
    path('update-patient-patient/<int:pk>', views.update_patient_patient_view,name='update-patient-patient'),
    path('hospitalstaff-add-patient', views.hospitalstaff_add_patient_view,name='hospitalstaff-add-patient'),
    path('hospitalstaff-approve-patient', views.hospitalstaff_approve_patient_view,name='hospitalstaff-approve-patient'),
    path('approve-patient/<int:pk>', views.approve_patient_view,name='approve-patient'),
    path('reject-patient/<int:pk>', views.reject_patient_view,name='reject-patient'),
    path('hospitalstaff-discharge-patient', views.hospitalstaff_discharge_patient_view,name='hospitalstaff-discharge-patient'),
    path('discharge-patient/<int:pk>', views.discharge_patient_view,name='discharge-patient'),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),
    path('hospitalstaff-appointment', views.hospitalstaff_appointment_view,name='hospitalstaff-appointment'),
    path('hospitalstaff-view-appointment', views.hospitalstaff_view_appointment_view,name='hospitalstaff-view-appointment'),
    path('hospitalstaff-add-appointment', views.hospitalstaff_add_appointment_view,name='hospitalstaff-add-appointment'),
    path('hospitalstaff-approve-appointment', views.hospitalstaff_approve_appointment_view,name='hospitalstaff-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),
]




#---------FOR PATIENT RELATED URLS-------------------------------------
urlpatterns +=[

    path('patient-dashboard', views.patient_dashboard_view,name='patient-dashboard'),
    path('patient-appointment', views.patient_appointment_view,name='patient-appointment'),
    path('patient-book-appointment', views.patient_book_appointment_view,name='patient-book-appointment'),
    path('patient-view-appointment', views.patient_view_appointment_view,name='patient-view-appointment'),
    path('patient-discharge', views.patient_discharge_view,name='patient-discharge'),
    path('patient-insurance', views.patient_insurance,name='patient-insurance'),
]
