from django.http import HttpResponse


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request
        print("--init-- starts>>>>:")
    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        print("handle_event starts>>>>:")
        print('--------------------------')
        intent1 = event.data.object
        print(intent1)
        print('--------------------------')
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)
    
    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        print("handle_payment_intent_succeeded starts>>>>:")
        print('--------------------------')
        intent2 = event.data.object
        print(intent2)
        print('--------------------------')
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
    
    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        print("handle_payment_intent_payment_failed starts>>>>:")
        print('--------------------------')
        intent3 = event.data.object
        print(intent3)
        print('--------------------------')
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)