import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.adapters.listadapter import ListAdapter

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.listview import ListItemButton, ListView


Builder.load_string("""
<Main>:
	BoxLayout:
		padding: 10

		BoxLayout:
			padding: 10

			Button:
				size_hint_y: 0.1
				text: 'Authentication'
				on_press: root.goto_authentication()

			Button:
				size_hint_y: 0.1
				text: 'Auto-Messages'
				on_press: root.goto_auto_message()

			Button:
				size_hint_y: 0.1
				text: 'Commands'
				on_press: root.goto_commands()

		BoxLayout:
			padding: 10
			orientation: 'vertical'

			TextInput:
				id: w_input
				font_name: 'cour'
				size_hint_y: 0.1
				multiline: False
				on_text_validate: root.input_enter()

			TextInput:
				id: w_log
				font_name: 'cour'
				cursor_color: [0, 0, 0, 0]

<Authentication>:
	BoxLayout:
		padding: 10

		Button:
			size_hint_y: 0.1
			text: 'Back'
			on_press: root.goto_main()

<AutoMessage>:
	BoxLayout:
		padding: 10

		Button:
			size_hint_y: 0.1
			text: 'Back'
			on_press: root.goto_main()

<Commands>:
	BoxLayout:
		padding: 10

		BoxLayout:
			padding: 10
			TextInput:
				size_hint_y: 0.5
				text: 'command'

			TextInput:
				size_hint_y: 0.5
				text: 'result'

		BoxLayout:
			ListView:
				id: command_list

	Button:
		size_hint_y: 0.1
		text: 'Back'
		on_press: root.goto_main()
""")


class Main(Screen):

	def input_enter(self):
		msg = self.ids['w_input'].text

		if msg:
			self.ids['w_log'].text = str(msg) + '\n' + self.ids['w_log'].text
			self.ids['w_input'].text = ""
			Clock.schedule_once(self._refocus_text_input, 0)
 
	def _refocus_text_input(self, args):
		self.ids['w_input'].focus = True

	def goto_authentication(self):
		sm.current = 'Authentication'

	def goto_auto_message(self):
		sm.current = 'AutoMessage'

	def goto_commands(self):
		sm.current = 'Commands'


class Authentication(Screen):

	def goto_main(self):
		sm.current = 'Main'


class AutoMessage(Screen):

	def goto_main(self):
		sm.current = 'Main'


class Commands(Screen):

	class Command():

		def __init__(self, command, result):
			self.command = command
			self.result = result


	def on_pre_enter(self):
		#temp
		data = [self.Command("help", "this is the help command"), self.Command("faq", "this is the faq command"), self.Command("donate", "this is the donate command")]
		#end temp

		args_converter = lambda row_index, obj: {'text': obj.command, 'size_hint_y': None, 'height': 25}

		list_adapter = ListAdapter(data=data,
			args_converter=args_converter,
			cls=ListItemButton,
			selection_mode='single',
			allow_empty_selection=False)

		self.ids['command_list'].adapter = list_adapter


	def goto_main(self):
		sm.current = 'Main'


#
#	Setup
#


sm = ScreenManager()
sm.add_widget(Main(name = 'Main'))
sm.add_widget(Authentication(name = 'Authentication'))
sm.add_widget(AutoMessage(name = 'AutoMessage'))
sm.add_widget(Commands(name = 'Commands'))
sm.current = 'Main'


def settings_load():

	print()


def settings_save():

	print()


class ToolApp(App):

	def build(self):
		settings_load()
		return sm


if __name__ == '__main__':
	ToolApp().run()
