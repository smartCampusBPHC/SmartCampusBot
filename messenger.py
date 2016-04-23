from flask import Flask, render_template, request, redirect, session
import os
import json
import requests

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

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
                print "....................:" + event['message']['text']
                break
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
    token = {"access_token":"CAAMpeMqMFaQBAD1rWOoDDLiGzn0wAlChwTnJy8fahWfUA8tx8OZAoeupSRlUBwZBkkRbsZC8UZCNiS1SEbhvKiLKdcZCInap0xBk79zJbAYZB0PRXRJTgBPigBiXH5OM7AfM6T91IjrnlBRnGxAJUyuqC3FHAL85wZAN98dZCf5u3UZABZAjSK2eolopQwZBoVw5j50dj1R9QlzKQZDZD"}
    content = {"recipient":{'id':session['recipient']}, "message":messageData}
    print content
    r =  requests.post('https://graph.facebook.com/v2.6/me/messages',params=token,json=content)
    print r.status_code

port = int(os.getenv('VCAP_APP_PORT', 8080))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
