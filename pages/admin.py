from django.contrib import admin
from .models import User,Company,Contactus,ContactusCom,ContactusUser,SearchEmployees,login,DataOfCV,Result
# Register your models here.

admin.site.register(User),
admin.site.register(Company),
admin.site.register(Contactus),
admin.site.register(ContactusCom),
admin.site.register(ContactusUser),
admin.site.register(SearchEmployees),
admin.site.register(login),
admin.site.register(DataOfCV),
admin.site.register(Result),
