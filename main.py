# bot.py
import os
import random
import discord
from dotenv import load_dotenv

#loads the .env variables
load_dotenv()

#token is in .env so it is not visible easily
TOKEN = os.getenv('DISCORD_TOKEN')

# This bit just tells you the bot is running on the server
client = discord.Client()

# A function that rolls the d6s
def roll(num_of_dice: int, win_limit: int, speaker: str):
    wins = 0
    output_string = ''
    if num_of_dice == 0:
        return "nothing to roll."
    # Checks to see if the user has asked to roll too many dice
    # 50 is the limit that was chosen
    if int(num_of_dice) > 50:
        return "No more than 50 dice please"

    # This bit does the actual rolling of the dice
    for i in range(int(num_of_dice)):
        die_roll = random.randint(1, 6)
        output_string = output_string + " " + str(die_roll) + " "
        if die_roll >= win_limit:
            wins = wins + 1
    # Make the message that the bot will put in chat
    output_string = output_string + "\n" + speaker + " rolled " + str(
        wins) + " Success"

    # For fun this bit will show a skull if they roll 0 wins
    # And show a Scream face if they get all wins
    if wins == 0:
        output_string = output_string + "\n:skull:"

    if wins == num_of_dice:
        output_string = output_string + "\n:scream:"
    return '`' + output_string + '`'


def roll20(speaker:str):
    # Roll one D20
    output_string = str(random.randint(1, 20))
    # Additional messages if you roll a 1 or a 20
    if output_string == "1":
        output_string = output_string + "\n" + ":skull: Your doom is certain :skull:"
    if output_string == "20":
        output_string = output_string + "\n" + ":star: Fate is in you favor :star:"
    return "`"+ speaker +" d20 roll was " + output_string + "`"


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

    if message.author == client.user:
        #ignore messages from the bot
        return
    else:
        #get name of user from the returned author object
        speaker = repr(message.author.name)

    command = message.content.lower().strip()
    mes = command.split()

    # make sure parameters make sense
    # check for number of dice
    try:
        number_of_dice = int(mes[1])
    except Exception:
        # if the number of dice was not a number
        # or it wasn't there
        # or it didn't make sense for some other reason
        # just set the number of dice to 0
        number_of_dice = 0

    # check for different roll target
    try:
        target = int(mes[2])
    except Exception:
        # if the number of dice was not a number
        # or it wasn't there
        # or it didn't make sense for some other reason
        # just set the target to the default
        target = 4

    if mes[0].startswith('!help'):
        await message.channel.send("""` 
    Normal roll                                
      !roll how_many_dice  OR !r how_many_dice 
      ex) !roll 5                              
      ex) !r 6                                 
                                               
    roll with advantage                        
      !roll+ how_many_dice OR !r+ how_many_dice
      ex) !roll+ 4                             
      ex) !r+ 5                                
                                               
    roll one d20                               
      !roll20 or !r20                          `""")                     

    elif mes[0].startswith('!blanket'):
        for n in range(number_of_dice):
            await message.channel.send(
                str(n) + " : " + roll_blanket(number_of_dice))
    elif mes[0].startswith('!r'):
        # it's a roll of some kind

        if mes[0].endswith('+'):
            # roll with advantage
            # something about destiny points
            target = 3
            await message.channel.send(roll(number_of_dice, target, speaker))
        elif mes[0].endswith('20'):
            await message.channel.send(roll20(speaker))
        else:
            # normal roll
            await message.channel.send(roll(number_of_dice, target, speaker))


client.run(TOKEN)
