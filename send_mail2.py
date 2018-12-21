from twilio.rest import Client
from secrets.sh import twil_SID, twil_token


# Your Account Sid and Auth Token from twilio.com/console
account_sid = twil_SID
auth_token = twil_token
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+14159937779',
                     to=
                 )

print(message.sid)