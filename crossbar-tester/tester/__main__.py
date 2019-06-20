from os import environ


from .base import Tester
from .wampcra import kWampCRATester


auth_type = environ.get('AUTHTYPE', 'ticket')

if auth_type == 'wampcra':
    tester = kWampCRATester()
else:
    tester = Tester()

tester.run()
