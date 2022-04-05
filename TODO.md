# Admin update patient doesn't work
1. Did not actually update the patient.

## Doctor create diagnosis view
1. The profile pic is not correctly displayed.
2. The create diagnosis button does not properly work.
3. The lab tests required is not being passed properly. 

## Doctor create prescription view
1. This is not properly working
    a. Manager object has no attribute name medicineName
2. The perscriptions are not being passed properly. 
    a. Most likely because a form in Django wasn't created

## Doctor update patient
1. This is not working.
2. The patient isn't updated.

## Lab Staff
1. Lab reports do not seem to be saving
    a. This may be ok as long as the apparance of creation happens
2. Lab Tests Requests tab doesn't work
    a. This just takes us back to the lab staff dashboard

## Patient
1. Needs to be able to create an insurance claim.
2. Patient needs to be able to update his own record.

## Transaction
1. After a patient submits a transaction an admin or hospital staff will have to approve it.

## OTP
1. OTP will need to be implemented with pyotp

## SSL certificates
1. We need to generate SSL certificates to sign our connection
    a. This is a requirement to get an https:// address

## Hospital Staff Discharge
1. Make sure to update the PDD for when a hospital staff dicharges a patient.
