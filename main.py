import os
import io
import aiohttp
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import json
from NhentaiManager import NHentaiOP as Nhentai
import configs
from random import choice
# from threading import hread

TOKEN = str(os.environ.get("TOKEN"))
#TOKEN = "NzU5NDI4OTczNjgyNzUzNTg3.X29XWA.OXjf69RqIYGqFCg6Gg-nQm9sYIQ"
dictn = {}
random_search_done = False
channel_id_waifu = None
channel_id_doujins = None
nhentai = Nhentai()
doujin = {}
counter = 0
read_ = False
disable_doujin = False
current_doujin_manager = 0



client = commands.Bot(command_prefix=".")

@client.event
async def on_ready():
	print("BOT CONNECTED")

@client.command()
async def setchannel(ctx,name:str):
	global channel_id_waifu
	global channel_id_doujins
	if check_authority(ctx):
		if name == 'waifu':
			channel_id_waifu = ctx.channel.id
		elif name == 'doujin':
			channel_id_doujins = ctx.channel.id
		await ctx.send("Done")

@client.command()
async def removechannel(ctx,name:str):
	global channel_id_doujins
	global channel_id_waifu
	if check_authority(ctx):
		if name == 'waifu':
			channel_id_waifu = None
		elif name == 'doujin':
			channel_id_doujins = None

def isOnii_chan(ctx):
	if str(ctx.message.author) in configs.onii_chan_id:
		return True
	return False

@client.command()
async def introduce(ctx):
	if not isChannelNormal(ctx):
		return await ctx.send("You can only use this commnad from gimme_a_waifu channel. Don't spam this here to avoid a ban")
	message = f"""konnichiwa {ctx.message.author} aniki, Boku wa GimmeALove booto. I'm currently under development,
			    so forgive me if anything goes wrong.
				Gimme a pat hehe, that will cheer me a lot.
				Use commnad $help to know all of my commands.
			Onii-chan is working really hard(and smart huhu...) to make me even awesome.
			So if you got any suggestion that would make me even better or you spot a bug then 
			don't forget to mention him at @pixalquarks. Although Onii-chan is Baka(big one), he'll still
			try his best over your suggestions and ideas.
			Onii-chan calls me Aski, you can call me that too, I you want, although it won't do anything.

			Have a nice day and keep being awesome {ctx.message.author} aniki.
			Ja Matane."""
	await ctx.send(message)

@client.command(aliases=["ELP",'Elp'])
async def elp(ctx):
	if not isChannelNormal(ctx):
		return await ctx.send("You cannot use this command from this channel")
	message = f"""Yo, {ctx.message.author} aniki, Currently I support these feautes:
				1. Waifu  Commands availabe:
					a. $random/Random used to spawn a random waifu
					b. $catch <name> used to catch the spawned waifu
				2. Doujin Commands available:
					a. $getDoujin <id> to get the doujin
					b. $read to read the searched doujin
					c. $/next|previous|restart|delete do just what they sounds like. Can only be used by DJ and mods
				3. Onii-chan exclusive commands:
					a.$imouto|daisuki|special|onii-chan-song last 2 are only exlusive for my kawaii and super awesome onii-chan"""
	await ctx.send(message)	

def check_authority(ctx):
	for i in ctx.message.author.roles:
		if i.name == 'Mods':
			return True
	return False

def isChannelNormal(ctx):
	global channel_id_waifu
	if ctx.channel.id == channel_id_waifu:
		return True
	return False

def isChannelDoujin(ctx):
	global channel_id_doujins
	if ctx.channel.id == channel_id_doujins:
		return True
	return False

@client.command(aliases=["PING","Ping"])
async def ping(ctx):
	if not isChannelNormal(ctx):
		return await ctx.send("You can only use this commnad from gimme_a_waifu channel. Don't spam this here to avoid a ban")
	await ctx.send(f"PONG! {round(client.latency * 1000)} ms")

@client.command(aliases=["Random"])
async def random(ctx):
	if not isChannelNormal(ctx):
		return await ctx.send("You can only use this commnad from gimme_a_waifu channel. Don't spam this here to avoid a ban")

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
					return await ctx.send('Could not download file...')
				with  io.BytesIO(await _resp.read()) as data:
					await ctx.send(file=discord.File(data, 'cool_image.png'))

@client.command()
async def catch(ctx, *, name):
	if not isChannelNormal(ctx):
		return await ctx.send("You can only use this commnad from gimme_a_waifu channel. Don't spam this here to avoid a ban")
		
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
	await ctx.send(stringh)

@client.command(aliases=["toggle"])
async def toggle_doujin(ctx):
	if not isChannelDoujin(ctx):
		return await ctx.send("You cannot use this command from this channel. Only from Doujin channel")
	if not check_authority(ctx):
		return await ("You are not eligible for this command. Only mods can config this")
	global disable_doujin
	global doujin
	doujin = {}
	disable_doujin = not disable_doujin
	return await ctx.send(f"Doujin disable mode set to {disable_doujin}")

@client.command(aliases=["find"])
async def getDoujin(ctx, id:int):
	if not isChannelDoujin(ctx):
		return await ctx.send("You cannot use this command from this channel. Only from Doujin channel")
	global disable_doujin
	if disable_doujin:
		return await ctx.send("Seems like mods have disable doujin on this channel. Try asking them for the permissions")
	global doujin
	global counter
	global current_doujin_manager
	current_doujin_manager = ctx.message.author.id
	counter = 0
	doujin = await nhentai._get_doujin(id=str(id))
	if doujin == None:
		await ctx.send("Oops couldn't get the doujin")
		return
	else:
		message = f"""Name     : {doujin["title"][0]}
					  Author   : {doujin["artists"][0]}
					  Language : {doujin["languages"]}
					  Pages    : {doujin["pages"][0]}
					  URL      : {doujin["url"]}"""
		with io.BytesIO(doujin["cover"]) as data:
			await ctx.send(message,file=discord.File(data, 'cover_img.jpeg'))

@client.command()
async def read(ctx):
	if not isChannelDoujin(ctx):
		return await ctx.send("You cannot use this command from this channel. Only from Doujin channel")
	global read_
	global doujin
	if not doujin:
		await ctx.send("Please search a doujin first. Use command $getDoujin <id> to search for one")
		return
	read_ = True
	await ctx.send(f"Entered the reading mode. {ctx.message.author} is the DJ right now.")

@client.command(aliases=["/"])
async def doujin(ctx, cmd:str, page=0):
	if not isChannelDoujin(ctx):
		return await ctx.send("You cannot use this command from this channel. Only from Doujin channel")
	global read_
	if not read_:
		return await ctx.send("Please enter the readmode first. Use the command $read to enter readmode")
	global doujin
	global counter
	global current_doujin_manager
	if ctx.message.author.id != current_doujin_manager or not check_authority(ctx):
		return await ctx.message("Only Mods or the DJ can send these commands")
	if cmd.lower() == 'next':
		if counter >= len(doujin["images"]):
			return await ctx.send("You alreardy are at the last page. Use command $doujin restart to read again")
		async with aiohttp.ClientSession() as session:
			async with session.get(doujin["images"][counter]) as resp:
				if resp.status != 200:
					return await  ctx.send("Oops, looks like something went wrong. Try once again senpai")
				with io.BytesIO(await resp.read()) as data:
					counter += 1
					return await ctx.send(f"Page : {counter}", file=discord.File(data, f'page{counter}.jpeg'))
	if cmd.lower() == 'previous':
		if counter <= -1:
			return await ctx.send("You are already at the first page")
		async with aiohttp.ClientSession() as session:
			async with session.get(doujin["images"][counter]) as resp:
				if resp.status != 200:
					return await  ctx.send("Oops, looks like something went wrong. Try once again senpai")
				with io.BytesIO(await resp.read()) as data:
					counter -= 1
					return await ctx.send(f"Page : {counter}", file=discord.File(data, f'page{counter}.jpeg'))
				
	if cmd.lower() == 'restart':
		counter = 0
		return await ctx.send("Reset the progess, Now you can restart reading. Use command $doujin next to read")
	if cmd.lower() == 'delete':
		doujin = {}
		return await ctx.send("Deleted the previous doujin. Use command $getDoujin <id> to find a new one")

@client.command(aliases=["imouto","aski-chan"])
async def call_aski_chan(ctx):
	if not isChannelNormal(ctx):
		return await ctx.send("You cannot use this command from this channel")
	filename = os.path.join(os.getcwd() + "/Musics",choice(configs.Normal_onii_chan_sounds))
	file = discord.File(filename,filename="onii_chan.mp3")
	await ctx.send(file=file)

@client.command(aliases=["daisuki"])
async def call_aski_daisuki(ctx):
	if not isChannelNormal(ctx):
		return await ctx.send("You cannot use this command from this channel")
	#v = random.choice(configs.Daisuki)
	filename = os.path.join(os.getcwd() + "/Musics",choice(configs.Daisuki))
	file = discord.File(filename,filename="daisuki.mp3")
	await ctx.send(file=file)

@client.command(aliases=["onii-chan-song"])
async def call_me_onii(ctx):
	if not isChannelNormal(ctx):
		return await ctx.send("You cannot use this command from this channel")
	if not isOnii_chan(ctx):
		return await ctx.send("You are not my special onii-chan.  Baaakaaa...")
	filename = os.path.join(os.getcwd() + "/Musics",configs.Onii_chan_song)
	file = discord.File(filename,filename="onii-chan-song.mp3")
	await ctx.send(file=file)

@client.command(aliases=["special"])
async def special_service(ctx):
	if not isChannelNormal(ctx):
		return await ctx.send("You cannot use this command from this channel")
	if not isOnii_chan(ctx):
		return await ctx.send("You are not my special onii-chan.  Baaakaaa...")
	filename = os.path.join(os.getcwd() + "/Musics",configs.Onii_chan_special)
	file = discord.File(filename,filename="special.mp3")
	await ctx.send(file=file)

client.run(TOKEN)