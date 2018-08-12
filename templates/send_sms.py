from twilio.rest import Client


key_sid = 'SK409fa36694e7485f65b0555967049ea6'
key_secret = 'I1Dk5CNXJ4HUdCqzZDOFVUuQx37HTkwb'
account_sid = 'AC24d6453f31a2a287184cca63d796ad38'
client = Client(key_sid, key_secret, account_sid)

message = client.messages.create(
                              body='Hello there Bee!',
                              from_='+14159804992',
                              to='+17045176027')
print message
print message.sid
