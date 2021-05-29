
# # --------------------------------------------- #
# # Plugin Name           : TelegramAirdropBot    #
# # Author Name           : trungtp               #
# # File Name             : main.py               #
# # --------------------------------------------- #

from telethon.sync import TelegramClient
import pymysql
from tginviter.storage import MemoryStorage
import time
import os
import telebot
from telethon import TelegramClient, Button, events 
from telegram.ext import Updater
from tginviter.client import TelethonClient
from telebot import types
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional, ClassVar, Union, Tuple, Any
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import ChatPhoto, TelegramObject, constants
from telegram.utils.types import JSONDict, FileInput, ODVInput, DVInput
import requests
api_id = 1861061452
api_hash = 'AAHL7nkKN2I3KC0JhHzjpbrrf4WkZjTPwT0'
phone = '+84338511781'

mysql_host = 'localhost'
mysql_db = 'airdrop'
mysql_user = 'root'
mysql_pw = '@At151202388@'
TEXT_ERROR = (
    "*Ошибка*\n\n"
    "Ссылка активации недействительна."
)
TEXT_SUCCESS = (
    "*Подписка активирована*\n\n"
    "Для перехода на канал используйте кнопку ниже."
)
TEXT_JOINCHAT_BUTTON = "Перейти на канал"

TEXT_ERROR = (
    "*Error*\n\n"
    "Invite token has been already used."
)
TEXT_SUCCESS = (
    "*Succes*\n\n"
    "Use button below to join secret channel."
)
TEXT_JOINCHAT_BUTTON = "Join channel"
# Secrets from .env file
# TELETHON_API_ID = int(os.environ.get("TELETHON_API_ID"))
# TELETHON_API_HASH = os.environ.get("TELETHON_API_HASH")
# TELETHON_SESSION_NAME = os.environ.get("TELETHON_SESSION_NAME")
# TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
# TEST_CHANNEL_ID = int(os.environ.get("TEST_CHANNEL_ID"))
TEST_JOINCHAT_KEY = os.environ.get("TEST_JOINCHAT_KEY")
bot_token = '1861061452:AAHL7nkKN2I3KC0JhHzjpbrrf4WkZjTPwT0'
bot = telebot.TeleBot(bot_token)

report_type = [
    "💳 Balance",
    "🔗 Referral link",
    "📤 Withdraw",
    "🌐 Our Website",
    "🔙 Start over"
]

import uuid
def get_random_token():
    """Generate random uuid token"""

    return uuid.uuid4()


def generate_invite_link(
    bot_name,
    *,
    token=None,
    max_uses=1,
    short=True,
    proto="https"
):
    """Generate customizable invite link"""

    if proto not in ["http", "https", "tg"]:
        raise ValueError("Use one of ['http', 'https', 'tg'] as proto")

    if not token:
        token = get_random_token()

    domain = "telegram.me/"
    if short:
        domain = "t.me/"

    params = f"{bot_name}?start={token}"
    if proto == "tg":
        domain = "resolve"
        params = f"?domain={bot_name}&start={token}"

    return f"{proto}://{domain}{params}", str(token)
# ////\
def get_connection():
    connection = pymysql.connect(host=mysql_host,
                                 user=mysql_user,
                                 password=mysql_pw,
                                 db=mysql_db,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor,
                                 autocommit=True)
    return connection
def create_tables():
    connection = get_connection()
    with connection.cursor() as cursor:
        table_name = "users"
        try:
            cursor.execute(
                "	CREATE TABLE `" + table_name + "` ( `user_id` int(12) DEFAULT NULL,  `address` varchar(42) DEFAULT NULL, `referral`  int(12) DEFAULT 0,`balance` int(12) DEFAULT 1000000000)")
            return create_tables
        except Exception as e:
            print(e)
try:
    get_db_tables = get_connection()
    get_db_tables
    create_db_tables = create_tables()
    create_db_tables
except:
    get_db_tables = get_connection()
    get_db_tables

def create_callbacks(storage):
    def deeplink_handler(update, context):
        if not context.args:
            return

        token = context.args[0]
        if storage.uses_left(token) <= 0:
            if update.message:
                update.message.reply_text(TEXT_ERROR, parse_mode="Markdown")
            return

        payload = storage.get_payload(token)

        joinchat_key = payload["joinchat_key"]
        keyboard = InlineKeyboardMarkup.from_button(
            InlineKeyboardButton(
                text=TEXT_JOINCHAT_BUTTON,
                url=generate_joinchat_link(joinchat_key)
            )
        )

        channel_id = payload["channel_id"]
        user_id = update.effective_user.id

        storage.add_subscription(channel_id, user_id)
        storage.count_new_use(token)

        time.sleep(2)

        if update.message:
            update.message.reply_text(
                TEXT_SUCCESS,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )

    job_num = 0
    def job_handler(context):
        nonlocal job_num
        job_num += 1

        # if job_num == 1:
        #     for channel_id in storage.get_channel_ids():
        #         client.subscribe_everyone(channel_id, storage)
        # else:
        #     for channel_id in storage.get_channel_ids():
        #         client.ban_extra_users(channel_id, storage)

    return job_handler,deeplink_handler
    # ///
def generate_joinchat_link(token, short=True):
    """Generate joinchat link"""

    domain = "telegram.me"
    if short:
        domain = "t.me"

    return f"https://{domain}/joinchat/{token}"
# @bot.message_handler(func=lambda message: True)     
# def echo_message(message):
#     cid = message.chat.id 
#     message_text = message.text 
#     user_id = message.from_user.id 
#     user_name = message.from_user.first_name 
#     mention = "["+user_name+"](tg://user?id="+str(user_id)+")"

#     if message_text.lower() == "hi":
#         bot.send_message(cid,"Hi, " + mention,parse_mode="Markdown")
# # ///////

@bot.message_handler(commands=["start"])
def start(chat):
 
    # keyboard = [[types.InlineKeyboardButton("Hackerearth", callback_data='/start@CHE_Finance_group'),
    #                      types.InlineKeyboardButton("Hackerrank", callback_data='HRlist8',url='https://t.me/che_finance_group'),],
    #                     [types.InlineKeyboardButton("Codechef", callback_data='CClist8'),
    #                      types.InlineKeyboardButton("Spoj", callback_data='SPlist8')],
    #                     [types.InlineKeyboardButton("Codeforces", callback_data='CFlist8'),
    #                      types.InlineKeyboardButton("ALL", callback_data='ALLlist8')]]
    # reply_markup = types.InlineKeyboardMarkup(keyboard)
    # keyboard = [[types.InlineKeyboardButton("CHE Finance group  ",callback_data='HRlist7',url='https://t.me/che_finance_group')],
    #             [types.InlineKeyboardButton("CHE Finance channel", callback_data='HRlist8',url='https://t.me/che_finance_channel')]]
    # reply_markup = types.InlineKeyboardMarkup(keyboard)

 
    # markup_settings_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # markup_settings_menu.add(types.KeyboardButton("💳 Balance"),
    #                          types.KeyboardButton("🔗 Referral link"),
    #                          types.KeyboardButton("📤 Withdraw"),
    #                          types.KeyboardButton("🌐 Our Website"),
    #                          types.KeyboardButton("🌐 Eixt"))
    # bot.send_message(
    #     chat.chat.id,
    #     'Hello!',
    #     reply_markup=reply_markup
    # )


    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    # reg_button = types.KeyboardButton(text="🚀 Join airdrop", request_contact=True)
    reg_button = types.KeyboardButton(text="🚀 Join airdrop")
    keyboard.add(reg_button)

    bot.send_message(
        chat.chat.id,
        """ Welcome to your reward,I am your friendly CHE Airdrop bot.

    ✅ Follow these simple tasks for a chance to earn up to $50 (1000000000 CHE) 5$(100000000 CHE) each Referral

        Please follow the step by step Guide:
            🔹 Follow CHE Finance on Twitter, Retweet the pinned post and Tag 3 friends.
            🔹 Join group and channel.
            🔹 Submit your BEP20 Wallet Address.

    ✅ Plan or in the near future

        💠 Q2 2021
            🔹 Launch of CHE on Binance Smart Chain.
            🔹 Airdrop & Swap on pancakeswap/bakeryswap.
        💠 Q3 2021
            🔹 Launch of official website.
            🔹 CHE is be listed crypto exchanges.
            🔹 Release stake pool and reward for staking.
        💠 Q1 2022
            🔹 Launching CHES, CHE Wallet 1.0 Release (iOS & Android).
            🔹 Release CHES pool and reward for staking, Release charity funds.
            🔹 There is a large amount of reward remaining, the leftover will be burned.

                    Join now!
                """,
        reply_markup=keyboard,
    )

    connection = get_db_tables
    with connection.cursor() as cursor:
        sql = "SELECT user_id FROM airdrop.users WHERE user_id = " + str(chat.chat.id) + ";"
        cursor.execute(sql)
        a = 0
        for user in cursor.fetchall():
            a = 1
        if a == 0:
            sql = "INSERT INTO airdrop.users (user_id, address,referral,balance) VALUES (" + str(chat.chat.id) + ", " + "'yyy'" + ", 0, 1000000000 );" 
            cursor.execute(sql)
    if '/start r' in str(chat.html_text):
        if str(chat.chat.id) in str(chat.html_text):
            bot.send_message(chat.chat.id, 'Airdrop CHE' )
        else:
            invi = str(chat.html_text).split(' r')
            with connection.cursor() as cursor:
                sql =  "SELECT * FROM airdrop.users WHERE user_id = " + str(invi[1]) + ";"
                cursor.execute(sql)
                b = 0
                for user in cursor.fetchall():
                    b = 1
            if b == 1:
                for user in cursor.fetchall():
                    bot.send_message(invi[1], 'Referral count ' + str(int(user['referral'])+1) )
                with connection.cursor() as cursor:
                    sql =  "UPDATE airdrop.users SET referral = referral + 1 WHERE user_id = " + str(invi[1]) + ";"
                    cursor.execute(sql)
                    sql =  "UPDATE airdrop.users SET balance = balance + 100000000 WHERE user_id = " + str(invi[1]) + ";"
                    cursor.execute(sql)
    connection.commit()
    bot.register_next_step_handler(chat, contact_handler)


def contact_handler(contact):
    if contact.contact:
        # a = bot.get_chat('WaterFinance_airdrop_bot')
        # a = bot.get_chat_member('1001492695567',contact.chat.id)
        link, token = generate_invite_link("@WaterFinance_airdrop_bot")
        # link, token = generate_invite_link("@WaterFinance_airdrop_bot")

        # link, token = generate_invite_link("@WaterFinance_airdrop_bot", short=False)


        # link, token = generate_invite_link("@WaterFinance_airdrop_bot",max_uses=10000, proto="tg")

        # storage = MemoryStorage()

        # client = TelethonClient(
        #     api_id=os.environ.get("TELETHON_API_ID"),
        #     api_hash=TELETHON_API_HASH,
        #     session=TELETHON_SESSION_NAME
        # )
        # deeplink_handler, job_handler = create_callbacks(storage)

        # bot.reply_to(contact, 'Number verified.')
# 
        # keyboard = types.ReplyKeyboardMarkup(
        # one_time_keyboard=True, resize_keyboard=True
        # )
        # keyboard.add("✅ Done Telegram")
        # bot.send_message(
        # contact.chat.id, """For more information, first complete this 2 Tasks then click Next Step:\n💠 join our Telegram group @CHE_Finance_group\n💠 join our Telegram channel @CHE_Finance_channel"""
        # , reply_markup=keyboard
        # )
        # bot.register_next_step_handler(contact, contact_handler)
# 

        # return contact_handler(contact)
        # keyboard = types.ReplyKeyboardMarkup(
        # one_time_keyboard=True, resize_keyboard=True
        # )
        # keyboard.add("✅ Done Twetter")
        # bot.send_message(
        # contact.chat.id, "Join Group -> @group", reply_markup=keyboard
        # )
        # bot.register_next_step_handler(contact, select_submission_type)
    else:
        if contact.html_text == '/start':
            return start(contact)
        else:
            if contact.html_text == '✅ Done Telegram':

                try:
                    if bot.get_chat_member(bot.get_chat("@CHE_Finance_group").id,str(contact.chat.id)).status != 'left':
                        keyboard = types.ReplyKeyboardMarkup(
                        one_time_keyboard=True, resize_keyboard=True
                        )
                        keyboard.add("✅ Done Twitter")
                        text = "TFF,Now\n" + "💠 Follow <a href='https://twitter.com/vineprotocol'>CHE Finance</a> on Twitter,Tag 3 friends and Retweet the pinned post .\n"
                        text = text + "💠 Then submit your Twitter username with @:\n"
                        text = text + "💠 Example: @Username\n💠 (Note⚠️- We will manually verify all entries)"
                        bot.send_message(
                        contact.chat.id, text
                        ,parse_mode='HTML',reply_markup=keyboard)
                        bot.register_next_step_handler(contact, contact_handler)
                    else:
                        bot.send_message(
                        contact.chat.id, "join group now -> @CHE_Finance_group"
                        )
                        bot.register_next_step_handler(contact, contact_handler)
                except:
                    bot.register_next_step_handler(contact, contact_handler)
                # keyboard = types.ReplyKeyboardMarkup(
                # one_time_keyboard=True, resize_keyboard=True
                # )
                # keyboard.add("✅ Done Twitter")
            elif contact.html_text == '🚀 Join airdrop' or contact.html_text == '🔙 Start over' :
                keyboard = types.ReplyKeyboardMarkup(
                one_time_keyboard=True, resize_keyboard=True
                )
                keyboard.add("✅ Done Telegram")
                bot.send_message(
                contact.chat.id, "Main Menu"
                , reply_markup=keyboard
                )
                #
                keyboard = [[types.InlineKeyboardButton("CHE Finance group  ",callback_data='HRlist7',url='https://t.me/che_finance_group')],
                [types.InlineKeyboardButton("CHE Finance channel", callback_data='HRlist8',url='https://t.me/che_finance_channel')]]
                reply_markup = types.InlineKeyboardMarkup(keyboard)
                bot.send_message(
                contact.chat.id,
                'For more information, first complete this 2 Tasks then click Next Step:\n💠 join our Telegram group @CHE_Finance_group\n💠 join our Telegram channel @CHE_Finance_channel',
                reply_markup=reply_markup
                )
                #
                bot.register_next_step_handler(contact, contact_handler)
            elif contact.html_text == '✅ Done Twitter':
                keyboard = types.ReplyKeyboardMarkup(
                one_time_keyboard=True, resize_keyboard=True
                )
                keyboard.add("✅ Done")
                bot.send_message(
                contact.chat.id, "Submit BSC (BEP20) Address in truswallet or metamask wallet:", reply_markup=keyboard
                )
                bot.register_next_step_handler(contact, contact_handler)
            elif contact.html_text == '✅ Done':
                # bot.register_next_step_handler(contact, select_submission_type)
                select_submission_type(contact)
            elif '@' in contact.html_text :
                bot.send_message(
                contact.chat.id, "Submit BSC (BEP20) Address in truswallet or metamask wallet:"
                )
                bot.register_next_step_handler(contact, contact_handler)
            else:
                if '@' not in contact.html_text and len(contact.html_text) > 20 :
                    #check and save address bsc
                    connection = get_db_tables
                    with connection.cursor() as cursor:
                        sql = "UPDATE airdrop.users SET address = " + "'" + contact.html_text + "'" + " WHERE user_id = " + str(contact.chat.id,) + ";"
                        cursor.execute(sql)
                        # sql =  "UP 
                        connection.commit()
                    #waiting hand click
                    select_submission_type(contact)
                else:
                    bot.send_message(contact.chat.id, "It looks like the information you entered is incorrect or the action is incorrect :((")
                    bot.register_next_step_handler(contact, contact_handler)
            # bot.register_next_step_handler(contact, contact_handler)
        # bot.send_message(contact.chat.id, "Please share phone number to continue.")
        # bot.register_next_step_handler(contact, contact_handler)


def select_submission_type(submission_type):
    markup_settings_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup_settings_menu.add(types.KeyboardButton("💳 Balance"),
                             types.KeyboardButton("🔗 Referral link"),
                             types.KeyboardButton("📤 Withdraw"),
                             types.KeyboardButton("🌐 Our Website"),
                             types.KeyboardButton("🔙 Start over"))
    bot.send_message(
        submission_type.chat.id, "Select model:", reply_markup=markup_settings_menu
    )
    bot.register_next_step_handler(submission_type, verify_submission_type)


def verify_submission_type(verify_submission):
    if verify_submission.text not in report_type:
        if verify_submission.html_text == '/start':
            return start(verify_submission)
        check = '/start r' + str(verify_submission.chat.id)
        if '/start r' in str(verify_submission.html_text):
            if str(verify_submission.chat.id) in str(verify_submission.html_text):
                return start(verify_submission)
            else:
                invi = str(verify_submission.html_text).split(' r')
                # bot.send_message(invi[1], 'Referral count 1' )
        bot.reply_to(verify_submission, 'Please select model from list')
        bot.register_next_step_handler(verify_submission, verify_submission_type)
    else:
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM airdrop.users WHERE user_id = " + str(verify_submission.chat.id) + ";"
            cursor.execute(sql)
        if verify_submission.html_text == '🔗 Referral link':
            # updater = Updater('1732490976:AAEde5-gJnShVCsVnwfEi7UWGi5BjBrD_eg')
            chat_id = verify_submission.chat.id
            text='https://t.me/CHE_Finance_bot?start=r'+str(chat_id)
            #getnumber referral
            for user in cursor.fetchall():
                try:
                    bot.send_message(verify_submission.chat.id, 'Referral link: \n' +  text + "\n\n👥 Total Referrals: " + str(user['referral']))
                except:
                    bot.send_message(verify_submission.chat.id, 'Referral link: \n' +  text + "\n\n👥 Total Referrals: 0" )
                    connection.close()
        elif verify_submission.html_text == '🌐 Our Website':
            bot.send_message(verify_submission.chat.id," Website: " + "<a href=''>Cooming soon</a>",parse_mode='HTML')
        elif verify_submission.html_text == '📤 Withdraw':
            bot.send_message(verify_submission.chat.id, 'Automatic withdrawal will be processed on August 30')
        elif verify_submission.html_text == '🔙 Start over':
            # bot.stop_polling()
            return contact_handler(verify_submission)
        elif verify_submission.html_text == '💳 Balance':
            for user in cursor.fetchall():
                try:
                    bot.send_message(verify_submission.chat.id, ' 💰 Balance : '+str(user['balance'])+' CHE\n\n 🎁 10000000 CHE per referral' + '\n\n 📤  Wallet : ' + str(user['address']) + '\n\n 👥 Total Referrals : ' + str(user['referral']))
                except:
                    connection.close()
            # bot.send_message(verify_submission.chat.id, ' 💰 Balance : 1000000000 WATER\n\n 🎁 10000000 WATER per referral' + '\n\n 📤  Wallet : jhbjhbj' + '\n\n 👥 People invited : 0')
        # bot.reply_to(verify_submission, 'Car model selected.')
        # bot.register_next_step_handler(verify_submission, finish)
        bot.register_next_step_handler(verify_submission, verify_submission_type)


def finish(f):
    bot.send_message(f.chat.id, 'Done.')


if __name__ == "__main__":
    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()
    bot.polling()

