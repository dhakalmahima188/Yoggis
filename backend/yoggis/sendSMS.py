from twilio.rest import Client
# from scheduler.models import Event

# Twilio account SID and auth token
account_sid = 'ACb1f5211276b92b89d72bca9b91467ffd'
auth_token = 'fb5f4197ff6cf48fa678648599a0816d'


client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+9779840044672", 
    from_="+16068067346",
    body="Yoga!")

print(message.sid)