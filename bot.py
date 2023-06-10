from discord.ext import commands
import discord
import socket
import time
import os

# Read token from text file
file = open('./discord_token.txt', 'r')
token = file.readline()
file.close()

# Init discord bot
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

# Init variables for the program

@client.event
async def on_ready():
    print('Shine.AI is not online!')
    await client.change_presence(activity=discord.Game(name='currently not hunting'))
    
@client.command('init_hunt')
async def init_hunt(ctx):
    await ctx.reply('Check the host device for more information!')
    print('-------------------------------------------------------------')
    hunt = input('What Pokemon is being hunted? ')
    game = input('What game are you hunting in? ')
    method = input('What method are you using for this hunt? ')
    encounters = int(input('How many encounters are you at? '))
    phase = int(input('What phase of the hunt is this? '))
    print(f'This hunt has been initialized to be updated in #{ctx.message.channel}')
    print('-------------------------------------------------------------')
    channel = client.get_channel(1108978958814425098)

    # Connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 5000))
    # Init data on the server
    s.send(f"SA.util.hunt {hunt}\n".encode())
    s.send(f"SA.util.game {game}\n".encode())
    s.send(f"SA.util.method {method}\n".encode())
    s.send(f"SA.util.encounters {encounters}\n".encode())
    s.send(f"SA.util.phase {phase}\n".encode())

    await ctx.reply(f'Hunt for {hunt} in {game} using {method} initialized at {encounters} encounters and phase {phase}\nHunt will be updated in this channel')
    await client.change_presence(activity=discord.Game(name=f'currently hunting {hunt} | {encounters} encounters'))

    s.send(b"SA.b.connect\n")
    s.send(b"SA.h.status\n")
    while s.recv(2048).decode() != "True":
        print("Waiting for hunt script to connect...")
        try:
            await channel.send("Waiting for hunt script to connect...")
        except:
            pass
        time.sleep(1)
        s.send(b"SA.h.status\n")
    print("Connection established beginning updates")

    # Init hunt
    s.send(b"SA.e.check\n")
    hunting = True
    while hunting:

        # Wait for hunt script to alert of an image
        s.send(b"SA.ss.exists\n")
        while s.recv(2048).decode() != "True":
            print("Waiting for a screenshot...")
            try:
                await channel.send("Waiting for screenshot...")
            except:
                pass
            time.sleep(1)
            s.send(b"SA.ss.exists\n")
        print("Screenshot recieved updating user")
        
        # Update hunt and user
        encounters += 1
        s.send(b"SA.sh.found\n")
        if s.recv(2048).decode() == "Found":
            try:  
                await ctx.reply(f"Encounter {encounters} is shiny!")
            except:
                pass
            hunting = False
            try:
                await client.change_presence(activity=discord.Game(name='currently not hunting'))
            except:
                pass
        else:
            try:
                await ctx.send(f"Encounter {encounters} is not shiny...")
                await client.change_presence(activity=discord.Game(name=f'currently hunting {hunt} | {encounters} encounters'))
            except:
                pass
        try:
            await ctx.send(file=discord.File('./temp.png'))
            print("User updated")
        except:
            pass

        s.send(b"SA.ss.del\n")
        s.send(b"SA.e.incr\n")

    s.send(b"SA.util.log\n")
    try:
        await ctx.reply(f"The hunt has been completed after {encounters} encounters")
    except:
        pass
    print("The hunt has been completed.")
    s.send(b"SA.util.disconnect\n")
    s.close()

client.run(token)