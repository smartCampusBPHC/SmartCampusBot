#!/usr/bin/env python

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import urllib
import json as m_json
import globalStructs
# import messenger

# Enable logging
logging.basicConfig(
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		level=logging.INFO)

logger = logging.getLogger(__name__)
job_queue = None
updater = None

TOKEN = "212506256:AAGnzNLnO7ZVuIik61OXlAx57WxLMbQ8h10"

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
	bot.sendMessage(update.message.chat_id, text='Hi! Use /token <token number> to '
												 'register for a token')
def echo(bot, update):
  bot.sendMessage(update.message.chat_id, text=update.message.text)

def token(bot, update, args):
	chat_id = update.message.chat_id
	try:
		print args[0]
		tok = int(args[0])
		if tok > 0 and tok <= 100:
			newUser = next((usr for usr in globalStructs.userList[tok] if usr.userId == chat_id), None)
			# print "new User = " + str(newUser.userId)
			if newUser == None:
				# print "inside if"
				newUser = globalStructs.User(chat_id, globalStructs.method[1])
				globalStructs.userList[tok].append(newUser)
				bot.sendMessage(chat_id, text='Token '+ str(tok) +' successfully registered !')
			else:
				bot.sendMessage(chat_id, text='Token '+ str(tok) +' already registered !')
		else:
			bot.sendMessage(chat_id, text='Please enter valid token number!')
			return
	
	except IndexError:
		bot.sendMessage(chat_id, text='Usage: /token <token number>')
	except ValueError:
		bot.sendMessage(chat_id, text='Please enter valid token number!')

def reply(chat_id,msg):
	updater.bot.sendMessage(chat_id,text=msg)



def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
	print "Thread started"	
	global job_queue
	global updater
	updater = Updater(TOKEN)
	# job_queue = updater.job_queue

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# on different commands - answer in Telegram
	dp.addHandler(CommandHandler("start", start))
	dp.addHandler(CommandHandler("help", start))
	dp.addHandler(CommandHandler("token", token, pass_args=True))
	# on noncommand i.e message - echo the message on Telegram
 	dp.addHandler(MessageHandler([Filters.text], echo))	

	# log all errors
	dp.addErrorHandler(error)

	# Start the Bot
	updater.start_polling()

	# Block until the you presses Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	# updater.idle()

if __name__ == '__main__':
	main()






