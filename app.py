import logging
import os
import io
import json
import threading
import time

from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *
from twitch.api import v3 as twitch
from twitch.exceptions import ResourceUnavailableException
import speech_recognition as sr

import Authentication
import AutoMessage
import Commands
from Chat import Chat


class Main:

	def __init__(self, parent):
		self.parent = parent
		self.update_forever = False

		# MAIN PROPERTIES

		self.settings = {
			"nick":"",
			"chan":"",
			"auth":"",
			"rate":10,
			"voic":True,
			"auto":[],
			"cmds":[]}

		self.auto_time_l = threading.Lock()
		self.auto_time = []

		self.load_settings()
		self.save_settings()

		# strip # character, it can be added when needed
		if self.settings["chan"].startswith("#"):
			self.settings["chan"] = self.settings["chan"][1:]

		print(self.settings["nick"])
		print(self.settings["chan"])
		print(self.settings["auth"])
		print(self.settings["rate"])
		print(self.settings["voic"])
		print(self.settings["auto"])
		print(self.settings["cmds"])

		if self.settings["rate"] == None:
			self.settings["rate"] = 10

		self.channel_data = {}

		# CONTROL BUTTONS FRAME

		self.frame_control		= ttk.Frame(self.parent, relief=SUNKEN, width = 50, borderwidth=15)

		self.btn_connect		= ttk.Button(self.frame_control, text = 'Connect', width = 25, command = self.core_connect)
		self.btn_goto_auth		= ttk.Button(self.frame_control, text = 'Authentication', width = 25, command = self.goto_authentication)
		self.btn_auto_msg		= ttk.Button(self.frame_control, text = 'Auto-Messages', width = 25, command = self.goto_auto_message)
		self.btn_commands		= ttk.Button(self.frame_control, text = 'Commands', width = 25, command = self.goto_commands)

		self.lab_followers_s	= StringVar()
		self.lab_followers		= ttk.Label(self.frame_control, textvariable = self.lab_followers_s, width = 25)

		self.lab_last5fol		= ttk.Label(self.frame_control, text = "Last 5 followers:", width = 25)
		self.lst_last5fol		= Listbox(self.frame_control, width = 25, height = 5, activestyle = 'none', takefocus = False, exportselection=False)

		self.lab_views_s		= StringVar()
		self.lab_views			= ttk.Label(self.frame_control, textvariable = self.lab_views_s, width = 25)

		self.lab_status_s		= StringVar()
		self.lab_status			= ttk.Label(self.frame_control, textvariable = self.lab_status_s, width = 25)

		self.lab_game_s			= StringVar()
		self.lab_game			= ttk.Label(self.frame_control, textvariable = self.lab_game_s, width = 25)

		self.lab_streams_s		= StringVar()
		self.lab_streams		= ttk.Label(self.frame_control, textvariable = self.lab_streams_s, width = 25)

		self.lab_popularity_s	= StringVar()
		self.lab_popularity		= ttk.Label(self.frame_control, textvariable = self.lab_popularity_s, width = 25)


		# CHAT AREA FRAME

		self.frame_chat			= ttk.Frame(self.parent, relief=SUNKEN, width = 50, borderwidth=15)

		self.ent_chat_input_s	= StringVar()
		self.ent_chat_input		= ttk.Entry(self.frame_chat, textvariable = self.ent_chat_input_s)
		self.txt_chat_log		= ScrolledText(self.frame_chat, wrap=WORD)

		self.chat				= Chat(self.settings["nick"], realname=self.settings["nick"])
		self.btn_chat_send		= ttk.Button(self.frame_chat, text = 'Send', width=10, command = self.chat.chat_send, state = DISABLED)
		self.chat.setup(self.ent_chat_input_s, self.txt_chat_log)


		# STATUS AREA FRAME

		self.frame_status		= ttk.Frame(self.parent, relief=SUNKEN)

		self.txt_status_s		= StringVar()
		self.txt_status			= ttk.Entry(self.frame_status, textvariable = self.txt_status_s)

		# GRID SETUP

		self.frame_control.grid	(column=0, row=0, sticky=(N, S, E, W))
		self.btn_connect.grid	(column=0, row=0, sticky=(E, W))
		self.btn_goto_auth.grid	(column=0, row=1, sticky=(E, W))
		self.btn_auto_msg.grid	(column=0, row=2, sticky=(E, W))
		self.btn_commands.grid	(column=0, row=3, sticky=(E, W))
		self.lab_followers.grid	(column=0, row=4, sticky=(E, W))
		self.lab_last5fol.grid	(column=0, row=5, sticky=(E, W))
		self.lst_last5fol.grid	(column=0, row=6, sticky=(E, W))
		self.lab_views.grid		(column=0, row=7, sticky=(E, W))
		self.lab_status.grid	(column=0, row=8, sticky=(E, W))
		self.lab_game.grid		(column=0, row=9, sticky=(E, W))
		self.lab_streams.grid	(column=0, row=10, sticky=(E, W))
		self.lab_popularity.grid(column=0, row=11, sticky=(E, W))

		self.frame_chat.grid	(column=1, row=0, sticky=(N, S, E, W))
		self.ent_chat_input.grid(column=0, row=0, sticky=(E, W), columnspan=2)
		self.btn_chat_send.grid	(column=1, row=0, sticky=E)
		self.txt_chat_log.grid	(column=0, row=1, sticky=(N, S, E, W), columnspan=2)

		self.frame_status.grid	(column=0, row=1, columnspan=2, sticky=(N, S, E, W))
		self.txt_status.pack	(fill=BOTH, expand=YES)

		# WINDOW FLAGS

		self.opened_dialog = False

		# PERFORM FIRST UPDATE MANUALLY TO POPULATE UI

		self.do_update()

		# SPEECH RECOGNITION

		if self.settings["voic"] == True:
			print("Using speech")
			self.run_speech()

	def goto_authentication(self):
		if not self.opened_dialog:
			self.opened_dialog = True
			# Instantiate window, bind focus change to func, set focus
			self.window = Authentication.Authentication(Toplevel(self.parent), self)
			self.window.parent.bind("<FocusOut>", self.focus_out)
			self.window.parent.focus_set()
			# Open window and make main window wait
			self.parent.wait_window(self.window.parent)
			self.opened_dialog = False

		else:
			self.window.parent.focus_set()

	def goto_auto_message(self):
		if not self.opened_dialog:
			self.opened_dialog = True
			# Instantiate window, bind focus change to func, set focus
			self.window = AutoMessage.AutoMessage(Toplevel(self.parent), self)
			self.window.parent.bind("<FocusOut>", self.focus_out)
			self.window.parent.focus_set()
			# Open window and make main window wait
			self.parent.wait_window(self.window.parent)
			self.opened_dialog = False

	def goto_commands(self):
		if not self.opened_dialog:
			self.opened_dialog = True
			# Instantiate window, bind focus change to func, set focus
			self.window = Commands.Commands(Toplevel(self.parent), self)
			self.window.parent.bind("<FocusOut>", self.focus_out)
			self.window.parent.focus_set()
			# Open window and make main window wait
			self.parent.wait_window(self.window.parent)
			self.opened_dialog = False

	def focus_out(self, event):
		pass
		#if self.opened_dialog:
			#self.window.goto_main()

	def get_update(self):

		result = {}
		channel = twitch.channels.by_name(self.settings["chan"])
		follows = twitch.follows.by_channel(self.settings["chan"], limit = 5)
		stream = twitch.streams.by_channel(self.settings["chan"])

		result['followers']		= channel["followers"]
		result['views']			= channel["views"]
		result['game']			= {}
		result['title']			= channel["status"]
		result['last5fol']		= []
		result['status']		= 0 if stream['stream'] == None else 1

		for i in follows["follows"]:
			result['last5fol'].append(i['user']['name'])

		streams = twitch.search.streams(channel["game"])
		games = twitch.search.games(channel["game"])

		result['game']['name']	= channel["game"]
		result['game']['total']	= streams["_total"]
		result['game']['popu']	= games["games"][0]["popularity"] if len(games["games"]) > 0 else 0

		return result

	def do_update(self):
		update = self.get_update()
		# self.chat.print_line("SYS", str(update)) # debug

		if self.channel_data == {}:
			self.channel_data = update

		else:
			if update["followers"] - self.channel_data["followers"] > 0:
				self.chat.message_send("Gained %d follower%s! :D"%(followers - self.channel_data["followers"], "s" if update["followers"] - self.channel_data["followers"] > 1 else ""))
				self.channel_data["followers"] = update["followers"]

			elif self.channel_data["followers"] - update["followers"] > 0:
				self.chat.message_send("Lost %d follower%s! :("%(self.channel_data["followers"] - update["followers"], "s" if self.channel_data["followers"] - update["followers"] > 1 else ""))
				self.channel_data["followers"] = update["followers"]

		self.lab_followers_s.set("Followers: %d"%(self.channel_data["followers"]))

		self.lst_last5fol.delete(0, 4)
		for i in update["last5fol"]:
			self.lst_last5fol.insert(END, i)
		self.lst_last5fol['state'] = DISABLED

		self.lab_views_s.set("Views:" + str(update['views']))
		self.lab_status_s.set("Status: Online" if update['status'] == 1 else "Status: Offline")
		self.lab_game_s.set("Game: " + update['game']['name'])
		self.lab_streams_s.set("Streams of game: " + str(update['game']['total']))
		self.lab_popularity_s.set("Game Popularity: " + str(update['game']['popu']))

	def do_automessage(self):
		self.auto_time_l.acquire()

		for i, a in enumerate(self.auto_time):
			if a[0] - time.clock() < 0.0:
				self.auto_time[i][0] = time.clock() + (a[1]['int'] * 60)
				self.chat.message_send(a[1]['msg'])

		self.auto_time_l.release()

	def reload_automessage_timings(self):

		self.auto_time_l.acquire()

		self.auto_time.clear()
		for i in self.settings['auto']:
			self.auto_time.append([time.clock() + (i['int'] * 60), i])

		self.auto_time_l.release()

	def on_voice_command(self, command):
		self.txt_status_s.set(command)

		if command.startswith("connect"):
			self.core_connect()

		elif command.startswith("disconnect"):
			self.core_connect()

		elif command.startswith("chat "):
			self.chat.message_send(command[5:])

	def run_update(self):
		"""Updater function that runs on a thread to grab Twitch data via API"""

		while self.update_forever:

			self.do_update()
			self.do_automessage()
			time.sleep(self.settings["rate"])

		print("updater thread finished")
		return 0

	def run_speech(self):
		"""Speech recognition thread"""
		print("Started speech thread")

		r = sr.Recognizer()
		m = sr.Microphone()
		print(m.device_index)

		self.txt_status_s.set("Waiting for voice input...")

		with m as source:
			r.adjust_for_ambient_noise(source)

		r.listen_in_background(m, self.speech_recognised)


	def speech_recognised(self, recogniser, audio):
		self.txt_status_s.set("Analysing input...")
		try:
			recognised = recogniser.recognize_google(audio)
			self.on_voice_command(recognised)

		except sr.UnknownValueError:
			self.txt_status_s.set("Could not understand audio")

		except sr.RequestError as e:
			self.txt_status_s.set("Speech recognition error!")
			print(e)

	def core_connect(self):

		if self.update_forever:
			self.btn_connect['text'] = "Connect"
			self.btn_goto_auth.configure(state = NORMAL)
			self.btn_chat_send.configure(state = DISABLED)
			self.chat.disconnect()
			self.update_forever = False

		else:
			self.btn_connect['text'] = "Disconnect"
			self.btn_goto_auth.configure(state = DISABLED)
			self.btn_chat_send.configure(state = NORMAL)
			self.chat.do_connect(self.settings["chan"], self.settings["nick"], self.settings["auth"], self.settings['cmds'])
			self.fakechat = threading.Thread(target=self.fake_chat)
			self.fakechat.start()
			self.update_forever = True
			self.updater = threading.Thread(target=self.run_update)
			self.updater.start()

	def fake_chat(self):
		time.sleep(2)
		self.chat.print_line("SYS", "Connected!")

		time.sleep(4)
		self.chat.print_line("Steve", "Hello everyone!")

		time.sleep(6)
		self.chat.print_line("Alice", "great stream!")

		time.sleep(7)
		self.chat.print_line("Bob", "whats your twitter?")

		time.sleep(5)
		self.chat.print_line("Alan", "type the !twitter command")

		time.sleep(6)
		self.chat.on_message("#southclaw", "Bob", "!twitter")

		time.sleep(5)
		self.chat.print_line("Bob", "thanks!")

		time.sleep(7)
		self.chat.print_line("Alice", "are you streaming tomorrow?")

	def load_settings(self):
		with io.open("settings.json", "r") as f:
			self.settings = json.load(f)
			self.reload_automessage_timings()

	def save_settings(self):
		with io.open("settings.json", "w") as f:
			json.dump(self.settings, f, indent = "\t", sort_keys = True)


def main(): 
	logging.basicConfig(filename='log.txt',level=logging.DEBUG)

	app = Main(Tk())
	app.parent.title("Lightweight Twitch Utility")
	app.parent.resizable(width=FALSE, height=FALSE)
	app.parent.mainloop()

	print("disconnecting from chat")
	app.chat.disconnect()

	print("closing updater thread")
	app.update_forever = False

if __name__ == '__main__':
	main()
