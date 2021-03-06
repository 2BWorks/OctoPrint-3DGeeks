import requests


class Geeks3DPusher:
	def __init__(self, plugin):
		self._logger = plugin.logger
		self._plugin = plugin


	def send_push(self, payload):
		headers = {
			"Content-type": "application/json"
		}
		url = "https://qx8eve27wk.execute-api.eu-west-2.amazonaws.com/prod/octoprint_push"
		data = {
			"token" : self._plugin.settings.get(["push_token"]),
			"event" : payload["event"],
			"printer" : self._plugin.settings.global_get(["appearance", "name"]),
			"print" : payload["file"],
			"percent" : payload["percent"]
		}
		requests.post(url, headers=headers, json=data)

