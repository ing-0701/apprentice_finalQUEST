
from django.contrib import admin
from .models import Texts, GatekeeperFlag, MinisterFlags

admin.site.register(Texts)
admin.site.register(GatekeeperFlag)
admin.site.register(MinisterFlags)
