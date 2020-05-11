import time
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv
import time
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import sys
import csv
import random
import time
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time
import random


print("   .--.  .---. .-.  .-.  .--.  .-..-. ") 
print("  / {} \ } }}_}}  \/  { / {} \ \ {} / ") 
print(" /  /\  \| } \ | {  } |/  /\  \/ {} \ ") 
print(" `-'  `-'`-'-' `-'  `-'`-'  `-'`-'`-'      https://github.com/Pyshios ")

print("Armax is a Tool disgned manage some telegram group functions automating it with Telethon")


api_id = input("API ID:")
api_hash = input("HASH:")
phone = input("CELL NUMBER:")

SLEEP_TIME = 30
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))



def msg_all():
    input_file = "ext_members.csv"
    users = []
    with open(input_file, encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user['username'] = row[0]
            user['id'] = int(row[1])
            user['access_hash'] = int(row[2])
            user['name'] = row[3]
            users.append(user)

    mode = int(input("Enter 1 to send by user ID or 2 to send by username: "))
    #CHANGE HERE TO DIFERENT MESSAGES
    messages = ["Hello {}, How are you?", "Hi {}, What's up?", "Hey {}, do you want to gotrained?"]

    for user in users:
        if mode == 2:
            if user['username'] == "":
                continue
            receiver = client.get_input_entity(user['username'])
        elif mode == 1:
            receiver = InputPeerUser(user['id'], user['access_hash'])
        else:
            print("Invalid Mode. Exiting.")
            client.disconnect()
            sys.exit()
        message = random.choice(messages)
        try:
            print("Sending Message to:", user['name'])
            client.send_message(receiver, message.format(user['name']))
            print("Waiting {} seconds".format(SLEEP_TIME))
            time.sleep(SLEEP_TIME)
        except PeerFloodError:
            print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
            client.disconnect()
            sys.exit()
        except Exception as e:
            print("Error:", e)
            print("Trying to continue...")
            continue
    client.disconnect()
    print("Done. Message sent to all users.")

def ext_all():
    chats = []
    last_date = None
    chunk_size = 200
    groups = []

    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup == True:
                groups.append(chat)
        except:
            continue

    print('Choose a group to extract all members:')
    i = 0
    for g in groups:
        print(str(i) + '- ' + g.title)
        i += 1

    g_index = input("Enter a Number: ")
    target_group = groups[int(g_index)]

    print('Fetching Members...............')
    all_participants = []
    all_participants = client.get_participants(target_group, aggressive=True)

    print('Saving In file.............')
    with open("ext_members.csv", "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])
        for user in all_participants:
            if user.username:
                username = user.username
            else:
                username = ""
            if user.first_name:
                first_name = user.first_name
            else:
                first_name = ""
            if user.last_name:
                last_name = user.last_name
            else:
                last_name = ""
            name = (first_name + ' ' + last_name).strip()
            writer.writerow([username, user.id, user.access_hash, name, target_group.title, target_group.id])
    print('Members extracted successfully please check ext_members ')

def add_all():
    input_file = "ext_members.csv"
    users = []
    with open(input_file, encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user['username'] = row[0]
            user['id'] = int(row[1])
            user['access_hash'] = int(row[2])
            user['name'] = row[3]
            users.append(user)

    chats = []
    last_date = None
    chunk_size = 300
    groups = []

    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0))

    chats.extend(result.chats)
    dialogs = client.get_dialogs()

    m = input("1: For only permitted groups \n2: For all groups\n")

    for chat in chats:
        try:
            if chat.megagroup == True:
                groups.append(chat)
        except:
            continue

    print('Choose a group to add members:')
    i = 0
    for group in groups:
        print(str(i) + '- ' + group.title)
        i += 1

    g_index = input("Enter a Number: ")
    target_group = groups[int(g_index)]

    target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

    mode = int(input("Enter 1 to add by username or 2 to add by ID: "))

    n = 0

    for user in users:
        n += 1
        if n % 50 == 0:
            time.sleep(900)
        try:
            print("Adding {}".format(user['id']))
            if mode == 1:
                if user['username'] == "":
                    continue
                user_to_add = client.get_input_entity(user['username'])
            elif mode == 2:
                user_to_add = InputPeerUser(user['id'], user['access_hash'])
            else:
                sys.exit("Invalid Mode Selected. Please Try Again.")
            client(InviteToChannelRequest(target_group_entity, [user_to_add]))
            print("Waiting for 60-180 Seconds...")
            time.sleep(random.randrange(10, 20))
        except PeerFloodError:
            print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
        except UserPrivacyRestrictedError:
            print("The user's privacy settings do not allow you to do this. Skipping.")
        except:
            traceback.print_exc()
            print("Unexpected Error")
            continue

print("1) Extract all members from a group")
print("2) Add all group members Extracted ")
print("3) Send automatic messages")

a = input("Input your choice:")
b = int(a)



try:
    if b == 1 :
        print("Opening extractor")
        time.sleep(3)
        ext_all()
    elif b == 2:
        print("Opening automatic add ")
        time.sleep(3)
        add_all()
    elif b == 3:
        print("Opening automatic message sender ")
        time.sleep(3)
        msg_all()
except:
    print("not a valid choice")

    
    
    

