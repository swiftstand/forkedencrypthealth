from django.contrib import admin
from .models import Doctor,Patient,Appointment,PatientDischargeDetails,Patient_LabTest_Records,LabTests,LabStaff
# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Doctor, DoctorAdmin)

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