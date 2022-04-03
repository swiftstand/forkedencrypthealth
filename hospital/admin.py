from django.contrib import admin
from .models import (Doctor, Patient, Appointment, PatientDischargeDetails,
        Patient_LabTest_Records, LabTests, LabStaff, Diagnosis, Prescription, Insurance)
# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Doctor, DoctorAdmin)

#insurance created by prem
class InsuranceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Insurance, InsuranceAdmin)

class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)

class Patient_LabTest_RecordsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient_LabTest_Records,Patient_LabTest_RecordsAdmin)

class LabTestsAdmin(admin.ModelAdmin):
    pass
admin.site.register(LabTests,LabTestsAdmin)

class LabStaffAdmin(admin.ModelAdmin):
    pass
admin.site.register(LabStaff,LabStaffAdmin)
class DiagnosisAdmin(admin.ModelAdmin):
    pass
admin.site.register(Diagnosis, DiagnosisAdmin)

class PrescriptionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Prescription, PrescriptionAdmin)
