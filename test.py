import unittest
import server

#things quickly left the relm of unittests since much of my issues stemmed from the actual udp communication aspect
class MyTest(unittest.TestCase):

	def test_processMessage(self):
		message = "000000`senderUsername`reciever1Username`reciever2Username`Message"
		howItShouldBe = ["000000", "senderUsername", "reciever1Username", "reciever2Username", "Message"]
		howItIS = server.processMessage(message);
		self.assertEqual(howItShouldBe, howItIS);

	def test_checksum(self):
		#needs implementation
		message = "0"	#case of no message
		self.assertTrue(server.checkChecksum(server.processMessage(message)))
		message = "user1`user2`user3`this is a test" #case of standard message format
		processedMessage = server.processMessage(message)
		messageSum = 0
		for i in range(len(processedMessage)):
			for k in range(len(processedMessage[i])):
				messageSum += ord(processedMessage[i][k])
		self.assertTrue(server.checkChecksum(server.processMessage(str(messageSum) + "`" + message)))



if __name__ == '__main__':
    unittest.main()