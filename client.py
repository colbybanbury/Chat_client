import socket

ip = "73.188.177.154" #IP address of the server
port = 5005	#port
BUFFER_SIZE = 2048

sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	#initialize socket
sckt.bind((ip, port))


def send(message, checksum):
	sckt.sendto(message, (ip, port)) #send to server
	timer = 0
	responseMessage = None
	while timer < 10000:
		responseMessage, address = sckt.recvfrom(BUFFER_SIZE)	#wait for ack
		timer += 1
		if not (responseMessage is None):
			if responseMessage == checksum:
				return 1
			else:
				return send(message) #resend
	return send(message) #resend

def register(username):
	checksum = checksum(username) #should be a string
	message = checksum + "`" + username
	return send(message, checksum)

def sendMessage(username, recipient1, recipient2, message):
	message = username + '`' + recipient1 + '`' + recipient2 + '`' + message
	checksum = checksum(message)
	message = checksum + '`' + message
	return send(message, checksum)

def main():
	userInput = input("Welcome. Press 's' to sign in or 'r' to register an account: ")
	while  (userInput.lower() != "r") and (userInput.lower() != "s"):
		print("Please only input one character")
		userInput = input("Press 's' to sign in or 'r' to register an account: ")
	if userInput.lower() == "r":
		username = input("Register, please enter your username: ")
		if not register(username.lower()):
			print "registration failed"
	elif userInput.lower() == "s":
		username = input("Sign in, please enter your username: ")
	print "--Message Center--"
	while (userInput.lower() != "1") and (userInput.lower() != "2"):
		userInput = input("Enter 1 or 2 recipients: ")
	recipient1 = None
	recipient2 = None
	if userInput == "1":
		recipient1 = input("enter the recipient")
	elif userInput == "2":
		recipient1 = input("enter the first recipient: ")
		recipient2 = input("enter the second recipient: ")
	message = input("Enter your message: ")
	sendMessage(username.lower(),recipient1.lower(), recipient2.lower(), message)

if __name__ == '__main__':
	main()