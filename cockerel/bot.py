import aiohttp
import asyncio
import discord

from cockerel.config import Config, ConfigDefault


class Cockerel(discord.Client):

    def __init__(self):
        self.ok = False
        self.config = Config(config_file=ConfigDefault.options_file)
        super().__init__()
        self.aiosession = aiohttp.ClientSession(loop=self.loop)

    async def on_ready(self):

        print('ready!')

        self.ok = True

    def run(self):

        try:
            self.loop.run_until_complete(self.start(self.config.login_token))
        except:
            pass

