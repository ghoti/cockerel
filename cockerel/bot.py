import aiohttp
import asyncio
import discord
from discord.ext.commands.bot import _get_variable
import pendulum
import pyowm

from functools import wraps

from cockerel.config import Config, ConfigDefault


class Cockerel(discord.Client):

    def __init__(self):
        self.ok = False
        self.config = Config(config_file=ConfigDefault.options_file)
        super().__init__()
        self.aiosession = aiohttp.ClientSession(loop=self.loop)

    #only person with minimum role can use this
    def authenticate(func=None, level='Administrator'):
        def _decorate(func):
            @wraps(func)
            async def wrapper(self, *args, **kwargs):
                orig_msg = _get_variable('message')
                for role in orig_msg.author.roles:
                    if role.name == level or not orig_msg:
                        return await func(self, *args, **kwargs)
            return wrapper
        if func:
            return _decorate(func)
        return _decorate

    async def on_ready(self):

        print('ready!')

        self.ok = True

    def run(self):

        try:
            self.loop.run_until_complete(self.start(self.config.login_token))
        except:
            pass

    async def cmd_time(self, *args):
        now = pendulum.utcnow().to_day_datetime_string()
        return 'Current UTC/EVE time: {}'.format(now)

    async def cmd_weather(self, *args):
        owm = pyowm.OWM(self.config.weatherapi)

        if not args:
            conditions = owm.weather_at_place('Reykjavik')
        else:
            conditions = owm.weather_at_place(' '.join(args[0]).strip())
        if conditions:
            return 'Current Conditions of {}: {}F/{}C and {}'.format(conditions.get_location().get_name(),
                                                                     conditions.get_weather().get_temperature(
                                                                         'fahrenheit')['temp'],
                                                                     conditions.get_weather().get_temperature(
                                                                         'celsius')['temp'],
                                                                     conditions.get_weather().get_detailed_status())
        else:
            return 'City not found, try again'

    async def send_typing(self, destination):
        try:
            return await super().send_typing(destination)
        except discord.Forbidden:
            print("Could not send typing to %s, no permssion" % destination)

    async def on_message(self, message):
        await self.wait_until_ready()

        message_content = message.content.strip()
        if message.author == self.user:
            return

        if not message_content.startswith(self.config.cmd_prefix):
            return

        command, *args = message_content.split()
        command = command[len(self.config.cmd_prefix):].lower().strip()

        handler = getattr(self, 'cmd_%s' % command, None)
        if not handler:
            return
        await self.send_typing(destination=message.channel)
        if args:
            return_message = await handler(args)
        else:
            return_message = await handler()

        if return_message:
            await self.send_message(destination=message.channel, content=return_message)



