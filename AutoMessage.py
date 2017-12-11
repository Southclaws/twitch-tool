from tkinter import *
from tkinter import ttk
import tkinter


class AutoMessage():

	def __init__(self, parent, app):
		self.parent = parent
		self.app = app
		self.frame = ttk.Frame(self.parent)

		self.current_idx = -1

		# LIST OF MESSAGES FRAME

		self.frame_list = ttk.Frame(self.frame)

		self.lst_messages = Listbox(self.frame_list, height = 10, width = 35)
		self.lst_messages.bind("<<ListboxSelect>>", self.update_config)
		self.btn_add = ttk.Button(self.frame_list, text = "Add", command = self.add_automsg)
		self.btn_del = ttk.Button(self.frame_list, text = "Del", command = self.del_automsg)

		self.reload_list()

		# CONFIG FRAME

		self.frame_config = ttk.Frame(self.frame)

		self.lab_interval = ttk.Label(self.frame_config, text="Interval (minutes)")
		self.spn_interval_v = StringVar()
		self.spn_interval = Spinbox(self.frame_config, from_=1, to=60, textvariable=self.spn_interval_v)
		self.txt_message_s = StringVar()
		self.txt_message = ttk.Entry(self.frame_config, textvariable = self.txt_message_s, width = 35)
		self.btn_save = ttk.Button(self.frame_config, text = "Save", command = self.save_config)

		self.btn_close = ttk.Button(self.frame, text = 'Close', command = self.goto_main)

		# LAYOUT

		self.frame_list.grid	(column=0, row=0, sticky=(N, S, E, W))
		self.lst_messages.grid	(column=0, row=0, columnspan = 2, sticky=(N, S, E, W))
		self.btn_add.grid		(column=0, row=1, sticky=(N, S, E, W))
		self.btn_del.grid		(column=1, row=1, sticky=(N, S, E, W))

		self.frame_config.grid	(column=1, row=0, sticky=(N, S, E, W))
		self.lab_interval.grid	(column=0, row=0, sticky=(N, S, E, W))
		self.spn_interval.grid	(column=1, row=0, sticky=(N, S, E, W))
		self.txt_message.grid	(column=0, row=1, columnspan=2, sticky=(N, S, E, W))
		self.btn_save.grid		(column=0, row=2, columnspan=2, sticky=(N, S, E, W))

		self.btn_close.grid		(column=0, row=1, columnspan=2, sticky=(N, S, E, W))

		self.frame.pack()

	def reload_list(self):
		self.lst_messages.delete(0, len(self.app.settings['auto']))
		for msg in self.app.settings["auto"]:
			self.lst_messages.insert(END, msg['msg'])
		self.app.reload_automessage_timings()

	def add_automsg(self):
		self.app.settings['auto'].append({"int":25, "msg":"New auto-message"})
		self.reload_list()

	def del_automsg(self):
		if self.current_idx == -1:
			pass

		self.app.settings['auto'].pop(self.current_idx)
		self.app.save_settings()
		self.reload_list()

	def update_config(self, event):
		self.current_idx = self.lst_messages.curselection()[0]

		self.spn_interval_v.set(self.app.settings['auto'][self.current_idx]['int'])
		self.txt_message_s.set(self.app.settings['auto'][self.current_idx]['msg'])

	def save_config(self):
		self.app.settings['auto'][self.current_idx]['int'] = int(self.spn_interval_v.get())
		self.app.settings['auto'][self.current_idx]['msg'] = self.txt_message_s.get()
		self.app.save_settings()

		self.reload_list()

	def goto_main(self):
		self.parent.destroy()
