from django.contrib import admin
from .models import *
from user.models import UserSubscription,Customer
# Register your models here.
admin.site.register(job)
admin.site.register(Package)
admin.site.register(UserSubscription)