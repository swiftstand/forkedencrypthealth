from django.contrib import admin
from django.urls import path
from hospital import views
from django.contrib.auth.views import LoginView,LogoutView


#-------------FOR ADMIN RELATED URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),

    path('aboutus', views.aboutus_view),

    path('adminclick', views.adminclick_view),
    path('doctorclick', views.doctorclick_view),
    path('patientclick', views.patientclick_view),
    path('insuranceclick', views.insuranceclick_view),

    path('adminsignup', views.admin_signup_view),
    path('doctorsignup', views.doctor_signup_view,name='doctorsignup'),
    path('patientsignup', views.patient_signup_view),
    #insurance (prem)
    path('insurancesignup', views.insurance_signup_view,name='insurancesignup'),

    
    path('adminlogin', LoginView.as_view(template_name='hospital/adminlogin.html')),
    path('doctorlogin', LoginView.as_view(template_name='hospital/doctorlogin.html')),
    path('patientlogin', LoginView.as_view(template_name='hospital/patientlogin.html')),
    #insurance (prem)
    path('insurancelogin', LoginView.as_view(template_name='hospital/insurancelogin.html')),
   


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
    path('admin-add-patient', views.admin_add_patient_view,name='admin-add-patient'),
    path('admin-approve-patient', views.admin_approve_patient_view,name='admin-approve-patient'),
    path('approve-patient/<int:pk>', views.approve_patient_view,name='approve-patient'),
    path('reject-patient/<int:pk>', views.reject_patient_view,name='reject-patient'),
    path('admin-discharge-patient', views.admin_discharge_patient_view,name='admin-discharge-patient'),
    path('discharge-patient/<int:pk>', views.discharge_patient_view,name='discharge-patient'),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),

#similarly creating for insurance
 
    path('admin-insurance', views.admin_insurance_view,name='admin-insurance'),
    path('admin-view-insurance', views.admin_view_insurance_view,name='admin-view-insurance'),
    path('delete-insurance-from-hospital/<int:pk>', views.delete_insurance_from_hospital_view,name='delete-insurance-from-hospital'),
    path('update-insurance/<int:pk>', views.update_insurance_view,name='update-insurance'),
    path('admin-add-insurance', views.admin_add_insurance_view,name='admin-add-insurance'),
    path('admin-approve-insurance', views.admin_approve_insurance_view,name='admin-approve-insurance'),
    path('approve-insurance/<int:pk>', views.approve_insurance_view,name='approve-insurance'),
    path('reject-insurance/<int:pk>', views.reject_insurance_view,name='reject-insurance'),
    path('admin-view-insurance-team',views.admin_view_insurance_team_view,name='admin-view-insurance-team'),


    path('admin-appointment', views.admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),
]


#---------FOR DOCTOR RELATED URLS-------------------------------------
urlpatterns +=[
    path('doctor-dashboard', views.doctor_dashboard_view,name='doctor-dashboard'),
    path('search', views.search_view,name='search'),
    path('doctor-patient', views.doctor_patient_view,name='doctor-patient'),
    path('doctor-view-patient', views.doctor_view_patient_view,name='doctor-view-patient'),
    path('doctor-view-prescription', views.doctor_view_prescription_view, name='doctor-view-prescription'),
    path('doctor-view-discharge-patient',views.doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),
    path('doctor-create-diagnosis/<int:pk>',views.doctor_create_diagnosis_view,name='doctor-create-diagnosis'),
    path('doctor-update-patient/<int:pk>', views.doctor_update_patient_view,name='doctor-update-patient'),
    path('doctor-create-prescription/<int:pk>', views.doctor_create_prescription_view,name='doctor-create-prescription'),
    path('doctor-appointment', views.doctor_appointment_view,name='doctor-appointment'),
    path('doctor-view-appointment', views.doctor_view_appointment_view,name='doctor-view-appointment'),
    path('doctor-delete-appointment',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
    path('download-diagnosis-pdf/<int:pk>', views.download_diagnosis_pdf_view,name='download-diagnosis-pdf'),
]




#---------FOR PATIENT RELATED URLS-------------------------------------
urlpatterns +=[

    path('patient-dashboard', views.patient_dashboard_view,name='patient-dashboard'),
    path('patient-appointment', views.patient_appointment_view,name='patient-appointment'),
    path('patient-book-appointment', views.patient_book_appointment_view,name='patient-book-appointment'),
    path('patient-view-appointment', views.patient_view_appointment_view,name='patient-view-appointment'),
    path('patient-view-doctor', views.patient_view_doctor_view,name='patient-view-doctor'),
    path('searchdoctor', views.search_doctor_view,name='searchdoctor'),
    path('patient-discharge', views.patient_discharge_view,name='patient-discharge'),

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


#---------FOR INSURANCE RELATED URLS-------------------------------------
urlpatterns +=[
    path('insurance-dashboard', views.insurance_dashboard_view,name='insurance-dashboard'),

    #created for new,requests, and fund dispersal in insurance base section(prem)
    path('insurance-requests', views.insurance_requests_view,name='insurance-requests'),
    path('insurance-new', views.insurance_new_view,name='insurance-new'),
    path('insurance-fund-dispersal', views.insurance_fund_dispersal_view,name='insurance-fund-dispersal'),
    path('insurance-new-requests', views.insurance_new_requests_view,name='insurance-new-requests'),
    path('insurance-under-review', views.insurance_under_review_view,name='insurance-under-review'),
    path('insurance-validate-requests', views.insurance_validate_requests_view,name='insurance-validate-requests'),


    path('insurance-patient', views.doctor_patient_view,name='insurance-patient'),
    path('insurance-view-patient', views.insurance_view_patient_view,name='insurance-view-patient'),
    path('insurance-view-discharge-patient',views.insurance_view_discharge_patient_view,name='insurance-view-discharge-patient'),

    path('insurance-appointment', views.doctor_appointment_view,name='insurance-appointment'),
    path('insurance-view-appointment', views.insurance_view_appointment_view,name='insurance-view-appointment'),
    path('insurance-delete-appointment',views.insurance_delete_appointment_view,name='insurance-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
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

