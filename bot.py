import discord
import json
import logging

logging.basicConfig(level=logging.INFO)


file1 = open("token.txt", "r")

TOKEN = file1.readlines()[0]


client = discord.Client()

## set up state variables
Locks = {}
house = {}
roles = {}
voice_channels = {}
text_channels = {}

serverLoaded = False 

commands = {}


ServerLoaded = False
botLoaded = False

@client.event
async def on_ready():
    global serverLoaded
    print('We have logged in as {0.user}'.format(client))
    house = loadJson('./scober.json')
    serverLoaded = False 



@client.event
async def on_voice_state_update(member, before, after):
    if (before.channel == after.channel):
        return
    else:
        await UserMovedVoice(member,before,after)
    

@client.event
async def on_message(message):
    await checkmessage(message)



async def checkmessage(message):
    global house
    global serverLoaded
    PlayerInput = message.content.lower()
    
    if message.author == client.user:
        return
    elif PlayerInput.startswith('$test'):
        await message.channel.send('im wokring')
    elif PlayerInput.startswith('$loadserver'):
        Log("load begin")
        house = loadJson('./scober.json')
        fetchRefrences(message.guild)
        Log("load finished")
        serverLoaded = True


    elif PlayerInput.startswith('$initserver 877807217'):
        Log("full init begin")
        house = loadJson('./scober.json')
        await initHouse(message.guild)
        Log("full init finished")
        serverLoaded = True


    elif not serverLoaded:
        Log("load begin")
        house = loadJson('./scober.json')
        fetchRefrences(message.guild)
        Log("load finished")
        serverLoaded = True
        await checkmessage(message)
    

    # Find current location
    elif PlayerInput.startswith('$location'):
        await message.channel.send('you are in the ' + message.channel.name)
        Log("User " + message.author.name + " in " + message.channel.name +  " : " + " has asked for their location with " + message.content )

    # Move command
    elif PlayerInput.startswith('$move'):
        command = getOption(PlayerInput, 5)
        print(message.author.name + " is trying to use command " + command)
        if (await isValidMove(message, command)):
            await MoveUser(message.author,message.channel.name,house['Rooms'][message.channel.name]['Moves'][command])
            Log("User " + message.author.name + " in " + message.channel.name +  " : " + "has moved to " + house['Rooms'][message.channel.name]['Moves'][command])
        else:
            Log("User " + message.author.name + " in " + message.channel.name +  " : " +  " has failed to move with command : " + command)

    # Basic rules blurb
    #elif PlayerInput.startswith('$help'):
    #    fetchRefrences(message.guild)
    #    Debug()

    #Allows a player to join the game by entering at the door step
    elif PlayerInput.startswith('$entergame'):
        await joinGame(message)
        Log("User " + message.author.name + " in " + message.channel.name +  " : " + " just joined the game")

    #Quits the game
    #elif PlayerInput.startswith('$quit'):
    #    await leaveGame(message)
    #    Log("User " + message.author.name + " in " + message.channel.name +  " : " + " just quit the game")

    elif PlayerInput.startswith('$knock'):
        await UnderConstruction(message,'$knock')
        Log("User " + message.author.name + " in " + message.channel.name +  " : " + " just called '$knock' with : " + message.content)



def Log(log):
    print(log)







# returns sends a message back which tells user the command is currently under constructure
async def UnderConstruction(message, command):
    await message.channel.send("sorry "+ command + " is currently under construction")








# removes a player from the game returning them to the waiting room
async def leaveGame(message):
    if roles["In "+ message.channel.name] in message.author.roles:
        await message.author.remove_roles(roles["In "+message.channel.name])








# loads in the house JSfile based on the filename
def loadJson(filename):
    global house
    with open(filename) as f:
        house = json.load(f)
    return house








# strips and cleans an input of its command returning only the option for such command
def getOption(message, start):
    command = message[start:]
    command = command.replace(" ","")
    command = command.lower()
    return command







# set up dict refrencces for easy refrence to server values  
def fetchRefrences(guild):
    # set up role dict for easy refrence
    global roles    
    for role in guild.roles:
        roles[role.name] = role
    
    # set up tc dict for easy refrence
    global text_channels
    for channel in guild.text_channels:
        text_channels[channel.name] = channel
    
    # set up vc dict for easy refrence
    global voice_channels
    for channel in guild.voice_channels:
        voice_channels[channel.name] = channel
    







# Checks that user can make the move they are attempting
async def isValidMove(message, command):
    return command in house["Rooms"][message.channel.name]["Moves"]








# Moves a user from room named chFrom to room named chTo 
async def MoveUser(member, chFrom, chTo):
    if (roles["In "+chFrom]) in member.roles:
        await member.remove_roles((roles["In "+chFrom]))
    await member.add_roles((roles["In "+chTo]))

    if (member.voice.channel != None):
        await member.move_to(voice_channels[chTo])
        
    await playerMovedIn(member, text_channels[chTo])



async def UserMovedVoice(member, chFrom, chTo):
    #print("User " + member.name + " : VC status changed from" +  chFrom.channel + " to " + chTo.channel)

        
    if (chTo.channel != None):

        if (chFrom.channel != None):
            print ("User " + member.name + " is trying to leave " +  chFrom.channel.name)
            await member.remove_roles((roles["In "+chFrom.channel.name]))
            print("User " + member.name + " has left " +  chFrom.channel.name)
            print ("User " + member.name + " is trying to join " +  chTo.channel.name)           
            await member.add_roles((roles["In "+chTo.channel.name]))
            print("User " + member.name + " has joined " +  chTo.channel.name)
        else:
            #updatedMember = await chTo.channel.guild.get_member(member.id)
            for role in member.roles:
                if role.name.startswith("In "):
                    await member.remove_roles(role)
            print ("User " + member.name + " is trying to join " +  chTo.channel.name)           
            await member.add_roles((roles["In "+chTo.channel.name]))
            print("User " + member.name + " has joined " +  chTo.channel.name)







# adds a playe to game by giving them the in doorstep role and the in game role
async def joinGame(message):
    await message.author.add_roles((roles["In doorstep"]))
    #await message.author.add_roles((roles["In game"]))
    #await text_channels["doorstep"].send(house["Rooms"]["doorstep"]["Discription"])







## init House creates all the required roles and text chats for the house to be used
async def initHouse(guild):
    fetchRefrences(guild)
    for key in house["Rooms"]:
        print("evaling  " + key)

        # does role exist?
        if "In " + key in roles:
            role = roles["In "+ key]
        else:
            print("role for " + key + " dosn't exist making one")
            role = await guild.create_role(name="In " + key,  reason="initing house")
        
        # set up overwrites
        overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                role: discord.PermissionOverwrite(view_channel=True)
        }

        # does tc exist?
        if key.replace(" ","-") in text_channels:
            pass
        else:
            print("text channel for " + key + " dosn't exist making one")
            await guild.create_text_channel(name=key,overwrites=overwrites)
        # does vc exist?
        if key in voice_channels:
            pass
        else:
            print("voice channel for " + key + " dosn't exist making one")
            await guild.create_voice_channel(name=key,overwrites=overwrites)

    fetchRefrences(guild)

    for key in house["Rooms"]:
        print("key = " + key)
        for doorKey in house["Rooms"][key]["Moves"]:
            print("doorKey = " + doorKey)
            if "In "+ key in voice_channels[house["Rooms"][key]["Moves"][doorKey]].overwrites:
                print("Overrides for " + doorKey + " exist skipping")
            else:
                print("Overrides for " + doorKey + " do not exist making one")
                await voice_channels[house["Rooms"][key]["Moves"][doorKey]].set_permissions(roles["In " + key],view_channel=True)
    
    #role = await guild.create_role(name="In Game",  reason="initing house")
    #await guild.create_text_channel(name="waiting-room",overwrites=overwrites)







# prints the discription of a room as well as let players know when a new player has entered the room
async def playerMovedIn(member, room):
    await room.send(member.display_name + " walks in to the room, you can't tell which door they came from maybe pester Seaney about this")
    await room.send(house["Rooms"][room.name]["Discription"])



async def clean(guild):
    for role in guild.roles:
        if (role.name.startswith("In")):
            print("removing role : " + role.name)
            await role.delete()
    for channel in guild.channels:
        print("removing channel : " + role.name)
        await channel.delete()
    await guild.create_text_channel(name="WaitingRoom")

async def cleanRebuild():

    Log("cleaning server start")

    for role in guild.roles:
        if (role.name.startswith("In")):
            print("removing role : " + role.name)
            await role.delete()
    for channel in guild.channels:
        print("removing channel : " + role.name)
        await channel.delete()

    Log("cleaning server end")
    Log("full init end")
    house = loadJson('./house1.json')
    await initHouse(message.guild)
    Log("full init finished")


def Debug():
    print ("Roles ")
    print(roles)
    print ("TextChannels ")
    print(text_channels)
    print ("VoiceChannels ")
    print(voice_channels)
    print ("House total JSon dump ")
    print(house)

client.run(TOKEN)