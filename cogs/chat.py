#Chat Extension Version 14.11.21
import discord
import random
import asyncio
from discord.ext import commands
from neuralintents import GenericAssistant
from discord.utils import get
from discord import utils
from datetime import timedelta, datetime

#Chatbot
chatbot = GenericAssistant('./cogs/Intents.json')
chatbot.train_model()
chatbot.save_model()

#Extension Class
class Chat(commands.Cog):
	#Initialisation
	def __init__(self, client):
		self.client = client
	#Chat Event
	@commands.Cog.listener()
	async def on_message(self, message):
		testserver   = self.client.get_guild(##################)
		if message.channel.id == ##################:
			trigger = message.content.lower()
			if message.author == self.client.user:
				pass
			if trigger.startswith('starbot'):
				response = chatbot.request(message.content)
				await message.channel.send(response)
#Setup Function
def setup(client):
	client.add_cog(Chat(client))
