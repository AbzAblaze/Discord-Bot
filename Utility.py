#Utility Extension Version 31.10.21
import discord
import random
import asyncio
from discord.ext import commands
from discord.utils import get
from discord import utils
from datetime import timedelta, datetime

#Extension Class
class Utility(commands.Cog):
	#Initialisation
	def __init__(self, client):
		self.client = client
	#On_Ready Event
	@commands.Cog.listener()
	async def on_ready(self):
		global usernamelist
		global useridlist
		global allowedUsers 
		global sandlandid    
		global yellowstoneid  
		global testserverid   
		allowedUsers = [505498222534328358]
		sandland     = self.client.get_guild(662755798568665089)
		yellowstone  = self.client.get_guild(890767427892281445)
		testserver   = self.client.get_guild(767432419346743329)
		#Collect Users
		usernamelist = []
		useridlist = []
		for member in sandland.members:
			usernamelist.append(member.name)
			useridlist.append(member.id)
		for member in yellowstone.members:
			usernamelist.append(member.name)
			useridlist.append(member.id)
		#Ready Message
		print('Starbot is ready!')
	#Message Event
	@commands.Cog.listener()
	async def on_message(self, message):
		testserver   = self.client.get_guild(767432419346743329)		
		#Self Avatar 
		if message.content == ';avatar':
			show_avatar = discord.Embed(title= f'Avatar for {message.author.name}', color = discord.Color.dark_blue())
			show_avatar.set_image(url= '{}'.format(message.author.avatar_url))
			await message.channel.send(embed=show_avatar)
		#Delete Unused Colors
		for role in testserver.roles:
			await asyncio.sleep(3)
			if role.name.startswith('Colour_Role') and len(role.members) == 0:
				try:
					await role.delete()
				except:
					pass
	#8 Ball Command
	@commands.command(aliases = ['8ball'])
	async def eight_ball(self, ctx, *, question):
		responses = ['As I see it, yes.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'No way in hell', 'Concentrate and ask again.', 'It is certain.', 'Dont count on it', 'It is decidedly so.']
		await ctx.send(f'{random.choice(responses)}')
	#DM Command
	@commands.command(aliases = ['say'])
	async def dm(self, ctx, name, *,  secretmessage):
		if name in usernamelist and ctx.author.id in allowedUsers:
			user = self.client.get_user(useridlist[usernamelist.index(name)])
			await user.send(secretmessage)
		else:
			await ctx.send("**Noob**. You can't use this command. <:smugqua:705951060656652340>")
	#Identify Command
	@commands.command(aliases = ['check'])
	async def identify(self, ctx, cid):
		channel = self.client.get_channel(int(cid))
		user    = self.client.get_user(int(cid))
		if user:
			await ctx.send(f'{user.name}')
		elif channel:
			await ctx.send(f'{channel.guild.name}: {channel.name}')
		else:
			 print('None...')
	#Avatar Command
	@commands.command()
	async def avatar(self, ctx, member: discord.Member):
		try:
			show_avatar = discord.Embed(title= f'Avatar for {member}', color = discord.Color.dark_blue())
			show_avatar.set_image(url= '{}'.format(member.avatar_url))
			await ctx.send(embed=show_avatar)
		except:
			pass
	#Purge Command
	@commands.command()
	async def purge(self, ctx, amount: int):
		if ctx.author.id in allowedUsers:
			await ctx.message.delete()
			await ctx.channel.purge(limit=amount)
			await ctx.send(f'Purged {amount} messages...', delete_after= 0.5)
		else:
			await ctx.send("**Noob**. You can't use this command. <:smugqua:705951060656652340>")
	#Echo Command
	@commands.command()
	async def echo(self, ctx, *, message):
		if ctx.author.id in allowedUsers:
			await ctx.message.delete()
			await ctx.send(message)
			if message == 'ping':
				await ping(ctx)
		else:
			await ctx.send("**Noob**. You can't use this command. <:smugqua:705951060656652340>")
	#Channel Send
	@commands.command()
	async def send(self, ctx, channelid, *,  thing):
		channel = self.client.get_channel(channelid)
		if ctx.author.id in allowedUsers:
			await channel.send(thing)
		else:
			await ctx.send("**Noob**. You can't use this command. <:smugqua:705951060656652340>")
	#Colour Roles
	@commands.command()
	async def colour(self, ctx, hexa_value):
		hexa_colour= int(hexa_value, 16)
		colour_role = discord.utils.get(ctx.guild.roles, name=f'Colour_Role: {hexa_value.upper()}')
		if colour_role is None:
			newcolour_role = await ctx.guild.create_role(name=f'Colour_Role: {hexa_value.upper()}', colour=discord.Colour(hexa_colour))
			await ctx.author.add_roles(newcolour_role)
			await ctx.send('Colour Added!')
		else:
			await ctx.author.add_roles(colour_role)
			await ctx.send('Colour Added!')
	#Add Colours
	@commands.command(aliases = ['addcolour', 'addcolor'])
	async def add_colour(self, ctx, hexa_value, member: discord.Member):
		hexa_colour= int(hexa_value, 16)
		colour_role = discord.utils.get(ctx.guild.roles, name=f'Colour_Role: {hexa_value.upper()}')
		if colour_role is None:
			newcolour_role = await ctx.guild.create_role(name=f'Colour_Role: {hexa_value.upper()}', colour=discord.Colour(hexa_colour))
			await member.add_roles(newcolour_role)
			await ctx.send(f'Colour Added to **{member.name}**!')
		else:
			await member.add_roles(colour_role)
			await ctx.send(f'Colour Added to **{member.name}**!')
	#Rumble Command
	@commands.command()
	async def rumble(self, ctx, member: discord.Member, countdown= 10):
		if ctx.author.id in allowedUsers: 
			await ctx.send(f"**{member.name} WILL BE RUMBLED. IT CAN'T BE STOPPED ANYMORE**".upper())
			time = int(countdown)
			await ctx.send('https://media4.giphy.com/media/PWktVcakHgf5emnk0d/giphy.gif')
			while time >= 0:
				botmessage = await ctx.send(time)
				await asyncio.sleep(1)
				time -= 1
				await botmessage.delete()
			try:
				await member.kick()
				await ctx.send(f'**Rumbled {member.name}**')
			except:
				await ctx.send("**No Perms. Epic Fail <:RelatableLaugh:682345860700307480>**")
		else:
			await ctx.send("**Noob**. You can't use this command. <:smugqua:705951060656652340>")
	#Archive Command
	@commands.command()
	async def archive(self, ctx, userid = 737749343334826054):
		#If Reply 
		if ctx.message.reference and ctx.author.id in allowedUsers:
			user = self.client.get_user(int(userid))
			spitchannel = self.client.get_channel(903350231389847572)
			referredmessageid = ctx.message.reference.message_id
			referredmessage = await ctx.message.channel.fetch_message(referredmessageid)
			#If Image
			if referredmessage.attachments:
				attachment = referredmessage.attachments[0]
				await spitchannel.send(attachment.url)
			else:
				await ctx.send('Not an Image.')
		elif ctx.author.id not in allowedUsers:
			await ctx.send("**Noob**. You can't use this command. <:smugqua:705951060656652340>")
		else:
			await ctx.send('No Reference Message.')
#Setup Function
def setup(client):
	client.add_cog(Utility(client))