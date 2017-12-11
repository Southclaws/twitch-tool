from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *


class Authentication():

	def __init__(self, parent, app):
		self.parent = parent
		self.app = app
		self.frame = ttk.Frame(self.parent)

		self.lab_chan = ttk.Label(self.frame, text = "Channel:")
		self.lab_nick = ttk.Label(self.frame, text = "IRC Name:")
		self.lab_auth = ttk.Label(self.frame, text = "OAuth:")

		self.ent_chan_s = StringVar()
		self.ent_chan_s.set(app.settings["chan"])
		self.ent_chan = ttk.Entry(self.frame, width = 45, textvariable = self.ent_chan_s)
		self.ent_chan.bind("<FocusOut>", self.on_modify)

		self.ent_nick_s = StringVar()
		self.ent_nick_s.set(app.settings["nick"])
		self.ent_nick = ttk.Entry(self.frame, width = 45, textvariable = self.ent_nick_s)
		self.ent_nick.bind("<FocusOut>", self.on_modify)

		self.ent_auth_s = StringVar()
		self.ent_auth_s.set(app.settings["auth"])
		self.ent_auth = ttk.Entry(self.frame, width = 45, textvariable = self.ent_auth_s)
		self.ent_auth.bind("<FocusOut>", self.on_modify)

		self.btn_quit = ttk.Button(self.frame, text = 'Close', width = 25, command = self.goto_main)

		self.lab_chan.grid(row=0, column=0, sticky=(E, W))
		self.lab_nick.grid(row=1, column=0, sticky=(E, W))
		self.lab_auth.grid(row=2, column=0, sticky=(E, W))
		self.ent_chan.grid(row=0, column=1, sticky=(E, W))
		self.ent_nick.grid(row=1, column=1, sticky=(E, W))
		self.ent_auth.grid(row=2, column=1, sticky=(E, W))
		self.btn_quit.grid(row=3, column=0, columnspan = 2, sticky=(E, W))

		self.frame.pack()

	def on_modify(self, args):
		self.app.settings["chan"] = self.ent_chan_s.get()
		self.app.settings["nick"] = self.ent_nick_s.get()
		self.app.settings["auth"] = self.ent_auth_s.get()
		self.app.save_settings()

	def goto_main(self):
		self.parent.destroy()
