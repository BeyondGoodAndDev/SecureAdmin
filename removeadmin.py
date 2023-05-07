#Script author: @Temporizzato aka T

#The purpose of this script is to remove administrators privileges to every users that
#ban too much users in the last hour. It is for groups that have a /ban command to ban
#users (specially those that works with group help). 

#It get the messages sent from your administrators and analyze how many times their
#messages have the command /ban inside and if there are more than 20 /ban command by the same
#admin in the last hour it will remove his admin role.

#This script also send a message to a user (like the founder of the group) in private to let him
#know that NAMEOFADMIN was removed as administrator. 

#Not only that, in group help there is an option to remove all inactive users, i'm Italian and
#in Italian the command is /inattivi, you should change it as per your language to make it work,
#This script will remove admin privilege to group help as soon as it intercept the command to delete
#all inactive users

#After this script remove an admin for /ban command used too much, the admin cannot be admin for almost
#one hour, as at every new message from him it will ALWAYS know that the user sent too many bans in 
#the last hour

#Also, you can use the command /security and the user related to this script will send you 
#a message in private to let you know if it is working or not (if no answer it is stopped problably)

#This script is made in 2 hours, it works, but for sure it can be improved in many ways
#Be sure to read all the code and change what need to be changed to make it work, i've done
#my best with comments.

#If you would like to donate for this script i will be happy, you can send something at chiaratentoti95@gmail,com
#via paypal, but it is not needed, if something good happen i will problably improve that. Thank you so much


#Pay attention: the script works when you create your admins using the user related to this script,
#otherwise it cannot remove their admin privileges if necessary

#This script is tested on Telethon 1.26

from telethon import TelegramClient, events, errors, types
from datetime import datetime, timedelta
from telethon import functions, types

import time
import asyncio

# Replace with your own values, this is the users that should create admins in your group
api_id = ''
api_hash = ''
session_name = 'Security Bot for Admins'
chat_id = '' #This is the chat id of the group where the user-bot should work

client = TelegramClient(session_name, api_id, api_hash)

# global variable to keep track of banned users
banned_users = {}

@client.on(events.NewMessage(chats=int(chat_id)))
async def check_ban_count(event):


    try_inattivi = False
    check_active = False
    check_active_priv = False

    #Here it will intercept the /security command only if sent by specific user (as founder of the group)
    #and will send a message in private to this user to let him know that the script is online and working
    if event.sender.id == 55555555 or event.sender.id == 55555555: #replace 55555555 with the users that should receive the message
        if event.message.message == '/security':
            check_active_priv = True

    if check_active_priv == True:
        if event.sender.id == 55555555: #replace 55555555 with id of the founder, replace the id also in next line with same value as this line
            await client.send_message(55555555, f"I'm active and i'm monitoring, don't worry.")
        elif event.sender.id == 55555555: # replace 55555555 with the id of other user that can use /security command, replace the id also in next line with same value as this line
            await client.send_message(55555555, f"I'm active and i'm monitoring, don't worry.")

        #uncomment and add an elif for every user that can use /security command
        #elif event.sender.id == 55555555: # replace 55555555 with the id of other user that can use /security command
            #await client.send_message(5376299916, f"Sono attivo e sto sorvegliando. Non ti preoccupare.")



    if not event.is_group or not event.sender or event.sender.bot:
        return

    # check if the sender is an admin
    try:
        user = await client.get_permissions(event.chat_id, event.sender)
        if not user.is_admin:
            return
    except errors.rpcerrorlist.UserNotParticipantError:
        return

    if event.message.message == '/inattivi': #replace /inattivi with the command of group help to kick or ban inactive users in your language
        try_inattivi = True

    


    current_time = time.time()
    hour_ago = current_time - 3600

    # get all events from the last hour
    ban_count = 0
    checkw = '/ban' #intercept /ban command in messages sent from your administrators
    async for message in client.iter_messages(event.chat_id, from_user=event.sender.id, min_id=1, max_id=event.id, reverse=True):

        if checkw in message.text:
            ban_count += 1

        if message.date.timestamp() > hour_ago:
            break


    # check if the admin has banned more than 20 users in the last hour
    if ban_count >= 20:
        # remove the admin rights
        await client(functions.channels.EditAdminRequest(
                                        channel=event.chat_id,
                                        user_id=event.sender.id,
                                        admin_rights=types.ChatAdminRights(
                                                invite_users=False,
                                                ban_users=False,
                                                ),
                                        rank=''

                                        ))


        # send a message in the group
        await client.send_message(event.chat_id, f"{event.sender.first_name} lost his admin role because banned too much users.")
        #replace following 55555555 with the id of every users that should receive a message to know that someone used /ban command too much
        await client.send_message(55555555, f"{event.sender.first_name} lost his admin role because banned too much users.")
        #await client.send_message(55555555, f"{event.sender.first_name} lost his admin role because banned too much users.")
        #await client.send_message(55555555, f"{event.sender.first_name} lost his admin role because banned too much users.")
        #await client.send_message(55555555, f"{event.sender.first_name} lost his admin role because banned too much users.")
        #await client.send_message(55555555, f"{event.sender.first_name} lost his admin role because banned too much users.")


    if try_inattivi == True: #if someone tried to used the command to remove inactive users, remove admin privileges
        # remove the admin rights
        await client(functions.channels.EditAdminRequest(
                                        channel=event.chat_id,
                                        user_id=event.sender.id,
                                        admin_rights=types.ChatAdminRights(
                                                invite_users=False,
                                                ban_users=False,
                                                ),
                                        rank=''

                                        ))

        # send a message to notify the admin, replace 55555555 with the id of users that should receive a message in private to know that someone used the command and lost his admin role
        await client.send_message(event.chat_id, f"{event.sender.first_name} lost admin role because tried to remove all inactive users")
        await client.send_message(55555555, f"{event.sender.first_name} lost admin role because tried to remove all inactive users")
        #await client.send_message(55555555, f"{event.sender.first_name} lost admin role because tried to remove all inactive users")
        #uncomment and add any times for any admin should receive a notification message
        #await client.send_message(55555555, f"{event.sender.first_name} lost admin role because tried to remove all inactive users")

    


# start the client
client.start()
client.run_until_disconnected()