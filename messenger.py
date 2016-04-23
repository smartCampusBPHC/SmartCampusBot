from flask import Flask, render_template, request, redirect, session
import os
import json
import requests

from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ytmtzbmi:hYQolEPk4i-pFB8XExOlSqxIIHi_ef-7@jumbo.db.elephantsql.com:5432/ytmtzbmi'
db = SQLAlchemy(app)

class token_reg(db.Model):
	token = db.Column(db.Integer, primary_key=True, autoincrement=True)
	usernames = db.Column(db.String)

	# def __init__(self, username):
	# 	self.usernames = username

	def __repr__(self):
		return '<User %r>' % self.username


admin = Admin(app, name='token_panel', template_mode='bootstrap3')
admin.add_view(ModelView(token_reg, db.session))
# Add administrative views here

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
		print messaging_events
		for event in messaging_events:
			if 'message' in event and 'text' in event['message']:
				user_id_curr = str(event['sender']['id'])
				session['recipient'] = event['sender']['id']
				
				if event['message']['text']:
					tok_str = event['message']['text'].split(',')
					for tok in tok_str:
						if tok.isdigit():
							i = int(tok)
							token_row = token_reg.query.get(i) #return an object of the token_reg table (row)
							users = token_row.usernames.split(',')    
							if user_id_curr in users:
								pass
							else:
								token_row.usernames = token_row.usernames + "," + user_id_curr
								db.session.add(token_row)
								db.session.commit()
				
			reply("token registered")

		return "Done!"

	#First time URL verification by facebook 
	elif request.method == 'GET': 
		if(request.args.get('hub.verify_token') == "smartcampus"):
			return request.args.get('hub.challenge')
		else:
			return "Error"


#Function that sends bot reply back to messenger
def reply(msg):
	messageData = {"text":msg}
	token = {"access_token":"CAADMARK7AawBAFZCiwNRiReYd94VDe1N1NrNdmGETGvd2fTZBmBbPjv6cLZBCo15ZA4FKuxdU2ydh6Ug3vqy9ig0rvQQaJc8BwJjZC0rlZA5lMCAxpmmscyNkclDQZAWulOXOqjfkGoo4XEGOCHNwjOLMqwxJ91ZCtr0OA61ZCAzv7m8J7t5GSfZCPZBjt75bNNyrruawv0KaSnrAZDZD"}
	content = {"recipient":{'id':session['recipient']}, "message":messageData}
	print content
	r =  requests.post('https://graph.facebook.com/v2.6/me/messages',params=token,json=content)
	print r.status_code


port = int(os.getenv('VCAP_APP_PORT', 8080))
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port, debug=True)
