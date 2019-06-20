import json
import re
import sys

from autobahn.wamp.types import CallOptions, SubscribeOptions
from kbaseapp.wamp_app import WampApp


class Tester(WampApp):
    PRINCIPAL = 'backend_app'

    async def ready(self):
        method_name = sys.argv[1]

        args = []
        kwargs = {}
        for arg in sys.argv[2:]:
            if arg.startswith('JSON:'):
                value = arg[5:]
                value = json.loads(value)
                args.append(value)
                continue

            parts = re.split('=', arg)
            parts_count = len(parts)
            if parts_count == 1:
                args.append(arg)
            elif parts_count == 2:
                key, value = parts
                kwargs[key] = value

        self.method_name = method_name
        self.args = args
        self.kwargs = kwargs

        def on_progress(i):
            print("Progress: {}".format(i))

        def on_event(event):
            print('Event:', event)

        if self.method_name == 'SUB':
            try:
                topic = self.args[0]
            except IndexError:
                topic = ''
            print('Subscribing to', topic)
            await self.subscribe(on_event, topic, SubscribeOptions(match="prefix"))
            print('Done')

        else:
            print('Calling', self.method_name)
            try:
                x = await self.call(self.method_name, *self.args, **self.kwargs, options=CallOptions(on_progress=on_progress))
            except Exception as ex:
                print(type(ex), ':', ex)
            else:
                print(x)

            self.disconnect()
