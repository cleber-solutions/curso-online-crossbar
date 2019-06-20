from kbaseapp.wamp_app import WampApp, register_method

from .listener import Listener


class kNotifier(WampApp):
    PRINCIPAL = 'cleber'

    def init(self):
        self.listener = Listener(self)

    async def ready(self, *args, **kwargs):
        try:
            await self.listener.listen()
        except KeyboardInterrupt:
            self.listener.close()
            self.disconnect()
