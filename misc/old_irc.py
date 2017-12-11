import socket, string, time, datetime, threading
from urllib.request import urlopen
from threading import Thread

# Set all the variables necessary to connect to Twitch IRC
HOST = "irc.twitch.tv"
NICK = "drovakbot"
PORT = 6667
PASS = "oauth:r5hcznbfc1rw7k2zwkwimvdruu72z2"
CHAN = "#drovak"
readbuffer = ""
MODT = False
RATE = (20/30)

# Connecting to Twitch IRC by passing credentials and joining a certain channel
s = socket.socket()
s.connect((HOST, PORT))
s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))


# Method for sending a message
def Send_message(message):
	sendMessage = ("PRIVMSG #drovak :" + message + "\r\n")
	s.send(sendMessage.encode("utf-8"))
	time.sleep(2)
	
while True:
	readbuffer = s.recv(1024).decode("utf-8")
	temp = str.split(readbuffer, "\n")
	readbuffer = temp.pop()
	
	#temp.pop()
	for line in temp:
		# Checks whether the message is PING because its a method of Twitch to check if you're afk
		if (line[0] == "PING"):
			s.send("PONG %s\r\n" % line[1].encode("utf-8"))
		else:
			# Splits the given string so we can work with it better
			parts = str.split(line, ":")
 
			if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
				try:
					# Sets the message variable to the actual message sent
					message = parts[2][:len(parts[2]) - 1]
				except:
					message = ""
				# Sets the username variable to the actual username
				usernamesplit = str.split(parts[1], "!")
				username = usernamesplit[0]
			   
			
				if MODT:
					print (username + ": " + message)
				   
					if message == "Hey" or message == "hello":
						Send_message("Welcome to my stream, " + username)
					
					if message == "!time":
						currentTime = time.strftime("%H:%M", time.gmtime())
						message = "The current time in England is " + currentTime
						Send_message(message)

					if message == "!uptime":
						endTimer = time.time()
						uptimeSeconds = endTimer - startTimer
						uptimeMinutes = str(int(round(uptimeSeconds/60,0)))
						message = "The stream has been online for: "+uptimeMinutes+" minutes."
						Send_message(message)
					

					if "!qrcode " in message:
						try:
							head, sep, url = message.partition('!qrcode ')
							qrcodeApiAddress = ("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=http://www.twitch.tv/"+url)
							Send_message(qrcodeApiAddress)
						except:
							pass

					if "!w " in message:
						try:
							head, sep, location = message.partition('!w ')
							address = ("http://api.openweathermap.org/data/2.5/weather?q="+location+"&appid=a9fbd826502e2267401d1c24aeb465e7")
							weather = urlopen(address)
							response = (weather.read().decode('utf-8'))
							body = response[1:2000]
							head, sep, tail = body.partition('"description":"')
							sky, sep, tail = tail.partition('","icon"')
							
							head, sep, country = body.partition('"country":"')
							country, sep, tail = country.partition('","')

							head, sep, temperature = body.partition('"temp":')
							temperature, sep, tail = temperature.partition(',"pressure"')
							temperature = float(temperature) - 273.15
							temperature = str(round(temperature,1))

							location, sep, tail = location.partition(',')
							location = location.title()

							message = ("The current weather in " + location + ", "+country+": " +sky+ ", temperature(celcius) = "+temperature)
							Send_message(message)
						except:
							pass

				for l in parts:
					if "End of /NAMES list" in l:
						MODT = True

