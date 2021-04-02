from django.apps import AppConfig


class PaypalPaymentConfig(AppConfig):
    name = 'paypal_payment'

    def ready(self):
        # import signal handlers
        import paypal_payment.signals
