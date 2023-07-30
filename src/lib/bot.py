from discord.ext import commands
import discord
import socket
import time
import os

def run_discord_bot(file, settings, exit_event, gui):
# Read token from text file
    token = settings.hunt['discord_token']
    path = file.path
    while path.find('/') != -1:
        path = path[path.find('/') + 1:]
    path = path[:path.find('.')]

    if settings.hunt['spam_channel'] != 'Not Set':
        spam_channel = int(settings.hunt['spam_channel'])
    else: spam_channel = None

    # Init discord bot
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix='!', intents=intents)

    # Init variables for the program

    @client.event
    async def on_ready():
        print('Shine.AI is not online!')
        await client.change_presence(activity=discord.Game(name='currently not hunting'))
        if exit_event.is_set():
            exit()

    @client.command('init_hunt')
    async def init_hunt(ctx):
        hunt = file.hunt
        game = file.game
        method = file.method
        encounters = file.encounters
        phase = file.phase
        print(f'This hunt has been initialized to be updated in #{ctx.message.channel}')
        if spam_channel != None:
            channel = client.get_channel(spam_channel)
        else: channel = None

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
                if channel != None:
                    await channel.send("Waiting for hunt script to connect...")
            except:
                pass
            time.sleep(1)
            s.send(b"SA.h.status\n")
            if exit_event.is_set():
                exit()
        print("Connection established beginning updates")

        # Init hunt
        hunting = True
        while hunting:

            # Wait for hunt script to alert of an image
            s.send(b"SA.ss.exists\n")
            while s.recv(2048).decode() != "True":
                print("Waiting for a screenshot...")
                try:
                    if channel != None:
                        await channel.send("Waiting for screenshot...")
                except:
                    pass
                time.sleep(1)
                s.send(b"SA.ss.exists\n")
                if exit_event.is_set():
                    exit()
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
                await ctx.send(file=discord.File(f'data/{path}/current.png'))
                print("User updated")
            except:
                pass
            
            s.send(b"SA.ss.del\n")
            s.send(b"SA.e.incr\n")
            s.send(b"SA.e.check\n")
            update = s.recv(2048).decode()
            gui.update_encounters(update)

        try:
            await ctx.reply(f"The hunt has been completed after {encounters} encounters")
        except:
            pass
        print("The hunt has been completed.")
        s.send(b"SA.util.disconnect\n")
        s.close()
        while True:                    
            if channel != None:
                await channel.send("Waiting for confirmation...")
            if exit_event.is_set():
                break

    if settings.hunt['use_discord'] == 'True':
        client.run(token)
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((socket.gethostname(), 5000))
        while True:
            s.send(b"SA.ss.exists\n")
            while s.recv(2048).decode() != "True":
                print("Waiting for a screenshot...")
                time.sleep(1)
                s.send(b"SA.ss.exists\n")
                if exit_event.is_set():
                    exit()
            print('Screenshot recieved')
            s.send(b"SA.sh.found\n")
            if s.recv(2048).decode() == "Found":
                break
            s.send(b"SA.ss.del\n")
            s.send(b"SA.e.incr\n")
            s.send(b"SA.e.check\n")
            update = s.recv(2048).decode()
            gui.update_encounters(update)
        print("The hunt has been completed.")
        s.send(b"SA.util.disconnect\n")
        s.close()
        gui.shiny_found()
