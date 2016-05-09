#userList is a dictioary indexed with tokens for storing user objects
TOTAL_TOKEN = 150

userList = dict()		
for i in range(TOTAL_TOKEN):
	userList[i] = list()

class User():
	userId = -1
	method = "default"
	def __init__(self,userId,method):
		self.userId = userId
		self.method = method

method = {0:"fb_messenger", 
		  1:"telegram"
		}

