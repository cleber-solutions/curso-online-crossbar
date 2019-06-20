import sys

from autobahn.asyncio.wamp import ApplicationRunner
from prettyconf import config

from .wamp import WampClient

URL = config('WAMP_URL', default='ws://crossbar.dronemapp.com:80/ws')
REALM = config('WAMP_REALM', default='kotoko')

runner = ApplicationRunner(URL, REALM)
try:
    runner.run(WampClient)
except OSError as ex:
    print('OSError:', ex)
    sys.exit(100)
