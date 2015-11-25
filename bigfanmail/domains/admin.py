from django.contrib import admin
from bigfanmail.domains.models import Domain, BFName, Team, SecurityQuestion, CustomerAnswer, Account

admin.site.register(Domain)
admin.site.register(BFName)
admin.site.register(Team)
admin.site.register(SecurityQuestion)
admin.site.register(CustomerAnswer)
admin.site.register(Account)
