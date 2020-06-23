# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import uuid
import flask
import logging
import socket
import threading
import json

from octoprint_geeks3d.Geeks3DApi import Geeks3DApi
from octoprint_geeks3d.Geeks3DEventHandler import Geeks3DEventHandler
from octoprint_geeks3d.Geeks3DPusher import Geeks3DPusher


class Geeks3DPlugin(
	octoprint.plugin.StartupPlugin,
	octoprint.plugin.SettingsPlugin,
	octoprint.plugin.AssetPlugin,
	octoprint.plugin.TemplatePlugin,
	octoprint.plugin.ProgressPlugin,
	octoprint.plugin.ShutdownPlugin,
	octoprint.plugin.EventHandlerPlugin,
	octoprint.plugin.SimpleApiPlugin,
	# octoprint.plugin.WizardPlugin
):

	def __init__(self):
		super(Geeks3DPlugin, self).__init__()
		self._logger = logging.getLogger("octoprint.plugins.geeks3d")
		self.logger = self._logger
		self.settings = self._settings
		self.event_handler = Geeks3DEventHandler(self)
		self.pusher = Geeks3DPusher(self)
		self.api = Geeks3DApi(self)


	# Wizard mix
	# def is_wizard_required(self):
	# 	return True
	#
	# def get_wizard_version(self):
	# 	return 2

	# TemplatePlugin mixin

	def get_template_configs(self):
		return [
			dict(type="settings", name="3D Geeks", custom_bindings=True)
		]

	# def get_template_vars(self):
	# 	return dict(
	# 		push_print_start= self._settings.get_boolean("push_print_start"),
	# 		push_print_progress=self._settings.get_boolean("push_print_progress"),
	# 		push_print_progress_interval=self._settings.get_int("push_print_start"),
	# 		push_print_cancelled=self._settings.get_boolean("push_print_cancelled"),
	# 		push_print_paused=self._settings.get_boolean("push_print_paused"),
	# 		push_print_resumed=self._settings.get_boolean("push_print_resumed"),
	# 		push_print_finished=True,
	# 		push_token=str(uuid.uuid1()),
	# 		test="Test"
	# 	)

	## API mixin

	def get_api_commands(self):
		return self.api.get_calls()

	def on_api_command(self, command, data):

		return self.api.handle_call(command, data)



	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			push_print_started=True,
			push_print_progress=True,
			push_print_progress_interval=50,
			push_print_cancelled=False,
			push_print_paused=False,
			push_print_resumed=False,
			push_print_finished=True,
			push_server_startup=False,
			push_server_shutdown=False,
			push_server_connected=False,
			push_server_disconnected=False,
			push_token=str(uuid.uuid4()),
			server_ip = "0.0.0.0",
			server_port = "80",
			plugin_version = "v1",
			plugin_qr = "{}"
		)

	def on_settings_save(self, data):
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)



##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/geeks3d.js"],
			css=["css/geeks3d.css"]
		)

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
		# for details.
		return dict(
			geeks3d=dict(
				displayName="3D Geeks: OctoPrint Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="2BWorks",
				repo="OctoPrint-3DGeeks",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/2BWorks/OctoPrint-3DGeeks/archive/{target_version}.zip"
			)
		)

	def on_print_progress(self, storage, path, progress):
		self.event_handler.handle_event( "PrintProgress", {
			"progress": progress
		})

	def on_event(self, event, payload):
		self.event_handler.handle_event( event, payload)

	def on_after_startup(self):
		t = threading.Timer(0,self.get_ip_and_save)
		t.start()
		self._settings.save()
		self.settings = self._settings

	def get_ip_and_save(self):
		server_ip = [(s.connect((self._settings.global_get(["server","onlineCheck","host"]), self._settings.global_get(["server","onlineCheck","port"]))), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
		server_port = self._settings.global_get(["server", "port"])
		self._settings.set(["server_ip"], str(server_ip))
		self._settings.set(["server_port"], str(server_port))
		self._settings.save()
		self.create_qr()

	def create_qr(self):
		self._settings.set(["plugin_qr"], json.dumps(
			{
				"host" : self._settings.get(["server_ip"]),
				"port" : self._settings.get(["server_port"]),
				"key" : self._settings.global_get(["api", "key"]),
				"name" : self._settings.global_get(["appearance", "name"]),
				"color" : self._settings.global_get(["appearance","color"]),
				"version" : self._settings.get(["plugin_version"]),
				"webcam_enabled" : self._settings.global_get(["webcam", "webcamEnabled"]),
				"webcam_stream" : self._settings.global_get(["webcam", "stream"]),
				"webcam_snapshot" : self._settings.global_get(["webcam", "snapshot"]),
				"bitrate" : self._settings.global_get(["webcam", "bitrate"]),
				"push_token" : self._settings.get(["push_token"])
			}
		))

		self._settings.save()



# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py


# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "3D Geeks: OctoPrint Plugin"


# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
# __plugin_pythoncompat__ = ">=2.7,<3" # only python 2
# __plugin_pythoncompat__ = ">=3,<4" # only python 3
# __plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3
__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = Geeks3DPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
