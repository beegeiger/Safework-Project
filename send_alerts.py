from secrets import twil_SID, twil_token, mailgun_private, mail_sandbox
from twilio.rest import Client
import requests


def send_message(recipient, message_text):
	"""Helper Function to send SMS"""
	messaging_api = Client(twil_SID, twil_token)
	message = messaging_api.messages \
                .create(
                     body=message_text,
                     from_='+14159937779',
                     to=recipient
                 )

	return message.sid

def send_email(recipient, email_text):
	"""Helper Function used to send e-mail"""
	request_url = 'https://api.mailgun.net/v3/sw.safeworkproject.org/messages'.format(mail_sandbox)
	request = requests.post(request_url, auth=('api', mailgun_private), data={
						'from': 'alerts@safeworkproject.org',
						'to': recipient,
						'subject': 'Alert From The SafeWork Project',
						'text': email_text
						})
	print('Status: {0}'.format(request.status_code))
	print('Body:   {0}'.format(request.text))
	return request

