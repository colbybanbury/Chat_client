import socket

ip = "0.0.0.0" #accept any IPv4 adress
port = 5005	#port
BUFFER_SIZE = 2048
CHECKSUM_SIZE = 16

sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	#initialize socket
sckt.bind((ip, port))

users = {} #username : IP

def processMessage(message):
	#message formats
	#registering: checksum,username
	#already registered: checksum,senderUsername,reciever1Username,reciever2Username,Message
	return message.split("`")

def checksum(processedMessage):
#checks to see if the message came through correctly
#in this implementation the checksum is equal to the sum of the rest of the message
	checksum = processedMessage[0]
	messageSum = 0
	for i in range(len(processedMessage)-1):
		for k in range(len(processedMessage[i+1])):
			messageSum = ord(processedMessage[i+1][k])
	if(messageSum == int(checksum)):
		return True
	else:
		return False

def ack(checksum, address):
	#send the checksum back to the sender
	sckt.sendto(checksum, (address, port))
	return

def serverRun():
	message = None
	while message is None: #keep checking until there is a response
		message, address = sckt.recvfrom(BUFFER_SIZE)
	processedMessage = processMessage(message)
	if(checksum(processedMessage)):
		ack(processedMessage[0], address)
		if(len(processedMessage) == 2):
			username[processedMessage[1]] = address #register a new user
		else:
			print "nothing"#send the message out to the users
	else:
		#send message to recipients
		print "nothing"
	return

def main():
	serverRun()

if __name__ == '__main__':
	main()