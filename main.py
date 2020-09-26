import os
import io
import aiohttp
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import json
# from threading import hread

TOKEN = 'NzU5NDI4OTczNjgyNzUzNTg3.X29XWA.F5HXTyoOi20igCaeXqwxy5VyGhs'
dictn = {}
random_search_done = False
channel_id = 759432390044418058



client = commands.Bot(command_prefix=".")

@client.event
async def on_ready():
	print("BOT CONNECTED")


@client.command()
async def introduce(ctx):
	global channel_id
	if ctx.channel.id != channel_id:
		await ctx.send("You can only use this commnad from gimme_a_waifu channel. Don't spam this here to avoid a ban")
		return
	message = f"""konnichiwa {ctx.message.author} aniki, Boku wa GimmeALove booto. I'm currently under development,
			    so forgive me if anything goes wrong.
				Gimme a pat hehe, that will cheer me a lot.
				Commands currently available : 
				1. .introduce - I'll introduce my self
				2. .ping - A pong reply with a ping
				3. .random - spawns a random waifu
				4. .catch <name> - if you got the correct name, waifu is yours. Not actually.
			Onii-chan is working really hard(and smart huhu...) to make me even awesome.
			So if you got any suggestion that would make me even better or you spot a bug then 
			don't forget to mention him at @pixalquarks. Although Onii-chan is Baka(big one), he'll still
			try his best over your suggestions and ideas.
			Onii-chan calls me Aski, you can call me that too, I you want, although it won't do anything.

			Have a nice day and keep being awesome {ctx.message.author} aniki.
			Ja Matane."""
	await ctx.send(message)


@client.command(aliases=["PING","Ping"])
async def ping(ctx):
	global channel_id
	if ctx.channel.id != channel_id:
		await ctx.send("You can only use this commnad from gimme_a_waifu channel. Don't spam this here to avoid a ban")
		return
	channel = client.get_channel(channel_id)
	await channel.send(f"PONG! {round(client.latency * 1000)} ms")

@client.command(aliases=["Random"])
async def random(ctx):
	global channel_id
	if ctx.channel.id != channel_id:
		await ctx.send("You can only use this commnad from gimme_a_waifu channel. Don't spam this here to avoid a ban")
		return
	global dictn
	global random_search_done
	random_search_done = True
	async with aiohttp.ClientSession() as session:
		async with session.get("https://mywaifulist.moe/random") as resp:
			if resp.status != 200:
				return await ctx.send('Could not your waifu senpai. Maybe try again')
			soup = BeautifulSoup(await resp.text(), 'html.parser')
			dictn = json.loads(soup.find('script', type="application/ld+json").string)
			async with session.get(dictn["image"]) as _resp:
				if resp.status != 200:
					return await channel.send('Could not download file...')
				data = io.BytesIO(await _resp.read())
				channel = client.get_channel(channel_id)
				await channel.send(file=discord.File(data, 'cool_image.png'))

@client.command()
async def catch(ctx, *, name):
	global channel_id
	if ctx.channel.id != channel_id:
		await ctx.send("You can only use this commnad from gimme_a_waifu channel. Don't spam this here to avoid a ban")
		return
	if name == None:
		await ctx.send("Enter a valid name")
		return
	global dictn
	stringh = ""
	author = ctx.message.author
	name_ = dictn["name"]
	if name.lower() == name_.lower():
		stringh = f"Yay! {str(author)} just made {name_} his waifu"
	else:
		stringh = f"{str(author)},That's the wrong answer Baka"
	channel = client.get_channel(channel_id)
	await channel.send(stringh)

client.run(TOKEN)