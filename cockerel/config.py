import os
import configparser


class Config:
    def __init__(self, config_file):
        config = configparser.ConfigParser()

        if not config.read(config_file, encoding='utf-8'):
            print('Config File not found or not readable...')
            os._exit(1)

        self.login_token = config.get('Credentials', 'bot_token')

        self.cmd_prefix = config.get('Bot', 'cmd_prefix')

        self.director_role = config.get('Permissions', 'director_role')
        self.admin_role = config.get('Permissions', 'admin_role')


class ConfigDefault:
    options_file = 'config/setting.ini'
