import asyncio
import datetime
from decimal import Decimal
import json
from queue import Queue, Empty

import asyncpg
from prettyconf import config


DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'
ACTIONS = {
    'INSERT': 'created',
    'UPDATE': 'updated',
    'DELETE': 'deleted',
}


class Listener:
    def __init__(self, wamp_app):
        self.wamp_app = wamp_app
        self.queue = Queue()

    def on_message(self, db_connection, process_id, topic, message_str):
        message = json.loads(message_str)
        self.queue.put(message)

    async def handle_message(self, message):
        object_id = message['id']
        table_name = message['table']
        app_name, *rest = table_name.split('_')
        model_name = '_'.join(rest)
        operation = message['op']
        action_name = ACTIONS[operation]

        if operation == 'DELETE':
            data = {}
        else:
            data = await self.conn.fetchrow(f'SELECT * FROM {table_name} WHERE id = $1', object_id)
            if data is None:
                return
            data = dict(data)

        for key, value in data.items():
            if isinstance(value, datetime.datetime):
                data[key] = value.strftime(DATETIME_FORMAT)
            elif isinstance(value, datetime.date):
                data[key] = value.strftime(DATE_FORMAT)
            elif isinstance(value, datetime.time):
                data[key] = value.strftime(TIME_FORMAT)
            elif isinstance(value, Decimal):
                data[key] = str(value)

        organization_id = data.get('organization_id', 0)

        topic = f'org.{organization_id}.{app_name}.{model_name}.{action_name}'

        try:
            self.wamp_app.publish(topic, data)
        except Exception as ex:
            print(ex.__class__.__name__, ':', ex)
        else:
            print(topic, ':', data)

    async def handle_messages(self):
        while True:
            try:
                message = self.queue.get(block=False)
            except Empty:
                await asyncio.sleep(5)
                continue

            await self.handle_message(message)

    async def listen(self):
        print('Connecting to database')
        self.conn = await asyncpg.connect(config('DATABASE_URL'))
        print('Starting listener')
        await self.conn.add_listener('wamp_notify', self.on_message)
        print("Waiting for notifications on channel 'wamp_notify'")

        await self.handle_messages()
