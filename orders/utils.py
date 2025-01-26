import africastalking
from django.conf import settings

def send_sms_alert(customer, order, action='placed'):
    username = "sandbox"
    api_key = settings.AFRICASTALKING_API_KEY
    africastalking.initialize(username, api_key)

    sms = africastalking.SMS
    message = f"Order for {order.item} has been {action}. Amount: {order.amount}. Time: {order.time}"
    recipient = customer.phone  

    response = sms.send(message, [recipient])
    print(response)
