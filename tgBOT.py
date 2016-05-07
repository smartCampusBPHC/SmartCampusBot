#!/usr/bin/env python

import telegram
from telegram.ext import Updater, CommandHandler
import logging
import urllib
import json as m_json

# Enable logging
logging.basicConfig(
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		level=logging.INFO)

logger = logging.getLogger(__name__)
job_queue = None

TOKEN = "YourTokenHere"

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
	bot.sendMessage(update.message.chat_id, text='Hi! Use /token <token number> to '
												 'register for a token')

def google(bot,update,args): # google <search term>
    '''Returns the link and the description of the first result from a google
    search
    '''
    query=args[0]
    print "going to google %s" % query


def wiki(bot,update,args): # wiki <search term>

    query=args[0]
    print "going to wiki %s" % query

def ready(bot,update,args):
	chat_id = update.message.chat_id
	try:
		# args[0] should contain the time for the timer in seconds
		print args
		due = args[0]
		# print due
		due = int(due)
		# print due
		if due < 1 or due > 100:
			bot.sendMessage(chat_id, text='Please enter valid token number!')
			return
		# print chat_id
		# def alam(bot,token):
		#     """ Inner function to send the alarm message """
		#     bot.sendMessage(chat_id, text='Hola! Your food for token:' + token + ' is ready! Have a nice meal')

		# Add job to queue
		# job_queue.put(alam, due)

		
		bot.sendMessage(chat_id, text='Token "'+ str(due) +'" successfully registered !')

	except IndexError:
		bot.sendMessage(chat_id, text='Usage: /token <token number>')
	except ValueError:
		bot.sendMessage(chat_id, text='Please enter valid token number!')



def token(bot, update, args):
	chat_id = update.message.chat_id
	try:
		# args[0] should contain the time for the timer in seconds
		print args
		due = args[0]
		# print due
		due = int(due)
		# print due
		if due < 1 or due > 100:
			bot.sendMessage(chat_id, text='Please enter valid token number!')
			return
		# def alam(bot,token):
		#     """ Inner function to send the alarm message """
		#     bot.sendMessage(chat_id, text='Hola! Your food for token:' + token + ' is ready! Have a nice meal')

		
		bot.sendMessage(chat_id, text='Token "'+ str(due) +'" successfully registered !')

	except IndexError:
		bot.sendMessage(chat_id, text='Usage: /token <token number>')
	except ValueError:
		bot.sendMessage(chat_id, text='Please enter valid token number!')


def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
	global job_queue

	updater = Updater(TOKEN)
	# job_queue = updater.job_queue

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# on different commands - answer in Telegram
	dp.addHandler(CommandHandler("start", start))
	dp.addHandler(CommandHandler("help", start))
	dp.addHandler(CommandHandler("token", token, pass_args=True))
	dp.addHandler(CommandHandler("google", google, pass_args=True))
	dp.addHandler(CommandHandler("wiki", wiki, pass_args=True))

	# log all errors
	dp.addErrorHandler(error)

	# Start the Bot
	updater.start_polling()

	# Block until the you presses Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()

if __name__ == '__main__':
	main()






