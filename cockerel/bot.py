import aiohttp
import asyncio
import discord
from discord.ext.commands.bot import _get_variable

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

    async def cmd_time(self):
        print('time!')
        pass

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
        else:
            await handler()



