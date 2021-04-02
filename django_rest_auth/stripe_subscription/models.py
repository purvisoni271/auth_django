from django.db import models
from auth_rest_app.models import User
from django.conf import settings
import stripe


class customer(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=250)


class subscription(models.Model):
    customer_id = models.ForeignKey(customer, on_delete=models.CASCADE)
    price_id = models.CharField(max_length=250)
    subscription_id = models.CharField(
        max_length=250, default='', null=True, blank=True, help_text='Do not fill subscription id value')

    def save(self, *args, **kwargs):
        price_id = self.price_id
        customer_id = customer.objects.get(id=self.customer_id.id)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription_data = stripe.Subscription.create(customer=customer_id.customer_id,
                                                       items=[
                                                           {"price": price_id}
                                                       ])
        self.subscription_id = subscription_data.id
        super(subscription, self).save(*args, **kwargs)
