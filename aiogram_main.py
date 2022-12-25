import aiogram.utils
import aiogram.types
import aiogram.dispatcher
import aiogram.utils.markdown
import aiogram.utils.helper
import aiogram.dispatcher.filters
import aiogram.dispatcher.middlewares
import aiogram.utils.executor
import sqlite3

# Replace this with your bot's token
TOKEN = 'YOUR_BOT_TOKEN'

# Replace this with the file path of your database
DB_FILE = 'database.db'

# Replace this with the user IDs of your bot's admins
ADMINS = [12345678]

# Initialize the bot
bot = aiogram.utils.Bot(token=TOKEN)

# Initialize the dispatcher
dp = aiogram.dispatcher.Dispatcher(bot)

# Define a handler function for the "/start" command
@dp.message_handler(commands='start')
async def start_command(message: aiogram.types.Message):
    # Save the user's name and user id in the database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (user_id, name) VALUES (?, ?)", (message.from_user.id, message.from_user.full_name))
    conn.commit()
    cursor.close()
    conn.close()

    # Retrieve a random question from the database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1")
    question = cursor.fetchone()
    cursor.close()
    conn.close()

    # Create a keyboard with buttons
    keyboard = aiogram.types.InlineKeyboardMarkup()
    button_yes = aiogram.types.InlineKeyboardButton(text='Ha', callback_data='answer_yes')
    button_no = aiogram.types.InlineKeyboardButton(text='Yo\'q', callback_data='answer_no')
    keyboard.add(button_yes, button_no)

    # Send the question and keyboard to the user
    await bot.send_message(
        message.chat.id,
        f"{question[1]}",
        reply_markup=keyboard
    )

# Define a handler function for button clicks
@dp.callback_query_handler(lambda call: True)
async def process_callback_button(call: aiogram.types.CallbackQuery):
    # Check the callback data of the button
    if call.data == 'answer_yes':
        # Retrieve the answer to the question
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT answer FROM questions WHERE id=?", (question[0],))
        answer = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        # Check if the user's answer is correct
        if answer == 'Yes':
            # Update the user's score in the database
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET score=score+1 WHERE user_id=?", (call.from_user.id,))
            conn.commit()
            cursor.close()
            conn.close()

            # Send a message to the user indicating that they got the answer correct
            await bot.answer_callback_query(call.id, text='To\'g\'ri! Sizga 1 ball qo\'shildi.')
        else:
            # Send a message to the user indicating that they got the answer incorrect
            await bot.answer_callback_query(call.id, text='Noto\'g\'ri! Sizning javobingiz noto\'g\'ri.')
    elif call.data == 'answer_no':
        # Retrieve the answer to the question
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT answer FROM questions WHERE id=?", (question[0],))
        answer = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        # Check if the user's answer is correct
        if answer == 'No':
            # Update the user's score in the database
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET score=score+1 WHERE user_id=?", (call.from_user.id,))
            conn.commit()
            cursor.close()
            conn.close()

            # Send a message to the user indicating that they got the answer correct
            await bot.answer_callback_query(call.id, text='To\'g\'ri! Sizga 1 ball qo\'shildi.')
        else:
            # Send a message to the user indicating that they got the answer incorrect
            await bot.answer_callback_query(call.id, text='Noto\'g\'ri! Sizning javobingiz noto\'g\'ri.')

# Define a handler function for the "/mypoints" command
@dp.message_handler(commands='mypoints')
async def mypoints_command(message: aiogram.types.Message):
    # Retrieve the user's score from the database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT score FROM users WHERE user_id=?", (message.from_user.id,))
    score = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    # Send a message to the user with their score
    await bot.send_message(
        message.chat.id,
        f"Sizning ballingiz: {score}"
    )

# Define a handler function for the "/admin" command
@dp.message_handler(commands='admin')
async def admin_command(message: aiogram.types.Message):
    # Check if the user is an admin
    if message.from_user.id in ADMINS:
        # Create a keyboard with buttons
        keyboard = aiogram.types.InlineKeyboardMarkup()
        button_add_question = aiogram.types.InlineKeyboardButton(text='Savol qo\'shish', callback_data='add_question')
        button_edit_question = aiogram.types.InlineKeyboardButton(text='Savolni tahrirlash', callback_data='edit_question')
        button_view_questions = aiogram.types.InlineKeyboardButton(text='Savollar', callback_data='view_questions')
        button_send_message = aiogram.types.InlineKeyboardButton(text='Xabar yuborish', callback_data='send_message')
        keyboard.add(button_add_question, button_edit_question, button_view_questions, button_send_message)

        # Send the keyboard to the user
        await bot.send_message(
            message.chat.id,
            'Admin paneli',
            reply_markup=keyboard
        )
    else:
        # Send a message to the user indicating that they are not an admin
        await bot.send_message(
            message.chat.id,
            'Siz admin emassiz!'
        )

# Define
# Define a handler function for button clicks in the admin panel
@dp.callback_query_handler(lambda call: True)
async def process_callback_button(call: aiogram.types.CallbackQuery):
    # Check the callback data of the button
    if call.data == 'add_question':
        # Prompt the user to enter a question
        await bot.send_message(
            call.from_user.id,
            'Savol qo\'shish:\nSavol yozing:'
        )

        # Wait for the user's response
        response = await bot.wait_for_message(
            chat_id=call.from_user.id
        )

        # Prompt the user to enter an answer
        await bot.send_message(
            call.from_user.id,
            'Savolni javob bering:'
        )

        # Wait for the user's response
        answer = await bot.wait_for_message(
            chat_id=call.from_user.id
        )

        # Add the question and answer to the database
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO questions (question, answer) VALUES (?, ?)", (response.text, answer.text))
        conn.commit()
        cursor.close()
        conn.close()

        # Send a message to the user indicating that the question was added
        await bot.send_message(
            call.from_user.id,
            'Savol qo\'shildi!'
        )
    elif call.data == 'edit_question':
        # Prompt the user to enter the id of the question to edit
        await bot.send_message(
            call.from_user.id,
            'Savolni tahrirlash:\nTahrirlanishni istagan savolning id raqamini kiriting:'
        )

        # Wait for the user's response
        response = await bot.wait_for_message(
            chat_id=call.from_user.id)
        # Check if the id is valid
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM questions WHERE id=?", (response.text,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result is None:
            # Send a message to the user indicating that the id is invalid
            await bot.send_message(
                call.from_user.id,
                'Id noto\'g\'ri!'
            )
            return

        # Prompt the user to enter the new question
        await bot.send_message(
            call.from_user.id,
            'Savolni tahrirlash:\nYangi savol yozing:'
        )

        # Wait for the user's response
        question = await bot.wait_for_message(
            chat_id=call.from_user.id
        )

        # Prompt the user to enter the new answer
        await bot.send_message(
            call.from_user.id,
            'Savolni tahrirlash:\nYangi javob bering:'
        )

        # Wait for the user's response
        answer = await bot.wait_for_message(
            chat_id=call.from_user.id
        )

        # Update the question and answer in the database
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("UPDATE questions SET question=?, answer=? WHERE id=?", (question.text, answer.text, response.text))
        conn.commit()
        cursor.close()
        conn.close()

        # Send a message to the user indicating that the question was edited
        await bot.send_message(
            call.from_user.id,
            'Savol tahrirlandi!'
        )
    elif call.data == 'view_questions':
        # Retrieve all questions from the database
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM questions")
        questions = cursor.fetchall()
        cursor.close()
        conn.close()

        # Build a message with the questions
        message = 'Savollar:\n'
        for question in questions:
            message += f"{question[0]}: {question[1]}\n"

        # Send the message to the user
        await bot.send_message(
            call.from_user.id,
            message
        )
    elif call.data == 'send_message':
        # Prompt the user to enter a message
        await bot.send_message(
            call.from_user.id,
            'Xabar yuborish:\nXabaringiz:'
        )
        # Wait for the user's response
        message = await bot.wait_for_message(
            chat_id=call.from_user.id
        )

        # Retrieve all user ids from the database
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users")
        user_ids = cursor.fetchall()
        cursor.close()
        conn.close()

        # Send the message to all users
        for user_id in user_ids:
            await bot.send_message(
                user_id[0],
                message.text
            )

        # Send a confirmation message to the user
        await bot.send_message(
            call.from_user.id,
            'Xabar yuborildi!'
        )

# Set the bot to be run on a certain interval
scheduler.add_job(game, 'interval', hours=12)

# Start the bot
dp.loop.create_task(send_updates())
dp.loop.create_task(scheduler.start())
dp.loop.create_task(bot.polling())
       

