#Weather Extension Version 30.10.21
import discord
import random
import asyncio
import requests
import json
from discord.ext import commands
from discord.utils import get
from discord import utils

#Global Vars
api_key = '71c8139ee24f28d6e3e07e99bb8a1449'
base_url = "http://api.openweathermap.org/data/2.5/weather?&units=metric"

#Extension Class
class Weather(commands.Cog):
	#Initialisation
	def __init__(self, client):
		self.client = client
	#Weather Command
	@commands.command()
	async def weather(self, ctx, cityname):
		# Complete url
		complete_url = base_url + "&appid=" + api_key + "&q=" + cityname 
		# Get method of requests module 
		response = requests.get(complete_url) 
		# JSON to Python
		x = response.json() 
		if x["cod"] != "404": 
			# Main
			y = x["main"] 
			current_temperature = y["temp"] 
			current_pressure = y["pressure"] 
			current_humidiy = y["humidity"] 
			feels_like = y["feels_like"]
			#Weather
			z = x["weather"] 
			weather_description = z[0]["description"] 
			#Wind
			w = x["wind"]
			wind_speed = w["speed"]
			#Clouds
			c = x["clouds"]
			cloudiness = c["all"]
			#Embeds
			embed = discord.Embed(
				title = 'Weather Forecast',
				description = f'Weather in {cityname.title()}',
				color = 0x00ffff 
			) 
			urls = ['https://previews.123rf.com/images/yupiramos/yupiramos1611/yupiramos161103295/66580854-globe-earth-weather-meteorology-cloud-and-sun.jpg','https://previews.123rf.com/images/droidworks/droidworks1507/droidworks150700131/42031459-vector-earth-globe-clouds-and-sun-.jpg', 'https://previews.123rf.com/images/cornelius30/cornelius301010/cornelius30101000137/7975859-globe-with-the-sky-on-the-background.jpg', 'https://imgs.mi9.com/uploads/science-fiction/3831/photo-manipulation-of-02-sky-world-156-nature-and-city_1920x1200_58213.jpg']
			embed.set_thumbnail(url= random.choice(urls))
			embed.add_field(name='Temperature  :thermometer:', value= (f'{current_temperature}°C'), inline='True')
			embed.add_field(name='￶￵ ￶￵ ￶￵ Feels Like', value= (f'￶￵ ￶￵ ￶￵ {feels_like}°C'), inline='True')
			embed.add_field(name='Atmospheric Pressure  :arrow_double_down:', value= (f'{current_pressure} hPa'), inline='False')
			embed.add_field(name='Humidity  :sweat_drops:', value= (f'{current_humidiy}%'), inline='True')
			embed.add_field(name='￶￵ ￶￵ ￶￵ Wind Speed  :dash:', value= (f'￶￵ ￶￵ ￶￵ {wind_speed} meters/sec'), inline='True')
			embed.add_field(name='Clouds  :cloud:', value= (f'{cloudiness}'), inline='False')
			embed.add_field(name='Description', value= (f'{weather_description.title()}'), inline='False')
			#Send
			await ctx.send(embed=embed)
		else:
			await ctx.send('City Not Found')
#Setup Function
def setup(client):
	client.add_cog(Weather(client))