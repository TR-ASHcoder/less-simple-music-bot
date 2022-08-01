import itertools
from itertools import cycle
from random import randint
from itertools import filterfalse
from logging import BASIC_FORMAT
from typing import Text
import random
import os
import json
import random
import asyncio
from nextcord.ext import commands 
import nextcord
import random
import wavelink
import datetime

intents = nextcord.Intents.default()
intents.message_content = True

             # add your own prefix⬎
bot = commands.Bot(command_prefix='', intents=intents)
bot.remove_command("help")



# ---- EVENTS ----

@bot.event
async def on_ready():
  print("a new start")
  bot.loop.create_task(node_connect())

@bot.event 
async def on_wavelink_node_ready(node: wavelink.Node):
  print(f"Node {node.identifier} is ready!!!!")

async def node_connect():
  await bot.wait_until_ready()
  await wavelink.NodePool.create_node(bot=bot, host='lavalinkinc.ml', port=443, password='incognito', https=True)


@bot.event
async def on_wavelink_track_end(player: wavelink.Player, track: wavelink.Track, reason):
  ctx = player.ctx
  vc: wavelink.Player = ctx.voice_client

  
  


  if vc.loop:
    return await vc.play(track)



  next_song = vc.queue.get()
  await vc.play(next_song)

  em = nextcord.Embed(title = f"*~Next Playing~*")
  em.add_field(name=f"`{next_song.title}`", value=f"**By**: ||`{next_song.author}`||")

  await ctx.send(embed=em, mention_author=False)
  



# ---- COMMMANDS ----


@bot.command()
async def play(ctx: commands.Context, *, search: wavelink.YouTubeTrack):
  if not ctx.voice_client: 
    vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
 
  elif not getattr(ctx.author.voice, "channel", None):
    return await ctx.reply("You are not in a vc, therefore, you cannot invoke the `play` command")
  
  else: 
    vc:wavelink.Player = ctx.voice_client 
  
  #guy = ctx.message.author.mention

  
  
  em = nextcord.Embed(title = f"*Now Playing*")
  em.add_field(name=f"`{search.title}`", value=f"**By**: ||`{search.author}`||")
    

  


  if vc.is_playing():
    await vc.queue.put_wait(search)
    await ctx.reply(f"***Added `{search.title}` to the queue***", mention_author=False)


  elif vc.queue.is_empty:
      await vc.play(search)
      await ctx.reply(embed=em, mention_author=False)








  
  vc.ctx = ctx 
  setattr(vc, "loop", False)



@bot.command(aliases = ['Pause'])
async def pause(ctx: commands.Context):
  if not ctx.voice_client: 
    vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
 
  elif not getattr(ctx.author.voice, "channel", None):
    return await ctx.reply("You are not in a vc, therefore, you cannot invoke the `pause` command")
  
  else: 
    vc: wavelink.Player = ctx.voice_client

  em = nextcord.Embed(title = f"*Paused*")
  em.add_field(name=f"*we `paused` your song for ya*", value="you better be grateful")

  
  


    

  await vc.pause()
  await ctx.reply(embed=em, mention_author=False)



@bot.command(aliases = ['Play','Resume'])
async def resume(ctx: commands.Context):
  if not ctx.voice_client: 
    vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
 
  elif not getattr(ctx.author.voice, "channel", None):
    return await ctx.reply("You are not in a vc, therefore, you cannot invoke the `resume` command")
  
  else: 
    vc: wavelink.Player = ctx.voice_client

  em = nextcord.Embed(title = f"*Resumed*")
  em.add_field(name=f"*we `resumed` your song for ya*", value="you better be grateful")

  
  


    

  await vc.resume()
  await ctx.reply(embed=em, mention_author=False)


  
@bot.command()
async def stop(ctx: commands.Context):
  if not ctx.voice_client: 
    vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
 
  elif not getattr(ctx.author.voice, "channel", None):
    return await ctx.reply("You are not in a vc, therefore, you cannot invoke the `stop` command")
  
  else: 
    vc: wavelink.Player = ctx.voice_client

  em = nextcord.Embed(title = f"*Stopped*")
  em.add_field(name=f"*we `stopped` your song for ya*", value="you better be grateful")

  
  


    

  await vc.stop()
  await ctx.reply(embed=em, mention_author=False)



@bot.command(aliases = ['kys','die'])
async def disconnect(ctx: commands.Context):
  if not ctx.voice_client: 
    vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
 
  elif not getattr(ctx.author.voice, "channel", None):
    return await ctx.reply("You are not in a vc, therefore, you cannot invoke the `disconnect` command")
  
  else: 
    vc: wavelink.Player = ctx.voice_client

  em = nextcord.Embed(title = f"*Disconnected*")
  em.add_field(name=f"*the bot has been `disconnected`*", value="type in `ADD PREFIX` play and a song of choice to invite it back :]")

  await vc.disconnect()
  await ctx.reply(embed=em, mention_author=False)


@bot.command()
async def loop(ctx: commands.Context):
  if not ctx.voice_client: 
   return await ctx.reply("You are not in a vc, therefore, you cannot invoke the `loop` command")
  else: 
   vc: wavelink.Player = ctx.voice_client


  
  try:
    vc.loop ^= True
  except:
    setattr(vc, "loop", False)

  if vc.loop:
    await ctx.reply(f"***Now looping your song~***", mention_author=False)
  else: 
    await ctx.reply(f'***`{vc.track.title}` is no longer looping***', mention_author=False)



@bot.command()
async def skip(ctx: commands.Context):
  if not ctx.voice_client: 
    vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
 
  elif not getattr(ctx.author.voice, "channel", None):
    return await ctx.reply("You are not in a vc, therefore, you cannot invoke the `skip` command")
  
  else: 
    vc: wavelink.Player = ctx.voice_client

  em = nextcord.Embed(title = f"*skiped*")
  em.add_field(name=f"*we `skiped` your song for ya*", value="you better be grateful")

  
  


    

  await vc.stop()
  await ctx.reply(embed=em, mention_author=False)


@bot.command()
async def queue(ctx: commands.Context):
  if not ctx.voice_client:  
   return await ctx.reply("You are not in a vc, therefore, you cannot invoke the `queue` command")
  
  else:
    vc: wavelink.Player = ctx.voice_client

  if vc.queue.is_empty:
    return await ctx.reply("***~thy `Queue` is empty~***", mention_author=False)


  
  em = nextcord.Embed(title = f"***Queue***",   
  color=nextcord.Color.from_rgb(46,49,54))
  queue = vc.queue.copy()
  song_count = 0 
  for song in queue:
      song_count += 1 
      em.add_field(name=f"⬐*Song `{song_count}`*⬎", value=f"`{song.title}`", inline=False)


  await ctx.reply(embed=em, mention_author=False)


@bot.command()
async def info(ctx: commands.Context):
  if not ctx.voice_client:  
   return await ctx.reply("You are not in a vc, therefore, you cannot invoke the `info` command")
  
  else:
    vc: wavelink.Player = ctx.voice_client

  if not vc.is_playing():
    await ctx.reply("***nothing is playing at the moment***", mention_author=False)


  em = nextcord.Embed(title = f"***Info***", description=f"**Artist:** \n`{vc.track.author}`"    
  ,color=nextcord.Color.from_rgb(100, 108, 245))
  em.add_field(name="Length:", value=f"`{str(datetime.timedelta(seconds=vc.track.length))}`")
  em.add_field(name="Extra Info:", value=f"[Click me for original]({str(vc.track.uri)})")

  await ctx.send(embed=em)

  

# ---- HELP COMMAND ----


@bot.command(aliases = ['HELP','hep','h','H'])
async def help(ctx):
  em = nextcord.Embed(title = "`commands:`")
  em.add_field(name = "**play**:", value = "plays song of choice,  e.g:  __t.play {song of choice}__", inline=False)
  em.add_field(name = "**pause**:", value = "pauses song that is being played", inline=False)
  em.add_field(name = "**resume/Play**:", value = "resumes song that was paused", inline=False)
  em.add_field(name = "**stop**:", value = "stops the song that was playing so you can play another one", inline=False)
  em.add_field(name = "**skip**:", value = "makes bot skip to the next song in queue", inline=False)
  em.add_field(name = "**loop**:", value = "loops song that is being played", inline=False)
  em.add_field(name = "**info**:", value = "shows info on the song being played", inline=False)
  em.add_field(name = "**queue**:", value = "shows queued songs", inline=False)
  em.add_field(name = "**disconnect**:", value = "makes bot leave the vc", inline=False)


  await ctx.send(embed=em)
 

    


  






  


bot.run("") #<----- add your token
