from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import os
#import configparser
import logging
import redis
import pymongo

global redis1

def main():
    # Load your token and create an Updater for your Bot
    
    #config = configparser.ConfigParser()
    #config.read('config.ini')
    updater = Updater(token=(os.environ['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher

    global redis1
    redis1 = redis.Redis(host=(os.environ['HOST']), password=(os.environ['PASSWORD']), port=(os.environ['REDISPORT']))

    global mongo1
    mongo1 = pymongo.MongoClient("mongodb+srv://abc:81445308@cluster0.butew.mongodb.net/Project7940?retryWrites=true&w=majority")
    db = mongo1.test
    global calcol
    calcol = db.calories

    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    
    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello", hello_command))
    dispatcher.add_handler(CommandHandler("cal", cal_command))

    # To start the bot:
    updater.start_polling()
    updater.idle()


def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('''Welcome! Here's the command you can use:
    /add <keyword> : Count how many times you input "keyword"
    /hello : Reply a greeting
    /help : Check all commands
    /cal <Name, Gender(M/F), Age, Weight(kg), Height(cm), Labor factor> : 
    Calculate the calories you need to eat one day. Please input the factors after "/cal". Use comma to separate factors.
    Labor factor:
    "1.2": Very Light. Almost sit like Office work. Never do sports.
    "1.375": Light. Always stand or walk like sales person. 1-3 days sports per week.
    "1.55": Medium. Need to move your arms often at work. 3-5 days sports per week.
    "1.725": Medium with high sports habit. 6-7 days sports per week.
    "1.9": High or Professional Athlete.''')


def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try: 
        global redis1
        logging.info(context.args[0])
        msg = context.args[0]   # /add keyword <-- this should store the keyword
        redis1.incr(msg)
        update.message.reply_text('You have said ' + msg +  ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')


def hello_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /hello is issued."""
    logging.info(context.args[0])
    msg = context.args[0]
    update.message.reply_text('Good day, '+ msg +' !')

def cal_command(update: Update, context: CallbackContext) -> None:
    """Send a calories result when the command /cal is issued."""
    logging.info(context.args[0])
    msg = context.args[0]
    #send information to database
    newlist = msg.split(",")
    usercal = {"_id":newlist[0],
               "Name":newlist[0],
               "Gender":newlist[1],
               "Age":newlist[2],
               "Weight":newlist[3],
               "Height":newlist[4],
               "Labor factor":newlist[5]}
    calcol.insert_one(usercal)
    #calculate calories
    x = calcol.find_one({"_id":usercal["Name"]})
    if x["Gender"] == "M" :
        bmr = round(66.0 + (13.7 * float(x["Weight"])) + (5.0 * float(x["Height"])) - (6.8 * float(x["Age"])),0)
    else:
        bmr = round(655.0 + (9.6 * float(x["Weight"])) + (1.8 * float(x["Height"])) - (4.7 * float(x["Age"])),0)
    result = round(bmr * float(x["Labor factor"]),0)
    update.message.reply_text(f"Your BMR is {bmr} kcal. \nYour daily calories needed are: {result} kcal.")


if __name__ == '__main__':
    main()