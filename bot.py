from discord.ext import commands
import discord

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
    encounters = int(input('How many encounters are you at? '))
    phase = int(input('What phase of the hunt is this? '))
    print(f'This hunt has been initialized to be updated in #{ctx.message.channel}')
    print('-------------------------------------------------------------')

    await client.change_presence(activity=discord.Game(name=f'currently hunting {hunt} | {encounters} encounters'))
    await ctx.reply(f'Hunt initialized | Hunt - {hunt} | Encounters - {encounters} | Phase - {phase}\nHunt will be updated in this channel')

client.run("token")
