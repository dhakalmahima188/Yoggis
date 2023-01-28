from django.core.management.base import BaseCommand
# from yoggis.views import sendMessage
from twilio.rest import Client
import schedule
import time


def sendMessage():
    # Twilio account SID and auth token
    account_sid = 'ACb1f5211276b92b89d72bca9b91467ffd'
    auth_token = 'fb5f4197ff6cf48fa678648599a0816d'

    # create a Twilio client
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+9779840044672", 
        from_="+16068067346",
        body='Hello, its a yoga time ! Get fresh and be ready !'
    )

class Command(BaseCommand):
    help = 'Run my_function'

    def handle(self, *args, **options):
        schedule.every().day.at("13:15").do(sendMessage)
        while True:
            schedule.run_pending()
            time.sleep(1)