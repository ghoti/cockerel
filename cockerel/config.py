import os
import configparser


class Config:
    def __init__(self, config_file):
        config = configparser.ConfigParser()

        if not config.read(config_file, encoding='utf-8'):
            print('Config File not found or not readable...')
            os._exit(1)

        self.login_token = config.get('Credentials', 'bot_token')


class ConfigDefault:
    options_file = 'config/setting.ini'
