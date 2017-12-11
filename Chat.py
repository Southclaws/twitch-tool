import sys
import itertools
import threading
import pydle


TWITCH_HOST = "irc.chat.twitch.tv"
TWITCH_PORT = 6667


class Chat(pydle.Client):

	def setup(self, chat_input, chat_log):

		self.chat_input = chat_input
		self.chat_log = chat_log
		self.memb = False

		self.print_line("SYS", "Chat module initiated with: %s:%d"%(TWITCH_HOST, TWITCH_PORT))

	def update_commands(self, commands):
		self.commands = commands

	def do_connect(self, chan, nick, auth, commands):
		self.print_line("SYS", "Connecting to: %s:%d #%s as %s"%(TWITCH_HOST, TWITCH_PORT, chan, nick))

		self.chan = "#" + chan
		self.nick = nick
		self.auth = auth
		self.commands = commands

		#try:
		#	self.connect(TWITCH_HOST, TWITCH_PORT, password=self.auth)
		#	self.thrd = threading.Thread(target=self.handle_forever)
		#	self.thrd.start()

		#except OSError as e:
		#	self.print_line("SYS", "OSError: %s"%(e))
			
	def on_connect(self):
		self.print_line("SYS", "Connected!")

		self.join(self.chan)
		super().on_connect()

	def on_raw_join(self, message):
		print("SYS", "Requesting membership")
		self._send("CAP REQ :twitch.tv/membership")

		super().on_raw_join(message)

	def on_join(self, channel, user):
		self.print_line("SYS", "%s joined %s"%(user, channel))
		super().on_join(channel, user)

	def on_disconnect(self, expected):
		if expected:
			self.print_line("SYS", "Disconnected")

		else:
			self.print_line("SYS", "Unexpectedly disconnected!")

	def on_raw(self, message):
		print("RAW", message._raw)
		super().on_raw(message)

	def _send(self, data):
		print("OUT", data)
		super()._send(data)


	def on_message(self, target, source, message):
		self.print_line(source, message)

		for i in self.commands:
			if i['trg'] == message:
				self.message_send(i['msg'])


	# Interface


	def message_send(self, text):

		self.print_line(self.nick, text)

		#self.message(self.chan, text)

		return

	def chat_send(self):
		text = self.chat_input.get()

		if text == "":
			return

		self.message_send(text)

		return

	def print_line(self, user, message):
		self.chat_input.set("")
		self.chat_log.insert("0.0", user + ": " + message + '\n')
