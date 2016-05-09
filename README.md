# SmartCampusBot_BPHC

Libraris used : 
 - [flask] (http://flask.pocoo.org/docs/0.10/quickstart/)
 - [python-telegram-bot] (https://github.com/python-telegram-bot/python-telegram-bot)

## Desciption (Notification proxy) : ##
This a python implementation for a telegram bot backend connecting to [SmartCampusBot] (https://telegram.me/SmartCampusBot>) in conjucture with a [flask] (http://flask.pocoo.org/docs/0.10/quickstart/) web app. for Bits Pilani Hyderabad Campus. It provides food status notification for Mess1 - All night Canteen(anc). (Running from 10pm to 12pm). This works in collaboration with the [all_night_canteen_oder_notification] (https://github.com/smartCampusBPHC/all_night_canteen_order_notification>). Currently its running on [IBM Bluemix] (mess1-bot.mybluemix.net)

## Working: ##
 - All the users can register their token at the [SmartCampusBot] (https://telegram.me/SmartCampusBot) by sending a `/token xx`request. e.g. "/token 45"
 - The Raspberry Pi setup in the anc (see the [all_night_canteen_oder_notification] (https://github.com/smartCampusBPHC/all_night_canteen_order_notification>) project) in addition to displaying tokens on the LCD screen, sends out an http post request this flask app. 
 - It notifies all the registered users with a telegram message/fb messenger msg.
