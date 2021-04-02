from django.contrib import admin
from stripe_subscription.models import *
# Register your models here.

admin.site.register(customer)
admin.site.register(subscription)
