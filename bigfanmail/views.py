from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.template import RequestContext
from bigfanmail.customers.models import BFCustomer
from bigfanmail.domains.models import Domain, BFName, Team, Account, CustomerAnswer, SecurityQuestion
from bigfanmail.products.models import Product, CommonName, Occupation
from random import randint
from bigfanmail.search import EAddress

from django.http import HttpResponse
import logging
logger = logging.getLogger(__name__)


def homepage(request):
    return render(request, 'base_generic.html', {'':''})

def mysession(request):
    return render(request, 'mysession.html', {'':''})

def findyourteam(request):
    return render(request, 'findyourteam.html', {'bfteams':''})

def college(request, group):
    bfteams = Team.objects.only('short_name').filter(sport='ncaa').order_by('short_name')
    return render(request, 'findyourteam.html', {'bfteams':bfteams, 'group': group})

def nfl(request):
    bfteams = Team.objects.only('short_name').filter(sport='nfl').order_by('short_name')
    return render(request, 'findyourteam.html', {'bfteams':bfteams})

def sports(request, group):
    bfteams = Team.objects.only('short_name').filter(sport=group).order_by('short_name')
    return render(request, 'findyourteam.html', {'bfteams':bfteams, 'group':group})

def baseball(request, group):
    bfteams = Team.objects.only('short_name').filter(sport='mlb').order_by('short_name')
    return render(request, 'findyourteam.html', {'bfteams':bfteams, 'group':group})

def nba(request, group):
    bfteams = Team.objects.only('short_name').filter(sport='nba').order_by('short_name')
    return render(request, 'findyourteam.html', {'bfteams':bfteams, 'group':group})

def nascar(request, group):
    bfteams = Team.objects.only('short_name').filter(sport='nascar').order_by('short_name')
    return render(request, 'findyourteam.html', {'bfteams':bfteams, 'group':group})

def creditcard(request):
   return render(request, 'creditcard.html', {'':''})

def teamview(request, team, form_errors=None):
   try:
      request.session['bfteam'] = Team.objects.get(short_name=team)
   except:
      return redirect('http://www.bigfanmail.com')
      
   request.session['domain_list'] = Domain.objects.filter(team=request.session['bfteam'])
   return render(request, 'search/teamview.html', {'team':team, 'domain_list': request.session['domain_list'],'form_errors':form_errors})

def register(request):
   return render(request, 'base_generic.html', {'team':team})

def bflogin(request):
   username = request.POST['username']
   password = request.POST['password']
   user = authenticate(username=username, password=password)
   if user is not None:
        if user.is_active:
            login(request, user)
            return redirect(request.POST['next'])
        else:
            return "User is not active"
            # Return a 'disabled account' error message
   else:
        # Return an 'invalid login' error message.
        error="Login failed."
        nexturl  = request.POST['next']
        return render(request, 'base_generic.html',{'error': error, 'nexturl': nexturl})

@login_required
def bflogout(request):
   logout(request)
   return redirect('/')

@login_required
def users(request):
   request.session['bfacct'] = Account.objects.filter(customer=request.user) 
   return render(request, 'user_account.html',{})

@require_POST
def changepassword(request):
   error=""
   if request.user.check_password(request.POST['old_password']):
      if request.POST['new_password1'] == request.POST['new_password2']:
        request.user.set_password(request.POST['new_password1'])
        request.user.save()
      else:
        error="Passwords don't match."
   else:
      error="Old password is not correct."
   return render(request, 'registration/password_change_form.html',{'error':error})

def forgotpassword(request):
   if 'username' in request.POST:
      username = request.POST['username']
      request.session['saveuser'] = username 
      try:
         bfuser = BFCustomer.objects.get(username__iexact=username)
         secquest = CustomerAnswer.objects.get(customer=bfuser)
         secquest2 = SecurityQuestion.objects.get(pk=secquest.security_question.id)
      except:
         return render(request, 'forgot_password.html',{'error':'We cannot find your username'})
      return render(request, 'forgot_password.html',{'question':secquest2})
      
   if 'secanswer' in request.POST:
      username = request.session['saveuser']
      bfuser = BFCustomer.objects.get(username__iexact=username)
      if CustomerAnswer.objects.get(customer=bfuser.id, answer__iexact=request.POST['secanswer']):
         return render(request, 'forgot_password.html', {})

   if 'newp1' in request.POST and 'newp2' in request.POST:
      if request.POST['newp1'] == request.POST['newp2']:
         bfuser = BFCustomer.objects.get(username__iexact=request.session['saveuser'])
         try:
            logger.debug('user: ' + bfuser.username)
            bfuser.set_password(request.POST['newp1'])
            bfuser.save()
            return render(request, 'forgot_password.html', {'success': 'success'})
         except:
            return render(request, 'forgot_password.html', {'failure': 'failure'})
      else:
         error="Your passwords do not match."
         return render(request, 'forgot_password.html',{'error': error})
   return render(request, 'forgot_password.html',{})

def bfname_registration(request, form_class=None):
    if request.user.username:
        form = form_class({
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            })

    #variables directly from the form
    local_name = request.POST['nickname']
    domain = request.POST['select_domain']

    #get stuff
    first_name = request.user.first_name
    last_name = request.user.last_name

    #variables generated from the form
    bfmail = local_name + domain
    first_initial = first_name[0:1]
    last_initial = last_name[0:1]
    suggest1 = local_name + str(randint(100,999))
    suggest2 = first_initial + request.user.last_name
    suggest3 = first_name + "." + last_name
    suggest4 = local_name + first_initial + last_initial

    try:
        get_bfname = BFName.objects.get(bfname=local_name)
    except BFName.DoesNotExist:
        get_bfname = 'DoesNotExist'

    if(get_bfname != 'DoesNotExist'):
        return render(request, 'search/username_registration.html',{
            'suggest1': suggest1,
            'suggest2': suggest2,
            'suggest3': suggest3,
            'suggest4': suggest4,
            'local_name': local_name,
            'domain': domain,
            'bfmail': bfmail,
            })
    else:
        data2 = BFName()
        data2.domain_id = Domain.objects.get(domain_name=domain)
        data2.bfname = local_name #form.data["bfname"]
        data2.product = Product.objects.get(pk=1)
        data2.save()
        return HttpResponse("User " + bfmail + " successfully registered")

def bfname_usersearch(request, form_class=None):
    #defaults
    #Get info from the form, removing spaces.
    first_name = request.POST['first_name'].replace(' ','')
    last_name  = request.POST['last_name'].replace(' ','')
    nickname   = request.POST['nickname'].replace(' ','')
    occupation = EAddress(request.POST['occupation'].replace(' ',''))

    """
    DECIDE CASE OF WHAT IS FILLED IN AND WHAT IS NOT
    """
    # if NOTHING is filled in...
    if not first_name and not last_name and not nickname and not occupation.get_eaddress():
       form_errors="Please fill in one of the search fields."
       return render(request, 'search/teamview.html', {'team':request.session['bfteam'].short_name, 'domain_list':request.session['domain_list'], 'form_errors':form_errors})
    else:
       #domain     = request.POST['select_domain']
       finame     = EAddress(request.POST['first_name'].replace(' ',''))
       team       = request.session['bfteam'].short_name.replace(' ','')

    """
    # if there is a first and last name 
    """
    if first_name and last_name:
        suggestion1 = EAddress(first_name[0] + last_name)
        suggestion2 = EAddress(first_name + last_name[0])
        suggestion3 = EAddress(first_name + last_name)
        suggestion4 = EAddress(first_name + "." + last_name)
    else:
        suggestion1 = EAddress("")
        suggestion2 = EAddress("")
        suggestion3 = EAddress("")
        suggestion4 = EAddress("")

    if nickname:
        logger.debug('Nickname: ' + nickname)
        nname = EAddress(nickname)
    else:
        nname = EAddress("")

    doms = Domain.objects.filter(team__short_name__iexact=team)
    for dom in doms:

       domain = dom.domain_name
       users_in_domain = BFName.objects.filter(domain__domain_name__iexact=domain)

       if users_in_domain.exists():
         if not (users_in_domain.filter(bfname=nname.get_eaddress()).exists()):
           if nname.get_eaddress():
              bfname_conf(nname, users_in_domain, domain)

         if not (users_in_domain.filter(bfname=occupation.get_eaddress()).exists()):
           if occupation.get_eaddress():
              bfname_conf(occupation, users_in_domain, domain)

         if not (users_in_domain.filter(bfname=finame.get_eaddress()).exists()):
           if finame.get_eaddress():
              bfname_conf(finame, users_in_domain, domain)

         if not (users_in_domain.filter(bfname=suggestion1.get_eaddress()).exists()):
           if suggestion1.get_eaddress():
              bfname_conf(suggestion1, users_in_domain, domain)

         if not (users_in_domain.filter(bfname=suggestion2.get_eaddress()).exists()):
           if suggestion2.get_eaddress():
              bfname_conf(suggestion2, users_in_domain, domain)

         if not (users_in_domain.filter(bfname=suggestion3.get_eaddress()).exists()):
           if suggestion3.get_eaddress():
              bfname_conf(suggestion3, users_in_domain, domain)

         if not (users_in_domain.filter(bfname=suggestion4.get_eaddress()).exists()):
           if suggestion4.get_eaddress():
              bfname_conf(suggestion4, users_in_domain, domain)
       else:
         if nname.get_eaddress():
            logger.debug('nname eaddress: ' + nname.get_eaddress())
            bfname_conf(nname, users_in_domain, domain)

         if occupation.get_eaddress():
            bfname_conf(occupation, users_in_domain, domain)

         if finame.get_eaddress():
            bfname_conf(finame, users_in_domain, domain)

         if first_name and last_name:
            if suggestion1.get_eaddress():
               bfname_conf(suggestion1, users_in_domain, domain)
            if suggestion2.get_eaddress():
               bfname_conf(suggestion2, users_in_domain, domain)
            if suggestion3.get_eaddress():
               bfname_conf(suggestion3, users_in_domain, domain)
            if suggestion4.get_eaddress():
               bfname_conf(suggestion4, users_in_domain, domain)

       if not suggestion1.is_registered() and suggestion1.get_plan() != 'trialstandard':
         suggestion1.set_is_registered(1)

       if not suggestion2.is_registered() and suggestion2.get_plan() != 'trialstandard':
         suggestion2.set_is_registered(1)

       if not suggestion3.is_registered() and suggestion3.get_plan() != 'trialstandard':
         suggestion3.set_is_registered(1)

       if not suggestion4.is_registered() and suggestion4.get_plan() != 'trialstandard':
         suggestion4.set_is_registered(1)

       #if not nname.is_registered() and nname.get_plan() != 'trialstandard':
       #  nname.set_is_registered(1)

       if not occupation.is_registered() and occupation.get_plan() == 'trialpremium':
         occupation.set_is_registered(1)

    return render(request, 'search/teamview.html',{
        'first_name': first_name,
        'last_name': last_name,
        'occupation': occupation,
        'nname': nname,
        'finame': finame,
        'suggestion1': suggestion1,
        'suggestion2': suggestion2,
        'suggestion3': suggestion3,
        'suggestion4': suggestion4,
        'domain': domain,
        'team': team,
        })

def bfname_conf(bfobj, users_in_domain, domain): 
    bfobj.set_try_eaddress(domain)
    bfobj.set_is_registered(0)
    if Occupation.objects.filter(occupation__iexact=bfobj.get_eaddress()).exists():
        bfobj.set_plan('ultra-premium')
    elif CommonName.objects.filter(common_name__iexact=bfobj.get_eaddress()).exists():
        bfobj.set_plan('trialpremium')
    else:
        bfobj.set_plan('trialstandard')
