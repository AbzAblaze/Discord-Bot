#Mainbot Version 03.11.21
import discord
import os
import json
from discord.ext import commands
import asyncpg
from asyncpg.pool import create_pool

#Intents
intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix = ";", intents = intents, help_command = None) 

#Configuration
if os.path.exists("./cogs/Configs.json"):
	with open("./cogs/Configs.json") as file:
		config = json.load(file)
		token = config["token"]
		sqlpword = config["sqlpword"]

#Database
async def create_db_pool():
	client.pg_con = await asyncpg.create_pool(database='Starbot',user='postgres',password=sqlpword)

#Load Cogs
@client.command()
async def load(ctx, extension):
	client.load_extension(f'cogs.{extension}')
	await ctx.send(f'{extension} loaded...')

#Unload Cogs
@client.command()
async def unload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')
	await ctx.send(f'{extension} unloaded...')

#Auto-Load Cogs
for filename in os.listdir('./cogs'):
	ignore_files = ['Wiretap.py', 'Chat.py']
	if filename.endswith('.py') and filename not in ignore_files:
		client.load_extension(f'cogs.{filename[:-3]}')

#Run Bot
client.loop.run_until_complete(create_db_pool())		
client.run(token)
