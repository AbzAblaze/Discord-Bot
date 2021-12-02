#Economy Extension Version 03.11.21
import discord
import random
import asyncio
from discord.ext import commands
from discord.utils import get
from discord import utils
import asyncpg
from asyncpg.pool import create_pool

#Extension Class
class Economy(commands.Cog):
	#Initialisation
	def __init__(self, client):
		self.client = client
	#Ready Event
	@commands.Cog.listener()
	async def on_ready(self):
		#Backup for Database
		await self.client.pg_con.execute("CREATE TABLE IF NOT EXISTS Economy (userid BIGINT NOT NULL, score BIGINT)")
		await self.client.pg_con.execute("ALTER TABLE Economy ADD COLUMN IF NOT EXISTS userid BIGINT NOT NULL")
		await self.client.pg_con.execute("ALTER TABLE Economy ADD COLUMN IF NOT EXISTS score BIGINT")
  	#Error Event
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			message = f'You\'re on cooldown. Please try again in **{int(error.retry_after)}** seconds.'
			await ctx.send(message)
  #Database Functions	
	#Add Score
	async def add(self, id, amount):
		balance = await self.client.pg_con.fetchrow("SELECT score FROM Economy WHERE userid = $1",id)
		await self.client.pg_con.execute("UPDATE Economy SET score = $1 WHERE userid = $2", balance[0]+amount, id)
	#Subtract Score
	async def subtract(self, id, amount):
		balance = await self.client.pg_con.fetchrow("SELECT score FROM Economy WHERE userid = $1",id)
		await self.client.pg_con.execute("UPDATE Economy SET score = $1 WHERE userid = $2", balance[0]-amount, id)
	#Check User
	async def check(self, id):
		user = await self.client.pg_con.fetchrow("SELECT * FROM Economy WHERE userid = $1", id)
		#If User Is Not In Database
		if user is None:
			await self.client.pg_con.execute("INSERT INTO Economy (userid, score) VALUES ($1, $2)", id, 0)
	#Get Balance
	async def balance(self, id):
		balance = await self.client.pg_con.fetchrow("SELECT score FROM Economy WHERE userid = $1",id)
		return balance[0]
	#Tops
	async def top(self):
		global topidlist
		global topscorelist
		topidlist = []
		topscorelist = []
		#Fetch all the IDs
		topids_record    = await self.client.pg_con.fetch("SELECT userid FROM Economy ORDER BY score DESC NULLS LAST")
		#Appends Each User ID
		for row in topids_record:
			for topid in row:
				topidlist.append(topid)
		#Fetch all the Scores
		topscores_record = await self.client.pg_con.fetch("SELECT score FROM Economy ORDER BY score DESC NULLS LAST")
		#Appends Each Users Score
		for row in topscores_record:
			for topscore in row:
				topscorelist.append(topscore)
  #Economy Functions		
	#Roll Command
	@commands.command()
	@commands.cooldown(2,600, type= commands.BucketType.user)
	async def roll(self, ctx):
		luck = ['add', 'add', 'add', 'subtract']
		await self.check(ctx.author.id)
		random_number = random.randint(1,100)
		if random.choice(luck) == 'add':
			await ctx.send(':game_die: Rolling the die...')
			await asyncio.sleep(2)
			await self.add(ctx.author.id, random_number)
			await ctx.send(f':coin: You have gained **{random_number}** coins! :coin: ')
		else:
			await ctx.send(':game_die: Rolling the die...')
			await asyncio.sleep(1)
			await self.subtract(ctx.author.id, random_number)
			await ctx.send(f':skull: You have lost **{random_number}** coins :skull: ')
	#Check Balance
	@commands.command(aliases = ['mybal'])
	async def my_bal(self, ctx):
		await self.check(ctx.author.id)
		bal = await self.balance(ctx.author.id)
		await ctx.send(f':bank: Your balance is: **{bal}** :bank:')
	#Check Someone's Balance
	@commands.command()
	async def bal(self, ctx, member: discord.Member):
		try:
			bal = await self.balance(member.id)
			await ctx.send(f':bank: **{member.name}\'s** balance is: **{bal}** :bank:')
		except:
			await ctx.send(f'**{member.name}\'s** balance could not be found.')
	#Leaderboard
	@commands.command()
	async def lb(self, ctx):
		await self.top()
		lbembed = discord.Embed(title = ":coin: Leaderboard :coin:", color = discord.Color.gold())
		x = 0
		lbidlist = ''
		lbscorelist = ''
		while x < len(topidlist):
			player =  self.client.get_user(topidlist[x]) 
			score  = str(topscorelist[x])
			lbidlist = lbidlist + player.mention + '\n'
			lbscorelist = lbscorelist + score + '\n'
			x = x + 1
		lbembed.add_field(name = 'Players:', value = lbidlist, inline = True)
		lbembed.add_field(name = 'Balance:', value = f'{lbscorelist}', inline = True)
		await ctx.send(embed = lbembed)
#Setup Function
def setup(client):
	client.add_cog(Economy(client))
