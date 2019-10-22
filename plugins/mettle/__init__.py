import os

import click

from objection.commands.filemanager import _path_exists_ios, _upload_ios, _path_exists_android, _upload_android
from objection.state.device import device_state, Ios, Android
from objection.state.connection import state_connection
from objection.utils.plugin import Plugin


class MettleLoader(Plugin):
    """ MettleLoader loads Mettle """

    def __init__(self, ns):
        """
            Creates a new instance of the plugin

            :param ns:
        """

        implementation = {
            'meta': 'Work with Mettle',
            'commands': {
                'load': {
                    'meta': 'Load mettle',
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

        self.mettle_dylib = 'mettle.dylib'
        self.mettle_droid = 'mettle'

    def load_mettle(self, args: list):
        """
            Loads mettle.

            :param args:
            :return:
        """
        agent = state_connection.get_api()
        environment = agent.env_runtime()
        if environment == 'android':
            self.device_jar_path = os.path.join(agent.env_android_paths()['cacheDirectory'], self.mettle_droid).replace("\\","/")
            if not _path_exists_android(self.device_jar_path):
                print('MettleDroid not uploaded, uploading...')
                if not self._upload_mettledroid(self.device_jar_path):
                    print('Error uploading mettle')
                    return
        else:
            device_dylib_path = os.path.join(agent.env_ios_paths()['DocumentDirectory'], self.mettle_dylib)
            if not _path_exists_ios(device_dylib_path):
                print('Mettle not uploaded, uploading...')
                if not self._upload_mettleios(device_dylib_path):
                    return
            click.secho('Loading dylib...', dim=True)
            self.api.init_mettle(self.mettle_dylib)
        click.secho('Mettle should be loaded! You can now issue the connect command.', fg='green')

    def _upload_mettleios(self, location: str) -> bool:
        """
            Uploads Mettle to the remote filesystem.

            :return:
        """

        local_mettle = os.path.join(os.path.abspath(os.path.dirname(__file__)), self.mettle_dylib)
        if not os.path.exists(local_mettle):
            click.secho('{0} not available next to plugin file. Please build it and copy it there!'.format(
                self.mettle_dylib), fg='red')
            return False

        _upload_ios(local_mettle, location)

        return True
	
    def _upload_mettledroid(self, location: str) -> bool:
        """
            Uploads MettleDroid to the remote filesystem.

            :return:
        """

        local_mettledroid = os.path.join(os.path.abspath(os.path.dirname(__file__)), self.mettle_droid).replace("\\","/")
        if not os.path.exists(local_mettledroid):
            click.secho('{0} not available next to plugin file. Please build it and copy it there!'.format(
                self.mettle_droid), fg='red') 
            return False

        _upload_android(local_mettledroid, location)

        return True	
	
    def connect_mettle(self, args: list):
        if len(args) < 2:
            click.secho("Usage: plugin mettle connect <ip> <port>")
            return

        ip = args[0]
        port = args[1]

        click.secho("Connecting to {}:{}".format(ip, port), dim=True)
        agent = state_connection.get_api()
        environment = agent.env_runtime()
        if environment == 'android':
            self.api.connect_mettle_android(self.device_jar_path, ip, port)
        else:
            self.api.connect_mettle_android(self.mettle_dylib, ip, port)


namespace = 'mettle'
plugin = MettleLoader
