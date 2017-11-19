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
	#registering: checksum,username,IP
	#already registered: checksum,senderUsername,reciever1Username,reciever2Username,Message
	processedMessage = []
	k = 0
	for i in range(len(message)):
		if message[i] = ',':
			i++
			k++
		processedMessage[k] += char(message[i])
	return processedMessage


def serverRun():
	while message is None: #keep checking until there is a response
		message, address = sckt.recvfrom(BUFFER_SIZE)
	processMessage(message)

def main():
	serverRun()

if __name__ == '__main__':
	main()