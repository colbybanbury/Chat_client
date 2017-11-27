import socket
import sys

serverIP = "localhost"#"73.188.177.154" #IP address of the server
serverPort = 8080

recieveIP = "0.0.0.0" #accepts any IPv4 adress
recievePort = 8081
BUFFER_SIZE = 2048

sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	#initialize sender 
reciever = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	#initialize reciever
reciever.bind((recieveIP, recievePort))

numMessages = 0
messages = {"":[]}

def processMessage(message):
	#message formats
	#registering: checksum,username
	#already registered: checksum`senderUsername`reciever1Username`reciever2Username`Message
	return message.split("`")

def ack(checksum, address):
	#send the checksum back to the sender
	sender.sendto(checksum, (address, serverPort))
	return

def checkChecksum(processedMessage):
#checks to see if the message came through correctly
#in this implementation the checksum is equal to the sum of the rest of the message
	checksum = processedMessage[0]
	messageSum = 0
	for i in range(len(processedMessage)-1):
		for k in range(len(processedMessage[i+1])):
			messageSum += ord(processedMessage[i+1][k])
	if(messageSum == int(checksum)):
		return True
	else:
		return False

def generateChecksum(message):
	#the checksum is the sum of the ord of all of the characters in the rest of the message
	checksum = 0
	for i in range(len(message)):
		if message[i] != '`':
			checksum += ord(message[i])
	return str(checksum)

def send(message, checksum, trys):
	if trys >25:
		return 0
	sender.sendto(message, (serverIP, serverPort)) #send to server
	timer = 0
	responseMessage = None
	while timer < 10000:
		responseMessage, address = reciever.recvfrom(BUFFER_SIZE)	#wait for ack
		timer += 1
		if not (responseMessage is None):
			if responseMessage == checksum:
				return 1
			else:
				return send(message, checksum, trys+1) #resend
	return send(message, checksum, trys+1) #resend

def register(username):
	checksum = generateChecksum(username) #should be a string
	message = checksum + "`" + username
	return send(message, checksum, 0)

def sendMessage(username, recipient1, recipient2, message):
	message = username + '`' + recipient1 + '`' + recipient2 + '`' + message #sections of the message are seperated by `
	checksum = generateChecksum(message)
	message = checksum + '`' + message
	return send(message, checksum, 0)

def recieveMessages():
	global numMessages
	timer = 0
	lastMessage = ""
	while (timer < 10000):
		timer +=1
		message = None
		while message is None:
			message, address = reciever.recvfrom(BUFFER_SIZE)
		if message == "422`done":
			ack("422", address[0])
			return
		processedMessage = processMessage(message)
		ack(processedMessage[1], address[0])
		if message != lastMessage:
			numMessages += 1
			fromUsers = processedMessage[1] + " + " + processedMessage[2]
			if(processedMessage[3] != ""):
				fromUsers += " + " + processedMessage[3]
			if not fromUsers in messages:
				messages[fromUsers] = [message]
			else:
				messages[fromUsers].append(message)
		lastMessage = message
	return			

def requestMessages(username):
	request = username + "`" + str(numMessages)
	checksum = generateChecksum(request)
	request = checksum + '`' + request
	send(request, checksum, 0)
	recieveMessages()
	return

def sendFile(username, recipient, filename):
	message = username + '`' + recipient + '`' + filename #file transfer initiation message
	checksum = generateChecksum(message)
	message = checksum + '`' + message
	if(send(message, checksum, 0)):
		responseMessage = None
		address = None
		timer = 0
		while (timer < 10000) and responseMessage is None: #wait for response from other client
			responseMessage, address = reciever.recvfrom(BUFFER_SIZE)
			timer += 1
		processedMessage = processMessage(responseMessage)
		if(checkChecksum(processedMessage)):
			ack(processedMessage[0], address[0])
			if(processedMessage[1]=="1"):
				f = open(filename, "rb")
				data = f.read(BUFFER_SIZE)
				while data:#keeps sending over packets until there is nothing left to send 
					checksum = generateChecksum(data)
					message = checksum +'`' + data
					send(message, checksum, 0)
					data = f.read(BUFFER_SIZE)
				send("0`0", "0", 0) #done sending the file
			else:
				print "File transfer was denied"
		else:
			print "file transfer failed"
	return


#the text interface is a little complicated code wise... please don't judge me
def messageCenter(username):
	print "--Message Center--"
	userInput = ""
	while (userInput.lower() != "r") and (userInput.lower() != "w") and (userInput.lower() != "f"):
		userInput = raw_input("Enter r to read, w to write, or f for file transfer: ")
	if(userInput.lower() == 'w'):
		while (userInput != "1") and (userInput != "2"):
			userInput = raw_input("Enter 1 or 2 recipients: ")
		recipient1 = ""
		recipient2 = ""
		if userInput == "1":
			recipient1 = raw_input("enter the recipient: ")
		elif userInput == "2":
			recipient1 = raw_input("enter the first recipient: ")
			recipient2 = raw_input("enter the second recipient: ")
		message = raw_input("Enter your message: ")
		if not sendMessage(username.lower(),recipient1.lower(), recipient2.lower(), message):
			print "message failed to send"
		else:
			print "message sent"
	elif userInput.lower() == "r":
		requestMessages(username.lower())
		print "You have conversations with: "
		for key in messages:
			print key
		userInput = "~"
		while(not userInput in messages):
			userInput = raw_input("select a conversation to view: ")
		print "messages from " + userInput + ": "
		for message in messages[userInput]:
			tempMes = processMessage(message)
			print tempMes[1] +': ' + tempMes[4]
	else:
		userInput = ""
		while (userInput.lower() != "r") and (userInput.lower() != "s"):
			userInput = raw_input("Enter s to send or r to recieve: ")
		if userInput.lower() == "s":
			filename = raw_input("enter the filename: ")
			recipient = raw_input("enter the recipient: ")
			sendFile(username, recipient, filename)
		else:
			message = None
			while message is None:
				print "Waiting for file transfer request... (ctl c to quit)"
				message, address = reciever.recvfrom(BUFFER_SIZE)
			if not message is None:
				processedMessage = processMessage(message)
				if(checkChecksum(processedMessage)):
					ack(processedMessage[0], address[0])
					print "file transfer request from " + processedMessage[1]
					print processedMessage[3]
					while (userInput.lower() != "y") and (userInput.lower() != "n"):
						userInput = raw_input("y to accept file transfer n to deny the request")
					if(userInput == "y"):
						send("1`1", "1", 0) #1 is the confirmation code
						data, addr = reciever.recvfrom(BUFFER_SIZE)
						"Received File:",data.strip()
						destination = raw_input("enter the destination of the file")
						f = open(destination,'wb')
						data, addr = reciever.recvfrom(BUFFER_SIZE)
						try:
						    while(data):
						        f.write(data)
						        reciever.settimeout(2)
						        data,addr = reciever.recvfrom(buf)
						except timeout:
						    print "File Downloaded"
					else:
						send("0`0", "0", 0) #0 is the deny code
						print "file transfer denied"
				else:
					print "file transfer failed"
	quit = raw_input("press q to quit or c to continue: ")
	if quit.lower() != "q":
		messageCenter(username)
	return

def main(): #controls the text user interface
	userInput = raw_input("Press s to sign in or r to register an account/IP pair: ")
	while  (userInput.lower() != "r") and (userInput.lower() != "s"):
		print("Please only input one character")
		userInput = raw_input("Press s to sign in or r to register an account: ")
	if userInput.lower() == "r":
		username = raw_input("Register, please enter your username: ")
		if not register(username.lower()):
			print "registration failed"
	elif userInput.lower() == "s":
		username = raw_input("Sign in, please enter your username: ")
	messageCenter(username)
	return

if __name__ == '__main__':
	main()