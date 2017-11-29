from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import WageringRequirement

admin.site.register(WageringRequirement, SingletonModelAdmin)
