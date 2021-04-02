from django.shortcuts import render
from django.views.generic import ListView
from stripe_subscription.models import *
from django.conf import settings
import stripe
import json
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse, HttpResponse


class subscription_retrieve(ListView):

    def get(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        sub_obj = subscription.objects.get(id=6)
        sub_res = stripe.Subscription.retrieve(sub_obj.subscription_id)
        print(sub_res.plan)
        return render(request, 'stripe_subscription/subscription.html', {'subscription': sub_res.plan})


@csrf_exempt
def create_subscription_session(request, price_id):
    if request.method == 'POST':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.api_key = "sk_test_51IYmNtSAfNxM2KGTAuE6zOUi10h2784XF1xCoopKEnNZt25G5K5tBtQYbWcDW66ECgNeD7ACdWn6rwgaMl4rxpfv00egIRqA8T"
        data = price_id
        # sub_list = stripe.Product.retrieve(price_id)
        # print(sub_list)
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + 'payment/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'payment/cancelled/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': price_id,
                        'quantity': 1
                    }
                ]
            )
            print(checkout_session['id'])
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)})
