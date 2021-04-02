from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.views.generic import TemplateView
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from django.views.generic import ListView
from paypal_payment.models import *
from .forms import SubscriptionForm
from django.conf import settings


def index(request):
    return render(request, 'paypal_payment/index.html')


class PaypalFormView(FormView):
    template_name = 'paypal_payment/paypal_form.html'
    form_class = PayPalPaymentsForm

    def get_initial(self):
        return {
            "business": 'your-paypal-business-address@example.com',
            "amount": 20,
            "currency_code": "EUR",
            "item_name": 'Example item',
            "invoice": 1234,
            "notify_url": self.request.build_absolute_uri(reverse('paypal/paypal-ipn')),
            "return_url": self.request.build_absolute_uri(reverse('paypal-return')),
            "cancel_return": self.request.build_absolute_uri(reverse('paypal-cancel')),
            "lc": 'EN',
            "no_shipping": '1',
        }


class PaypalReturnView(TemplateView):
    template_name = 'paypal_payment/paypal_success.html'


class PaypalCancelView(TemplateView):
    template_name = 'paypal_payment/paypal_cancel.html'


class ProductView(ListView):
    template_name = 'paypal_payment/product.html'

    def get(self, request):
        product_obj = Product.objects.all()
        return render(request, self.template_name, {'product': product_obj})


def subscription(request):
    if request.method == 'POST':
        f = SubscriptionForm(request.POST)
        if f.is_valid():
            request.session['subscription_plan'] = request.POST.get('plans')
            return redirect('process_subscription')
    else:
        f = SubscriptionForm()
    return render(request, 'paypal_payment/subscription_form.html', locals())


def process_subscription(request):

    subscription_plan = request.session.get('subscription_plan')
    host = request.get_host()

    if subscription_plan == '1-month':
        price = "10"
        billing_cycle = 1
        billing_cycle_unit = "M"
    elif subscription_plan == '6-month':
        price = "50"
        billing_cycle = 6
        billing_cycle_unit = "M"
    else:
        price = "90"
        billing_cycle = 1
        billing_cycle_unit = "Y"

    paypal_dict = {
        "cmd": "_xclick-subscriptions",
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        "a3": price,  # monthly price
        "p3": billing_cycle,  # duration of each unit (depends on unit)
        "t3": billing_cycle_unit,  # duration unit ("M for Month")
        "src": "1",  # make payments recur
        "sra": "1",  # reattempt payment on payment error
        "no_note": "1",  # remove extra notes (optional)
        'item_name': 'Content subscription',
        'custom': 1,     # custom data, pass something meaningful here
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('paypal-return')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('paypal-cancel')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")
    return render(request, 'paypal_payment/process_subscription.html', locals())

