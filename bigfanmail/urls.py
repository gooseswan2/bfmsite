from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.auth.forms import PasswordChangeForm 
from bigfanmail.domains.models import UserRegistrationForm
import bigfanmail.regbackend

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^findyourteam/$', 'bigfanmail.views.findyourteam', ),
     url(r'^bflogout/$', 'bigfanmail.views.bflogout', {}),
     url(r'^bflogin/$', 'bigfanmail.views.bflogin', {}),
     url(r'^bfsearch/$', 'bigfanmail.views.teamview', {}),
    # register https always:
     url(r'^register/$', 'registration.views.register', {'backend': 'registration.backends.simple.SimpleBackend', 'form_class': UserRegistrationForm }, name='registration_register'),
     url(r'^register/teampage/(?P<team>\w+)/$', 'bigfanmail.views.teamview',{} ),
     url(r'^register/username_search/$', 'bigfanmail.views.bfname_usersearch', {}),
     url(r'^register/bfsubscribe/', 'bigfanmail.customers.views.subscribe'),
     url(r'^register/get_host_password/', 'bigfanmail.customers.views.get_host_password'),
     url(r'^register/registration_complete/$', 'bigfanmail.customers.views.registration_complete',{'bfemail':'bfemail'},name='registration_complete'),
     url(r'^profile/$', 'bigfanmail.views.users', ),
     url(r'^editprofile/$', 'bigfanmail.customers.views.editusers', ),
     url(r'^editaccount/(?P<idno>\d+)/$', 'bigfanmail.customers.views.editacct', ),
     url(r'^saveprofile/$', 'bigfanmail.customers.views.saveusers', ),
     url(r'^savepassword/$', 'bigfanmail.customers.views.save_emailpassword', ),
     url(r'^saveaccount/$', 'bigfanmail.customers.views.save_account', ),
     url(r'^forgotpassword/$', 'bigfanmail.views.forgotpassword', ),
     url(r'^features/$', TemplateView.as_view(template_name="features.html")),
     url(r'^partners/$', TemplateView.as_view(template_name="partners.html")),
     url(r'^support/$', TemplateView.as_view(template_name="support/support.html")),
     url(r'^terms/$', TemplateView.as_view(template_name="terms.html")),
     url(r'^privacy/$', TemplateView.as_view(template_name="privacy.html")),
     url(r'^passwordchange/$', 'bigfanmail.views.changepassword', {}),
     url(r'^passwordform/$', 'django.contrib.auth.views.password_change', {'template_name': 'registration/password_change_form.html', 'post_change_redirect': '/passwordchange/'}),
     url(r'^username_registration/$', 'bigfanmail.views.bfname_registration'),#, {'template_name': 'search/username_registration.html'}),

    #These are the team page urls
     url(r'^payments/', include('payments.urls')),
     url(r'^registration_complete/', 'bigfanmail.customers.views.registration_complete', {}),
     url(r'^testregform/', 'bigfanmail.test.regcom'),
     url(r'^testhash/', 'bigfanmail.test.testhash'),

     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^(?P<group>\w+)/$', 'bigfanmail.views.sports', ),
     url(r'^/$', 'bigfanmail.views.homepage', ),
     url(r'^$', 'bigfanmail.views.homepage', ),
)
