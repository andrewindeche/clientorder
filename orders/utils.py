import africastalking
from django.conf import settings

def send_sms_alert(customer, order, action='placed'):
    username = "sandbox" 
    api_key = settings.AFRICASTALKING_API_KEY
    africastalking.initialize(username, api_key)

    sms = africastalking.SMS
    message = f"Order for {order.item} has been {action}. Amount: {order.amount}. Time: {order.time.strftime('%Y-%m-%d %H:%M:%S')}"
    
    recipient = customer.phone 
    
    try:
        response = sms.send(message, [recipient])
        print(f"SMS sent successfully to {recipient}")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error sending SMS: {e}")
