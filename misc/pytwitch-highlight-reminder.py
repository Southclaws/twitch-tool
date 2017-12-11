import requests
import io
import json
from datetime import *
from dateutil.parser import parse
from dateutil.relativedelta import *
from dateutil.tz import *


class App():

	def load(self):
		with io.open("settings.cfg", "r") as f:
			self.settings = json.load(f)

	def run(self):
		print("Loading settings")
		self.load()
		print("name:", self.settings['name'])

		print("Running Highlight Reminder")
		streamtime = self.getStreamTime()

		if streamtime == None:
			print("Error: Stream is offline or no data recieved from Twitch endpoint.")
			return 0

		print("Saving current stream time to 'Highlight Reminders.txt'")

		with io.open("Highlight Reminders.txt", "a") as f:
			f.write(streamtime + "\n")

		return 1

	def getStreamTime(self):
		print("Finding stream details")
		now = datetime.now()
		r = requests.get('https://api.twitch.tv/kraken/streams/%s'%(self.settings['name']), verify=False) # verify=False: workaround to prevent py2exe ssl bug

		if r.json()['stream'] == None:
			return None

		print("Calculating stream time")
		streamcreated = parse(r.json()['stream']['created_at'], ignoretz=True)

		streamtime = relativedelta(now, streamcreated)
		streamtimestr = "%02d:%02d:%02d"%(streamtime.hours, streamtime.minutes, streamtime.seconds)

		return streamtimestr


def main():
	app = App()
	app.run()


if __name__ == '__main__':
	main()
