from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from bigfanmail.customers.models import BFCustomer
from bigfanmail.domains.models import Domain, BFName, Team, Account
from bigfanmail.products.models import Product, CommonName, Occupation
from random import randint
from bigfanmail.search import EAddress
from bigfanmail.domains.models import UserRegistrationForm
from base64 import b64encode, b64decode
from M2Crypto.EVP import Cipher
from django.utils.crypto import get_random_string
import hashlib
from bigfanmail import settings
from bigfanmail.domains.models import Account

from django.http import HttpResponse
import logging
logger = logging.getLogger(__name__)


def regcom(request):
    #request.session['bfacct'] = Account.objects.get(customer=request.user.bfcustomer)
    return render(request, 'registration/host_password.html', {'form': UserRegistrationForm})

def regform(request):
    return HttpResponse(request.POST['plan'])

def testhash(request):
    key=settings.SECRET_KEY
    iv=Account.objects.get(id=1).random_str
    data=b64decode('MTkcUSMxaxZytN4D3B7XEaPy5wNvAe0MHB1xNZeqZKo=')
    cipher=Cipher(alg='aes_256_cbc', key=key, iv=iv, op=0)
    v=cipher.update(data) + cipher.final()
    del cipher
    return HttpResponse(v)
