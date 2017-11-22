import socket

ip = "0.0.0.0"#"73.188.177.154" #IP address of the server
port = 5005	#port
BUFFER_SIZE = 2048

sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	#initialize socket
sckt.bind((ip, port))

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

def main():
	userInput = raw_input("Press s to sign in or r to register an account: ")
	while  (userInput.lower() != "r") and (userInput.lower() != "s"):
		print("Please only input one character")
		userInput = raw_input("Press s to sign in or r to register an account: ")
	if userInput.lower() == "r":
		username = raw_input("Register, please enter your username: ")
		if not register(username.lower()):
			print "registration failed"
	elif userInput.lower() == "s":
		username = raw_input("Sign in, please enter your username: ")
	print "--Message Center--"
	while (userInput.lower() != "1") and (userInput.lower() != "2"):
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
	quit = raw_input("press q to quit or c to continue: ")
	if quit.lower() != "q":
		main()
	return

if __name__ == '__main__':
	main()