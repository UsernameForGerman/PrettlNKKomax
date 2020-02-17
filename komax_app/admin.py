from django.contrib import admin
from .models import Laboriousness, HarnessAmount, Harness, Komax, KomaxTask, EmailUser, Kappa


admin.site.register(Laboriousness)
admin.site.register(Harness)
admin.site.register(HarnessAmount)
admin.site.register(Komax)
admin.site.register(Kappa)
admin.site.register(KomaxTask)
admin.site.register(EmailUser)

