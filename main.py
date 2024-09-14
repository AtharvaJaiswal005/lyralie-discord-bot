import os
import discord
import requests
import json
import random
from pickupline import pickupline
import data as db
from keep_alive import keep_alive
keep_alive()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

greet = ['Hey', 'hey', 'Hello', 'hello', 'hi', 'Hi', 'yo', 'Yo', 'sup', 'Sup', 'what\'s up', 'What\'s up', 'howdy', 'Howdy',
         'hey there', 'Hey there', 'hiya', 'Hiya', 'greetings', 'Greetings', 'how\'s it going', 'How\'s it going', 'yoohoo',
         'Yoohoo', 'holla', 'Holla', 'howdy-do', 'Howdy-do', 'aloha', 'Aloha', 'hi there', 'Hi there', 'good day', 'Good day',
         'what\'s happening', 'What\'s happening', 'hi friend', 'Hi friend', 'hi pal', 'Hi pal', 'hey buddy', 'Hey buddy',
         'hi mate', 'Hi mate', 'hi dude', 'Hi dude', 'hey dude', 'Hey dude', 'hiya mate', 'Hiya mate', 'hiya pal', 'Hiya pal',
         'hey gorgeous', 'Hey gorgeous', 'hello beautiful', 'Hello beautiful', 'hey love', 'Hey love', 'hello love', 'Hello love',
         'hey sweetie', 'Hey sweetie', 'hello sweetie', 'Hello sweetie', 'hi sunshine', 'Hi sunshine', 'hello sunshine', 'Hello sunshine',
         'hey cutie', 'Hey cutie', 'hello cutie', 'Hello cutie', 'hey hottie', 'Hey hottie', 'hello hottie', 'Hello hottie',
        ]

greet_res = ["Hey there! What's going on?", "Hello, lovely! How are you?", "Hey! Long time no see.", 
             "Hiya! How's your day so far?", "Yoohoo! What brings you here?", "Hi friend! What's up?",
             "Hey dude! Ready for some fun?", "Hi there! What's happening?", "Hey buddy! How's life?",
             "Hello sunshine! Ready to shine?", "Hi cutie! How's it going?", "Hey love! Missed you.",
             "Hello beautiful! What's new?", "Hey sweetie! How's your day?", "Howdy-do! What's the news?",
             "Aloha! How's the day treating you?", "Sup? Anything exciting happening?", "Yo! What's the word?",
             "Hiya mate! What's the plan?", "Greetings! How can I assist you?", "Howdy! Ready for an adventure?",
             "Hi pal! What's cooking?", "Hiya pal! Long time no chat.", "Hey gorgeous! Looking fabulous as always.",
             "Hello love! How's everything?", "Hi sunshine! Ready to brighten the day?", "Hey cutie! What's up?",
             "Hello hottie! Looking good!", "Hiya mate! What's the vibe?", "Hey there! How's life treating you?",
             "Hey my friend! How's it going?", "My pal! What's the latest?"]

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " ~" + json_data[0]['a']
    return quote
help_command = '''
Greetings, puny humans! I am **Lyralei ヅ**, your mischievous bot extraordinaire. Crafted with Python 3.10.6, I'm here to bring chaos, laughter, and a sprinkle of magic to your server.

Behold, the commands and their mystical powers:
- `;help`: Uncover the secrets of the bot and its mysterious commands.
- `;motivate`: Receive an enchanting quote to elevate your spirits.
- `;pickupline`: Summon a Dota-themed pickup line that might crit your heart.
- `;choose-from arg1, arg2, ...`: Let me roll the dice of destiny and choose from your options.
- `;rolldice`: Roll the magical dice and see what fate has in store for you.
- `;gif <search_term>`: Use the ancient art of Giphy to summon a GIF with specific search terms.
- `;roast @mentionsomeone`: Unleash the banter upon your friends by mentioning them.
- `;wish-buday @mentionuser`: Celebrate someone's birthday with a touch of magical gifs.
- `;view-buday`: Gaze into the crystal ball to see upcoming birthdays.
- `;clear-buday`: Erase birthday data as if it never existed.
- `;set-buday @mentionuser, birthday`: Set the birthday for a user with a touch of magic.

General Greetings: I shall respond to your greetings with a mischievous grin.

Feel free to dance in the chaos! If you seek wisdom or simply want to chat, I might just respond.

Best magical regards,
Lyralei ヅ

______________________________________________________________________
🏠 [Main Page](https://lyraliebot.000webhostapp.com/)
✉️ [Send Feedback](https://lyraliebot.000webhostapp.com/feedback.html)
🌐 [Creator's LinkedIn](https://www.linkedin.com/in/atharva-jaiswal/)
📧 [Contact Wizard Who created Me ](https://lyraliebot.000webhostapp.com/c.html)
💡  [Support Creator](https://lyraliebot.000webhostapp.com/s.html)
'''

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_member_join(member):
    join = True

# Birthday handler
import datetime

current_date = datetime.date.today()
current_year = current_date.year
current_month_day = str(current_date)[5:]

# Dictionary to store birthday information for each server
birthday_data = {}

def set(server_id, user, d):
    try:
        datetime.datetime.strptime(d, '%Y-%m-%d')
        
        # Check if the server exists in the dictionary
        if server_id not in birthday_data:
            birthday_data[server_id] = {'user': [], 'b_date': [], 'wished': []}
        
        birthday_data[server_id]['user'].append(user)
        birthday_data[server_id]['b_date'].append(d)
        birthday_data[server_id]['wished'].append(False)  # Set wished status to False initially
        print(f"Birthday set for {user} in server {server_id}: {d}")
    except ValueError:
        print("Invalid date format. Please use the format 'YYYY-MM-DD'.")

def view(server_id):
    try:
        o = "User    Birthdays    Days Left"
        for i in range(len(birthday_data[server_id]['b_date'])):
            birth_date = datetime.datetime.strptime(birthday_data[server_id]['b_date'][i], '%Y-%m-%d').date()
            next_birthday = datetime.date(current_year, birth_date.month, birth_date.day)
            days_left = (next_birthday - current_date).days
            if days_left < 0:
                next_birthday = datetime.date(current_year + 1, birth_date.month, birth_date.day)
                days_left = (next_birthday - current_date).days
            o += f'\n{birthday_data[server_id]["user"][i]}    {birthday_data[server_id]["b_date"][i]}    {days_left} days left'
        return o
    except Exception as e:
        pass


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    u_msg = str(message.content)

    if message.author == client.user:
        return

    # Check for birthdays and wish users
    server_id = str(message.guild.id) if message.guild else None  # Get the server ID or None if not in a guild
    if server_id and birthday_data.get(server_id):  # Check if server_id is not None and exists in birthday_data
        for i in range(len(birthday_data[server_id].get('b_date', []))):
            date = birthday_data[server_id]['b_date'][i]
            if date[5:] == current_month_day and not birthday_data[server_id]['wished'][i]:
                birth_year = int(date[:4])
                age = current_year - birth_year
                birthday_message = f"Happy Birthday {birthday_data[server_id]['user'][i]}! You are {age} years old this year. \n{db.b_msg()}"
                await message.channel.send(birthday_message)
                await message.channel.send(db.b_gif())
                # Mark the birthday as wished
                birthday_data[server_id]['wished'][i] = True

    if u_msg.lower().startswith(';set-buday'):
        print(u_msg)
        msg = u_msg
        msg = ''.join(msg.split())
        u = msg.split(',')[0]
        bd = msg.split(',')[-1]
        set(server_id, u[10:], msg.split(',')[-1])
        await message.channel.send(f'Birthday Set for {u[10:]} on {bd}')
        print(birthday_data)
    elif u_msg.lower() == ';view-buday':
        if server_id and birthday_data.get(server_id, {}).get('user'):
            await message.channel.send(view(server_id))
        else:
            await message.channel.send('No birthdays found.')
    elif u_msg.lower() == ';clear-buday':
        if server_id and server_id in birthday_data:
            birthday_data[server_id] = {'user': [], 'b_date': [], 'wished': []}
            await message.channel.send("Birthday data cleared.")
        else:
            await message.channel.send("No birthdays found to clear.")

    if u_msg.lower() == ';motivate':
        await message.channel.send(get_quote())
    elif u_msg.lower() == ';pickupline':
        await message.channel.send(pickupline())
    elif u_msg.lower() == ';help':
        await message.channel.send(help_command)
    elif u_msg.lower() == ';rolldice':
        await message.channel.send(random.choice([i for i in range(1,7)]))
    elif u_msg.lower().startswith(';roast'):
        mentioned_user = message.mentions[0] if message.mentions else None
        if mentioned_user:
            roast_message = f"{mentioned_user.mention}, {db.roast()}"
            await message.channel.send(roast_message)
        else:
            await message.channel.send(db.roast())
    elif u_msg.lower().startswith(';gif'):
        try:
            search_term = ' '.join(u_msg.split()[1:])
            giphy_api_key = 'ryGjA28KERjL9ILsNM1NY3LCPt7o8ryk'
            base_url = 'https://api.giphy.com/v1/gifs/search'
            params = {'api_key': giphy_api_key, 'q': search_term, 'limit': 1}
            response = requests.get(base_url, params=params)
            data = response.json()
            gif_url = data['data'][0]['url']
            await message.channel.send(gif_url)
        except Exception as e:
            pass
    elif u_msg.lower().startswith(';wish-buday'):
        mentioned_user = message.mentions[0] if message.mentions else None
        if mentioned_user:
            birthday_message = f"Happy Birthday {mentioned_user.mention}! {db.b_msg()}"
            await message.channel.send(birthday_message)
            await message.channel.send(db.b_gif())
        print(mentioned_user)
    elif u_msg.lower().startswith(';choose-from'):
        try:
            choices_str = ' '.join(u_msg.split()[1:])
            choices = [choice.strip(',') for choice in choices_str.split(',')]

            if len(choices) < 2:
                await message.channel.send("Please provide at least two choices.")
                return
            random_choice = random.choice(choices)
            await message.channel.send(f"My choice is: {random_choice}")
            print(u_msg)
        except Exception as e:
            pass

    elif any(word in u_msg for word in greet):
        await message.channel.send(random.choice(greet_res) + username)


client.run('MTAwOTQzMDY3NDA4MTU5NTQ0Mw.Gqtv7X.ahSQf0BYbvZNvqXnzz_U_gBQiIIBoMAhXalhUs')

