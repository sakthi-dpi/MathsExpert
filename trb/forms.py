# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Student, Course

class StudentSignupForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    MEDIUM_CHOICES = (
        ('Tamil', 'Tamil'),
        ('English', 'English'),
        ('Malayalam', 'Malayalam'),
        ('Kannadam', 'Kannadam'),
    )

    BATCH_TYPE_CHOICES = (
        ('Regular', 'Regular batch'),
        ('Weekend', 'Weekend batch'),
        ('Evening', 'Evening batch'),
    )

    CLASS_TYPE_CHOICES = (
        ('Online', 'Online'),
        ('Offline', 'Offline'),
    )

    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    qualification = forms.CharField(max_length=100)
    employment_status = forms.CharField(max_length=100)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    contact_number = forms.CharField(max_length=15)
    email = forms.EmailField()
    guardian_contact_number = forms.CharField(max_length=15)
    contact_address = forms.CharField(widget=forms.Textarea)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_of_joining = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    medium_of_study = forms.ChoiceField(choices=MEDIUM_CHOICES)
    batch_type = forms.ChoiceField(choices=BATCH_TYPE_CHOICES)
    class_type = forms.ChoiceField(choices=CLASS_TYPE_CHOICES)
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    recommended_by = forms.CharField(max_length=100)

    class Meta:
        model = Student
        fields = ['username', 'password', 'password_confirmation', 'firstname', 'lastname', 'qualification', 'employment_status', 'gender', 'contact_number', 'email', 'guardian_contact_number', 'contact_address', 'date_of_birth', 'date_of_joining', 'medium_of_study', 'batch_type', 'class_type', 'course', 'passport_photo', 'recommended_by']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            raise forms.ValidationError("Passwords do not match.")

