from bigfanmail.customers.models import BFCustomer
from bigfanmail.domains.models import Account, CustomerAnswer, SecurityQuestion, Domain, BFName, UserRegistrationForm
from bigfanmail.products.models import Product
from django.http import HttpResponse
import logging
logger = logging.getLogger(__name__)

def user_created(sender, user, request, **kwargs):
   request.session.set_expiry(1800)
   form = UserRegistrationForm(request.POST)
   logger.debug('I am in the backend')
   data2 = BFName()
   data2.domain = Domain.objects.get(team=request.session['bfteam'], domain_name=form.data["domainname"])
   data2.bfname = form.data["bfname"].lower()
   data2.product = Product.objects.get(product_name=form.data["plan"])
   request.session['BigFanObj'] = data2
   
   #data2.save()
   data3 = CustomerAnswer()
   data3.customer = request.user 
   data3.security_question = SecurityQuestion.objects.get(id=form.data["sec_question1"])
   data3.answer = form.data["sec_answer1"]
   data3.save()
#   data4 = CustomerAnswer()
#   data4.customer = request.user 
#   data4.security_question = SecurityQuestion.objects.get(id=form.data["sec_question2"])
#   data4.answer = form.data["sec_answer2"]
#   data4.save()
   bfacct = Account()
   bfacct.customer = request.user 
   bfacct.bfname = data2
   #bfacct.save()
   request.session['BigFanAcct'] = bfacct

from registration.signals import user_registered
user_registered.connect(user_created)
