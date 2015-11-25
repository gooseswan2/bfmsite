from django.db import models
from django import forms
from bigfanmail.products.models import Product
from bigfanmail.customers.models import BFCustomer
from registration.forms import RegistrationForm
from django_localflavor_us.forms import USStateSelect, USZipCodeField
from django.forms.widgets import HiddenInput
from bigfanmail import settings


class UserRegistrationForm(RegistrationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=40)
    add1 = forms.CharField(label='Address1', required=False)
    add2 = forms.CharField(label='Address2', required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(widget=USStateSelect(),required=False)
    zipcode = USZipCodeField(label='Zip code',required=False)
    sec_question1 = forms.ModelChoiceField(label='Security question1',queryset=SecurityQuestion.objects.all())
    sec_answer1 = forms.CharField(label='Security answer1',)

    def clean_email(self):
       data = self.cleaned_data['email']
       if BFCustomer.objects.filter(email_address=data).exists():
           raise forms.ValidationError("This email is already used")
       return data

    def add_fields(self, request, bfname="", domainname=""):
       if request.method == 'GET':
          self.fields['bfname'] = forms.CharField(initial=bfname,widget=HiddenInput)
       else:
          self.fields['bfname'] = forms.CharField(initial=request.POST['bfname'],widget=HiddenInput)

       if request.method == 'GET':
          self.fields['domainname'] = forms.CharField(initial=domainname,widget=HiddenInput)
       else:
          self.fields['domainname'] = forms.CharField(initial=request.POST['domainname'],widget=HiddenInput)

       if request.method == 'GET':
          plan = request.GET['plan']
          self.fields['plan'] = forms.CharField(initial=plan,widget=HiddenInput)
       else:
          self.fields['plan'] = forms.CharField(initial=request.POST['plan'],widget=HiddenInput)

class AccountCreationForm(forms.Form):
    username = forms.CharField(max_length=75)
    email_address = forms.CharField(max_length=75)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=40)
    password1 = forms.CharField(min_length=6, max_length=15)
    password2 = forms.CharField(min_length=6, max_length=15)
    security_answer = forms.CharField(max_length=75)
