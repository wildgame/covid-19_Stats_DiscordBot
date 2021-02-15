import discord
import os
from discord.ext import commands

token = 'NjkzODQ2ODQ3OTk4OTE4NjU3.XoDCog.vINX8PUvsGdB7QpCTeH_Rs6djG4'

bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready():
    print('Bot Online')

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if(filename.endswith('.py')):
        bot.load_extension(f'cogs.{filename[:-3]}')

#ctx = context, passed automatically

bot.run(token)