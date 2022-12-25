import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import random

# Riddle database
riddles = [
    {'riddle': 'I am not alive, but I grow; I don't have lungs, but I need air; I don't have a mouth, but water kills me. What am I?', 'answer': 'fire'},
    {'riddle': 'I am light as a feather, yet even the world's strongest man couldn't hold me for much longer than a minute. What am I?', 'answer': 'breath'},
    {'riddle': 'I am not alive, but I grow; I don't have lungs, but I need air; I don't have a mouth, but water kills me. What am I?', 'answer': 'fire'},
    {'riddle': 'I go in hard, come out soft, and am never the same. What amm I?', 'answer': 'chewing gum'},
]

# Function to get a random riddle from the database
def get_random_riddle():
    riddle = random.choice(riddles)
    return riddle['riddle'], riddle['answer']

# Function to handle the /start command
def start(update, context):
    user = update.message.from_user
    update.message.reply_text(f'Hello {user.first_name}! Welcome to the game of wits. I will pose you a riddle, and you have to try to solve it. Are you ready to play?')

# Function to handle the /riddle command
def riddle(update, context):
    # Get a random riddle
    riddle, answer = get_random_riddle()

    # Send the riddle to the user
    update.message.reply_text(f'Here is your riddle: {riddle}')

# Function to handle user answers
def answer(update, context):
    # Get the user's answer
    user_answer = update.message.text

    # Check if the answer is correct
    if user_answer.lower() == answer:
        update.message.reply_text('Correct! You win the round.')
    else:
        update.message.reply_text(f'Incorrect. The correct answer is "{answer}". I win the round.')

# Function to handle errors
def error(update, context):
    print(f'An error occurred: {context.error}')

if __name__ == '__main__':
    # Load the bot token from a file
    with open('bot_token.txt', 'r') as f:
        bot_token = f.read()

    # Create a bot and an updater
    bot = telegram.Bot(token=bot_token)
    updater = Updater(bot_token, use_context=True)

    # Set up the command handlers
    start_handler = CommandHandler('start', start)
    riddle_handler = CommandHandler('riddle', riddle)
    answer_handler = CommandHamdler('answer',answer)
