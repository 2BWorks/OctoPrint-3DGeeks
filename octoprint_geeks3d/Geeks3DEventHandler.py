class Geeks3DEventHandler:

	current_file = ""
	progress = 0

	def __init__(self, plugin):
		self._plugin = plugin
		self._logger = plugin.logger


	def handle_event(self, event, payload):
		self._logger.info("Event: %s" % event)
		self._logger.info("Payload: %s " % payload)

		if event == "PrintStarted":
			self._logger.info("Print started")
			self.current_file = payload["name"]
			if self._plugin.settings.get_boolean(['push_print_started']):
				self._logger.info("Send started")
				self._plugin.pusher.send_push(
					self.create_payload_dict("started")
				)
		elif event == "PrintProgress":
			self.progress = payload["progress"]
			if self.progress != 0:
				if self._plugin.settings.get_boolean(["push_print_progress"]):
					if self.progress % self._plugin.settings.get_int(["push_print_progress_interval"]) == 0:
						self._plugin.pusher.send_push(
							self.create_payload_dict("progress")
						)

		elif event == "PrintPaused":
			if self._plugin.settings.get_boolean(['push_print_paused']):
				self._plugin.pusher.send_push(
					self.create_payload_dict("paused")
				)

		elif event == "PrintResumed":
			if self._plugin.settings.get_boolean(['push_print_resumed']):
				self._plugin.pusher.send_push(
					self.create_payload_dict("resumed")
				)
		elif event == "PrintCancelling":
			if self._plugin.settings.get_boolean(['push_print_cancelled']):
				self._plugin.pusher.send_push(
					self.create_payload_dict("cancelled")
				)
		elif event == "PrintFailed":
			if self._plugin.settings.get_boolean(['push_print_failed']):
				self._plugin.pusher.send_push(
					self.create_payload_dict("failed")
				)
		elif event == "PrintDone":
			if self._plugin.settings.get_boolean(['push_print_finished']):
				self._plugin.pusher.send_push(
					self.create_payload_dict("finished")
				)

		elif event == "TestNotification":
			self._plugin.pusher.send_push(
				self.create_payload_dict("test")
			)

		elif event == "Connected":
			if self._plugin.settings.get_boolean(['push_server_connected']):
				self._plugin.pusher.send_push(
						self.create_payload_dict("connected")
					)

		elif event == "Disconnected":
			if self._plugin.settings.get_boolean(['push_server_disconnected']):
				self._plugin.pusher.send_push(
					self.create_payload_dict("disconnected")
				)

		elif event == "Shutdown":
			if self._plugin.settings.get_boolean(['push_server_shutdown']):
				self._plugin.pusher.send_push(
					self.create_payload_dict("shutdown")
				)

		elif event == "Startup":
			if self._plugin.settings.get_boolean(['push_server_startup']):
				self._plugin.pusher.send_push(
					self.create_payload_dict("startup")
				)


	def create_payload_dict(self, event):
		return dict(
			event=event,
			print=self.current_file,
			percent=self.progress
		)


