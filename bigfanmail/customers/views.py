import stripe
import decimal
import payments
from bigfanmail import settings
from bigfanmail.customers.models import BFCustomer
from bigfanmail.domains.models import Account
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist 
from django.core.mail import EmailMessage 
from payments.models import (
    Customer,
    CurrentSubscription,
    Event,
    EventProcessingException
)
import logging

logger = logging.getLogger(__name__)

@require_POST
@login_required
def subscribe(request):
  if 'terms' in request.POST:
            bfcust = request.user 
            BigFanAcct = request.session['BigFanAcct']
            customer = Customer.create(bfcust, charge_immediately=False)
            customer.update_card(request.POST.get("stripeToken"))
            bfcust.add1 = request.POST['address1']
            bfcust.add2 = request.POST['address2']
            bfcust.city = request.POST['city']
            bfcust.state = request.POST['state']
            bfcust.zipcode = request.POST['zipcode']
            try:
               coupon = request.POST['coupon'].lower()
               stripe.Coupon.retrieve(coupon)
            except stripe.StripeError as e:
               coupon=None
            bfcust.save()
            try:
              if 'autorenew' in request.POST:
                if coupon:
                  customer.subscribe(BigFanAcct.bfname.product.product_name, coupon=coupon)
                else:
                  customer.subscribe(BigFanAcct.bfname.product.product_name)
                bfemail = BigFanAcct.bfname.bfname + "@" + BigFanAcct.bfname.domain.domain_name
                message = "Congratulations, you have successfully registered email address, " + bfemail + "." +  "\nYou will soon receive verfication that your BigFanMail email address is ready to use.\nIf you have any questions, please email us at support@BigFanMail.com .\n\nBigFanMail Support"
                acctemail = EmailMessage('New Account', message, 'support@bigfanmail.com', [BigFanAcct.customer.email_address], settings.ADMINS, headers = {})
                acctemail.send()
                BigFanName = request.session['BigFanObj']
                BigFanName.save()
                #BigFanAnswer = request.session['BigFanAnswer']
                #BigFanAnswer.save()
                BigFanAcct.bfname = BigFanName 
                BigFanAcct.offer_code = request.POST['coupon']
                BigFanAcct.auto_renew = True
                BigFanAcct.save()
                request.session['BigFanAcct'] = BigFanAcct
              else:
                customer.charge(decimal.Decimal(BigFanAcct.bfname.product.price), description="BigFanAcct.bfname.product.description")
            except stripe.StripeError as e:
              try:
                data = {}
                data["error"] = e.args[0]
              except IndexError:
                data["error"] = "Unknown error"
              return render(request, 'registration/creditcard.html', {})
#    return _ajax_response(request, "payments/_subscribe_form.html", **data)
#    return render(request, 'registration/registration_complete.html', {})
            return redirect('/register/get_host_password/', permanent=True)
  else:
            return render(request, 'registration/creditcard.html', {})

def get_host_password(request):
    return render(request, 'registration/host_password.html', {})

def registration_complete(request, bfemail=''):
    return render(request, 'registration/registration_complete.html', {'bfemail':bfemail})

@login_required
def editusers(request):
    bfacct = Account.objects.filter(customer=request.user)
    return render(request, 'user_edit.html',{'bfacct': bfacct})

@login_required
def editacct(request, idno):
    logger.debug('idno: ' + idno)
    request.session['idno'] = idno
    thisacct = request.session['bfacct']
    return render(request, 'acct_edit.html',{'thisacct': thisacct[int(idno)],})

@login_required
def saveusers(request):
    bfcust = request.user
    bfcust.first_name = request.POST['first_name']
    bfcust.last_name = request.POST['last_name']
    bfcust.add1 = request.POST['address1']
    bfcust.add2 = request.POST['address2']
    bfcust.city = request.POST['city']
    bfcust.state = request.POST['state']
    bfcust.zipcode = request.POST['zipcode']
    bfcust.save()
    return redirect('/profile')

@require_POST
@login_required
def save_emailpassword(request):
   if len(request.POST['hostpass1']) > 5:
      if request.POST['hostpass1'] == request.POST['hostpass2']:
         bfacct = Account.objects.get(customer=request.user, bfname=request.session['BigFanObj'])
         try:
            bfacct.save_password(request.POST['hostpass1'])
         except:
            return render(request, 'registration/host_password.html',{}) 
         return redirect('/register/registration_complete', permanent=True)
      else:
         error="Passwords don't match."
   else:
      error = "Password must be 6 characters long."
      
   return render(request, 'registration/host_password.html', {'error': error}) 

@require_POST
@login_required
def save_account(request):
   bfacct = request.session['bfacct'][int(request.session['idno'])] 
   if 'autorenew' in request.POST:
      bfacct.auto_renew = True
   else:
      bfacct.auto_renew = False
   bfacct.save()
   return redirect('/profile', permanent=True)

def retrieve_password(request):
   return password
