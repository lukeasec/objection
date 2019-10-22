import os
import tempfile
import time

import click
from tabulate import tabulate

from objection.state.connection import state_connection
from objection.state.device import device_state, Ios, Android
from objection.state.filemanager import file_manager_state
from objection.commands.filemanager import _path_exists_android, _upload_android
from objection.utils.helpers import sizeof_fmt
from objection.utils.plugin import Plugin

class MettleAndroid(Plugin):
    def __init__(self, ns):
        """
            Creates a new instance of the plugin

            :param ns:
        """

        implementation = {
            'meta': 'Mettle for Android',
            'commands': {
                'load': {
                    'meta': 'Load Mettle',
                    'exec': self.load_mettle
                },
				'connect': {
                    'meta': 'Connect mettle',
                    'exec': self.connect_mettle
                }
            }
        }

        super().__init__(__file__, ns, implementation)

        self.inject()

        self.mettle_droid = 'mettle'
	
    def load_mettle(self, args: list):
        agent = state_connection.get_api()
        device_jar_path = os.path.join(agent.env_android_paths()['cacheDirectory'], self.mettle_droid).replace("\\","/")

        if not _path_exists_android(device_jar_path):
            print('MettleDroid not uploaded, uploading...')
            if not self._upload_mettledroid(device_jar_path):
                return

        click.secho('Asking mettledroid to load...', dim=True)
        self.api.init_mettle()
		
    def _upload_mettledroid(self, location: str) -> bool:
        """
            Uploads MettleDroid to the remote filesystem.

            :return:
        """

        local_mettledroid = os.path.join(os.path.abspath(os.path.dirname(__file__)), self.mettle_droid).replace("\\","/")
        print(local_mettledroid)
        if not os.path.exists(local_mettledroid):
            click.secho('{0} not available next to plugin file. Please build it and copy it there!'.format(
                self.mettle_droid), fg='red') 
            return False

        _upload_android(local_mettledroid, location)

        return True	
		
    def connect_mettle(self, args: list):
        return

namespace = 'mandroid'
plugin = MettleAndroid