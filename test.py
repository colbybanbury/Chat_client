import unittest
import server


class MyTest(unittest.TestCase):

	def test_processMessage(self):
		message = "000000`senderUsername`reciever1Username`reciever2Username`Message"
		howItShouldBe = ["000000", "senderUsername", "reciever1Username", "reciever2Username", "Message"]
		howItIS = server.processMessage(message);
		self.assertEqual(howItShouldBe, howItIS);

	def test_checksum(self):
		#needs implementation
		message = "0"	#case of no message
		self.assertTrue(server.checksum(server.processMessage(message)))
		message = "user1`user2`user3`this is a test" #case of standard message format
		processedMessage = server.processMessage(message)
		messageSum = 0
		for i in range(len(processedMessage)-1):
			for k in range(len(processedMessage[i+1])):
				messageSum = ord(processedMessage[i+1][k])
		self.assertTrue(server.checksum(server.processMessage(str(messageSum) + "`" + message)))



if __name__ == '__main__':
    unittest.main()