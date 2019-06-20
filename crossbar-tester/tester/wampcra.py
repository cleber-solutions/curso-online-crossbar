from os import environ

from .base import Tester


class kWampCRATester(Tester):
    async def onConnect(self):
        self.join(self.config.realm, [u"wampcra"], environ['AUTHID'])
        await self.ready()
