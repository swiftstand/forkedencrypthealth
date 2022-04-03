from hashlib import new
from django.db import models
from django.contrib.auth.models import User

departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
]

lab_work_required=[('Complete Blood Count', 'Complete Blood Count'),
          ('Basic Metabolic Panel', 'Basic Metabolic Panel'),
          ('Comprehensive Metabolic Panel','Comprehensive Metabolic Panel'),
          ('Lipid Panel', 'Lipid Panel'),
          ('Thyroid Stimulating Hormone', 'Thyroid Stimulating Hormone'),
          ('Hemoglobin', 'Hemoglobin'),
          ('Urinalysis', 'Urinalysis'),
          ('Cultures', 'Cultures')]

company=[('Aetna','Aetna'),
('Cigna','Cigna'),
('Anthem','Anthem'),
('UHG','UHG'),
('Humana','Humana')
]

class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)


class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    symptoms = models.CharField(max_length=100,null=False)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    patientInsuranceProvider = models.CharField(max_length=100,null=True)
    patientPolicyNumber=models.PositiveIntegerField(null=True)
    medicalHistory = models.CharField(max_length=500, null=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.symptoms+")"


class Appointment(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    doctorId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40,null=True)
    doctorName=models.CharField(max_length=40,null=True)
    appointmentDate=models.DateField(auto_now=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)


class PatientDischargeDetails(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40)
    assignedDoctorName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    patientInsuranceProvider = models.CharField(max_length=100, null=True)
    patientPolicyNumber = models.PositiveIntegerField(null=True)
    symptoms = models.CharField(max_length=100,null=True)

    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)

    roomCharge=models.PositiveIntegerField(null=False)
    medicineCost=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)
    OtherCharge=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)


class LabStaff(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/LabStaffProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    department= models.CharField(max_length=50,choices=departments,default='xxx')
    status=models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{}".format(self.user.first_name)

class LabTests(models.Model):
    testname = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.testname

class Patient_Lab_Reports(models.Model):
    patient_name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=200, null=True)
    test_name = models.CharField(max_length=200)

    roomCharge = models.PositiveIntegerField(null=False)
    medicineCost = models.PositiveIntegerField(null=False)
    doctorFee = models.PositiveIntegerField(null=False)
    OtherCharge = models.PositiveIntegerField(null=False)
    total = models.PositiveIntegerField(null=False)

class Patient_LabTest_Records(models.Model):
    patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=1, null=True)
    labtest = models.ForeignKey(LabTests, null=True, on_delete=models.CASCADE)
    STATUS = (
        ('Done', 'Done'),
        ('InProgress', 'InProgress'),
        ('Incomplete', 'Incomplete')
    )
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    results = models.CharField(max_length=200, null=True)
    reports = models.ForeignKey(Patient_Lab_Reports, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.patient.name

class Appointment(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    doctorId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40,null=True)
    doctorName=models.CharField(max_length=40,null=True)
    appointmentDate=models.DateField(auto_now=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)

class Prescription(models.Model):
    patientId = models.PositiveIntegerField(null=True)
    patientName = models.CharField(max_length=40, null=True)
    medicineName = models.CharField(max_length=500,null=True)
    description = models.CharField(max_length=500,null=True)

class Diagnosis(models.Model):
    assignedDoctorId = models.PositiveIntegerField(null=True)
    # id=models.PositiveIntegerField(null=True)
    first_name=models.CharField(max_length=40,null=True)
    last_name=models.CharField(max_length=40,null=True)
    address = models.CharField(max_length=40)
    feedback = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    symptoms = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=40)
    # # labtests = models.CharField(max_length=50,choices=departments,default='Complete Blood Count')
    # labtests = models.CharField(max_length=50)
    lab_work_required = models.CharField(max_length=100)

#insurance agent
class Insurance(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/InsuranceProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    company= models.CharField(max_length=50,choices=company,default='Aetna')
    #change
    #status=models.CharField(default='new_requests',max_length=100)
    status=models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.company)

class PatientDischargeDetails(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40)
    assignedDoctorName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    symptoms = models.CharField(max_length=100,null=True)

    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)

    roomCharge=models.PositiveIntegerField(null=False)
    medicineCost=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)
    OtherCharge=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)
