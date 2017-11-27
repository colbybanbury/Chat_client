import socket


ip = "0.0.0.0" #accept any IPv4 adress
serverPort = 8080	#port
clientPort = 8081

BUFFER_SIZE = 2048


sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	#initialize socket
sckt.bind((ip, serverPort))

sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	#initialize sender 

users = {"colby" : "localhost"} #username : IP

messages = {"colby": ["1721`thomas`colby``hello", "2484`thomas`colby``hello number 2" ]}

def send(address, message, checksum, trys):
	if trys >25:
		return 0
	sender.sendto(message, (address, clientPort)) #send to server
	timer = 0
	responseMessage = None
	while timer < 100000:
		responseMessage, otherAddress = sckt.recvfrom(BUFFER_SIZE)	#wait for ack
		timer += 1
		if not (responseMessage is None):
			if responseMessage == checksum:
				return 1
			else:
				return send(address, message, checksum, trys+1) #resend
	return send(address, message, checksum, trys+1) #resend


def processMessage(message):
	#message formats
	#registering: checksum,username
	#already registered: checksum`senderUsername`reciever1Username`reciever2Username`Message
	return message.split("`")

def checkChecksum(processedMessage):
#checks to see if the message came through correctly
#in this implementation the checksum is equal to the sum of the rest of the message
	checksum = processedMessage[0]
	messageSum = 0
	for i in range(len(processedMessage)-1):
		for k in range(len(processedMessage[i+1])):
			messageSum += ord(processedMessage[i+1][k])
	if(messageSum == int(checksum)):
		print("checksum passed")
		return True
	else:
		return False

def relayMessages(processedMessage):
	userMessages = messages[processedMessage[1]]
	if int(processedMessage[2]) < len(userMessages): #if there are new messages
		for i in range(int(processedMessage[2]),len(userMessages)):
			print "sending message: " + str(i)
			print userMessages
			send(users[processedMessage[1]], userMessages[i], processMessage(userMessages[i])[0], 0)
	send(users[processedMessage[1]], "422`done", "422", 0)
	print "done sent"
	return

def ack(checksum, address):
	#send the checksum back to the sender
	sender.sendto(checksum, (address, clientPort))
	return

def saveMessage(processedMessage, message):
	#Currently assumes that the recipients have already registered
	#relay message to recipients
	print "saving message"
	#saves the message to be requested later by the recipient
	if(processedMessage[3] != ""): #two recipients
		if not processedMessage[3] in messages:
			messages[processedMessage[3]] = [message]
		else:
			messages[processedMessage[3]].append(message)
	if not processedMessage[1] in messages:	#save sent messages in the conversation too
		messages[processedMessage[1]] = [message]
	else:
		messages[processedMessage[1]].append(message)
	if not processedMessage[2] in messages: #if this person has not yet been added to messages add them
		messages[processedMessage[2]] = [message]
	else:
		messages[processedMessage[2]].append(message)
	return

def fileTransfer(processedMessage, message):
	send(users[processedMessage[2]], message, processedMessage[0], 0)
	responseMessage = None
	print "waiting for file transfer response..."
	while responseMessage is None: #keep checking until there is a response
		responseMessage, address = sckt.recvfrom(BUFFER_SIZE)
	processedMessage = processMessage(responseMessage)
	if(checkChecksum(processedMessage)):
		ack(processedMessage[0], address[0])
		send(users[processedMessage[1]], responseMessage, processedMessage[0], 0)
		if processedMessage[1] == "1":
			data = None
			while data != "0`0":
				data = None
				while data is None:
					data, address = sckt.recvfrom(BUFFER_SIZE)
				processedData = processMessage(data)
				if(checkChecksum(processedData)):
					ack(processedMessage[0], address[0])
					send(processedMessage[2], data, processedData[0], 0)
	return

def serverRun():
	message = None
	print "waiting for message..."
	while message is None: #keep checking until there is a response
		message, address = sckt.recvfrom(BUFFER_SIZE)
	processedMessage = processMessage(message)
	print "message recieved"
	if(checkChecksum(processedMessage)):
		ack(processedMessage[0], address[0])
		if(len(processedMessage) == 2):
			users[processedMessage[1]] = address[0] #register a new user
			print "registered"
			print users
		elif(len(processedMessage) == 3):
			relayMessages(processedMessage)
		elif(len(processedMessage)==4):
			fileTransfer(processedMessage, message)
		else:
			#send the message out to the users
			saveMessage(processedMessage, message)
	else:
		print "message corrupted" #no ack sent back
	return serverRun()

def main():
	serverRun()

if __name__ == '__main__':
	main()