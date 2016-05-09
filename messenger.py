from flask import Flask, render_template, request, redirect, session
import os
import json
import requests
import thread

from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# MARKER - TELEGRAM
import globalStructs
import tgBOT


app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ytmtzbmi:hYQolEPk4i-pFB8XExOlSqxIIHi_ef-7@jumbo.db.elephantsql.com:5432/ytmtzbmi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class token_reg(db.Model):

	token = db.Column(db.Integer, primary_key=True, autoincrement=True)
	usernames = db.Column(db.String)

	# def __init__(self, username):
	# 	self.usernames = username

	def __repr__(self):
		return '<User %r>' % self.usernames

admin = Admin(app, name='token_panel', template_mode='bootstrap3')
admin.add_view(ModelView(token_reg, db.session))
# Add administrative views here

#globals
REPLY_STR = "Hola! Your food for token:%d is ready! Have a nice meal and Good Luck for exams!!"

#user object for storing registeration requests

@app.route('/')
def home():
	return "Hello World"

#Webhook Url which facebook calls whenever new message arrives
@app.route('/webhook',methods=['GET','POST'])
def verify_Webhook():
	#Handle new message
	if request.method == 'POST':
		content = request.get_json()
		try:
			messaging_events = content['entry'][0]['messaging']
		except:
			print "Error in get messaging events"
		# print messaging_events
		for event in messaging_events:
			if 'message' in event and 'text' in event['message']:
				userid = event['sender']['id']
				user_id_curr = str(userid)
				
				if event['message']['text']:
					tok_str = event['message']['text'].split(',')
					for tok in tok_str:
						if tok.isdigit():
							i = int(tok)
							if i > 0 and i <= globalStructs.TOTAL_TOKEN:
								# adding 
								newUser = next((usr for usr in globalStructs.userList[i] if usr.userId == userid), None)
								if newUser == None:
									newUser = globalStructs.User(userid, globalStructs.method[0])
									globalStructs.userList[i].append(newUser) 
									# notify user of successful reg status
									reply("token no. %d registered" % (i),userid)
								else:
									# notify user of already successful reg status
									reply("token %d already registered" % (i) ,userid)	

								# token_row = token_reg.query.get(i) #return an object of the token_reg table (row)
								# if token_row.usernames:
								# 	users = token_row.usernames.split(',')    
								# 	if user_id_curr in users:
								# 		# notify user of successful reg status
								# 		reply("token %d already registered" % (i) ,userid)									
								# 	else:
								# 		token_row.usernames = token_row.usernames + "," + user_id_curr
								#		# db.session.add(token_row)
								# 		db.session.commit()
								# 		# notify user of successful reg status
								# 		reply("token no. %d registered" % (i) ,userid)
								# else: # for first time the token is used
								# 	token_row.usernames = user_id_curr
								# 	# db.session.add(token_row)
								# 	db.session.commit()
								# 	# notify user of successful reg status
								# 	reply("token no. %d registered" % (i),userid)

							else:
								reply("Error : invalid range; Usage : token numbers must be in range 1-150",userid)
						else:
							reply("Error : invalid type; Usage : tokens must be only comma separated values in range 100",userid)

		return "Done!"

	#First time URL verification by facebook 
	elif request.method == 'GET': 
		if(request.args.get('hub.verify_token') == "smartcampus"):
			return request.args.get('hub.challenge')
		else:
			return "Error"


#Function that sends bot reply back to messenger
def reply(userid,msg):
	messageData = {"text":msg}
	token = {"access_token":"CAADMARK7AawBAFZCiwNRiReYd94VDe1N1NrNdmGETGvd2fTZBmBbPjv6cLZBCo15ZA4FKuxdU2ydh6Ug3vqy9ig0rvQQaJc8BwJjZC0rlZA5lMCAxpmmscyNkclDQZAWulOXOqjfkGoo4XEGOCHNwjOLMqwxJ91ZCtr0OA61ZCAzv7m8J7t5GSfZCPZBjt75bNNyrruawv0KaSnrAZDZD"}
	content = {"recipient":{'id':userid}, "message":messageData}
	print content
	r =  requests.post('https://graph.facebook.com/v2.6/me/messages',params=token,json=content)
	print r.status_code

#flask web app for relaying token status
@app.route('/ready',methods=['GET','POST'])
def dataFromPi():
	if request.method == 'POST':
		i = request.form['token']
		i = int(i)
		print "post received"
		print globalStructs.userList
		# token_row = token_reg.query.get(i) #return an object of the token_reg table (row)
		# if token_row.usernames:
		# 	users = token_row.usernames.split(',')
		# 	for user in users:
		# 		s = 'Your token no. {} is ready'.format(i)
		# 		reply(s,int(user))

		# 	token_row.usernames = None
		# 	db.session.commit()
		print "token received" + str(i)
		while (globalStructs.userList[i]):
			usr = next((u for u  in globalStructs.userList[i]),None)
			if usr:
				if usr.method == globalStructs.method[0]:
					reply(usr.userId, REPLY_STR % (i))
					globalStructs.userList[i].remove(usr)
				elif usr.method == globalStructs.method[1]:
					print "sending telegram msg"
					tgBOT.reply(usr.userId, REPLY_STR % (i))
					globalStructs.userList[i].remove(usr)
			else:
				print "Done replying to all users!!"


	return "Got it!!"


try:
	thread.start_new_thread(tgBOT.main,())
except:
	print "Error: unable to start thread"

port = int(os.getenv('VCAP_APP_PORT', 8080))
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port, debug=False)
