import asyncio
import sys

from autobahn.asyncio.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError
from prettyconf import config

from .authenticator import Authenticator


PRINCIPAL = 'cleber'


class WampClient(ApplicationSession):
    def __init__(self, *args, **kwargs):
        self.exit_status = 0
        super().__init__(*args, **kwargs)

        db_url = config('DATABASE_URL')
        self.authenticator = Authenticator(db_url)

    def onOpen(self, *args, **kwargs):
        print('Opened.')
        super().onOpen(*args, **kwargs)

    def onWelcome(self, *args, **kwargs):
        print('Welcome message received.')
        super().onWelcome(*args, **kwargs)

    def onConnect(self):
        print("Client session connected. Starting WAMP-Ticket authentication on realm '{}' as principal '{}' ..".format(
            self.config.realm, PRINCIPAL)
        )
        self.join(self.config.realm, [u"ticket"], PRINCIPAL)

    async def onJoin(self, details):
        last_exception = None
        for counter in range(0, 3):
            if counter > 0:
                await asyncio.sleep(5)

            try:
                await self.register(self.authenticator.authenticate, 'session_authenticate')
                await self.register(self.authenticator.get_user_data, 'kotoko.kauth.get_user_data')
            except ApplicationError as e:
                last_exception = e
                continue
            else:
                print("Custom WAMP-CRA authenticator registered")
                break
        else:
            print(f"Could not register custom WAMP-CRA authenticator: {last_exception}")
            self.exit_status = 10
            self.disconnect()

    def onChallenge(self, challenge):
        if challenge.method == u"ticket":
            print("WAMP-Ticket challenge received: {}".format(challenge))
            return config('WAMPYSECRET')
        else:
            raise Exception("Invalid authmethod {}".format(challenge.method))

    def onLeave(self, *args, **kwargs):
        # 1 - leave
        super().onLeave(*args, **kwargs)
        print('Left.')

    def onDisconnect(self):
        # 2- disconnect
        super().onDisconnect()
        print("Disconnected.")

    def onClose(self, *args, **kwargs):
        # 3- close
        super().onClose(*args, **kwargs)
        print('Closed.')
        sys.exit(self.exit_status)
