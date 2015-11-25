import bigfanmail.settings
from django.db import models
from django import forms
from bigfanmail.products.models import Product
from bigfanmail.customers.models import BFCustomer
from registration.forms import RegistrationForm
from django_localflavor_us.forms import USStateSelect, USZipCodeField
from django.forms.widgets import HiddenInput
from django.contrib.auth.hashers import make_password 

from bigfanmail import settings
from base64 import b64encode, b64decode
from M2Crypto.EVP import Cipher
from django.utils.crypto import get_random_string


# Create your models here.
class Team(models.Model):
    team_name       =	models.CharField(max_length=75)
    short_name      =	models.CharField(max_length=4, unique=True)
    sport           =	models.CharField(max_length=40)

    class Meta:
       ordering = ['short_name']

    def __unicode__(self):
       return self.short_name

class Domain(models.Model):
    team =		models.ForeignKey(Team)
    domain_name =	models.CharField(max_length=75)

    class Meta:
       unique_together = ('team', 'domain_name')

    def __unicode__(self):
       return self.domain_name

class BFName(models.Model):
    domain =            models.ForeignKey(Domain)
    product =           models.ForeignKey(Product)
    bfname =            models.CharField(max_length=40)

    class Meta:
       unique_together = ('domain', 'bfname')

    def __unicode__(self):
       return self.bfname + "@" + self.domain.domain_name

class Account(models.Model):
    customer =          models.ForeignKey(settings.AUTH_USER_MODEL)
    bfname =            models.ForeignKey(BFName)
    host_id =           models.CharField(max_length=40)
    host_password =     models.CharField(max_length=128)
    interests =         models.CharField(max_length=16)
    offer_code =        models.CharField(max_length=30)
    auto_renew =        models.BooleanField()

    def __unicode__(self):
        return self.bfname.bfname + '@' + self.bfname.domain.domain_name

    def encrypt_hpwd(self, clearpass):
        key=settings.SECRET_KEY
        iv=get_random_string(16)
        cipher=Cipher(alg='aes_256_cbc', key=key, iv=iv, op=1)
        v=cipher.update(clearpass) + cipher.final()
        del cipher
        return b64encode(v), iv

    def decrypt_hpwd(self, password):
        data=b64decode(password)
        cipher=Cipher(alg='aes_256_cbc', key=settings.SECRET_KEY, iv=self.interests, op=0)
        v=cipher.update(data) + cipher.final()
        del cipher
        return v

    def save_password(self, clearpass):
        (self.host_password, self.interests)=self.encrypt_hpwd(clearpass) 
        self.save(update_fields=['host_password', 'interests'])

class SecurityQuestion(models.Model):
    question =     models.CharField(max_length=150)

    def __unicode__(self):
        return self.question

class CustomerAnswer(models.Model):
    customer =                  models.ForeignKey(settings.AUTH_USER_MODEL)
    security_question =         models.ForeignKey(SecurityQuestion)
    answer =                    models.CharField(max_length=75)

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
    #sec_question2 = forms.ModelChoiceField(label='Security question2',queryset=SecurityQuestion.objects.all())
    #sec_answer2 = forms.CharField(label='Security answer2',)

    def clean_password1(self):
        password = self.cleaned_data['password1']
        if len(password) < 6:
            raise forms.ValidationError('Password has to be at least 6 characters long.')
        return password 

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
