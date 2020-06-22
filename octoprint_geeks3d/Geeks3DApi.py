import uuid
import flask


class Geeks3DApi:

	def __init__(self, plugin):
		self._plugin = plugin

	def get_calls(self):
		return dict(
			new_token=[],
			get_token=[],
			check=[],
			test_notification=[]
		)

	def handle_call(self, command, data):
		if command == "new_token":
			return self.new_token()
		if command == "get_token":
			return self.get_token()
		if command == "check":
			return self.check()
		if command == "test_notification" :
			return self.test_notification()
		return None

	def new_token(self):
		token = str(uuid.uuid4())
		self._plugin.settings.set(["push_token"], token)
		self._plugin.settings.save()
		return flask.jsonify(dict(code=200, token=token))

	def check(self):
		return flask.jsonify(dict(code=200))

	def get_token(self):
		return flask.jsonify(dict(code=200, token=self._plugin.settings.get(["push_token"])))

	def test_notification(self):
		self._plugin.event_handler.handle_event("TestNotification", {})
		return flask.jsonify(dict(code=200))
