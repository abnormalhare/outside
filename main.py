import discord
import os
import random
import asyncio
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

meat = 0
pickItems = ["a rock","nothing","a stick","a bone","a dead bush", "a grapevine", "nothing", "a tree", "a leaf","a bush","a deer","a goat","a chicken"]
allItems = ["nothing","a rock","a stick","a bone","a dead bush", "a grapevine","deer meat","goat meat","chicken","a stick pile","a pickaxe","a piece of dirt", "a leaf", "a tree", "a bush", "a piece of coal", "a piece of copper", "a piece of iron", "a piece of gold"]
allItemsPlural = ["nothings","rocks","sticks","bones","dead bushes", "grapevines","deer meat","goat meat","chicken","stick piles","pickaxes","pieces of dirt", "leaves", "trees", "bushes", "pieces of coal", "pieces of copper", "pieces of iron", "pieces of gold"]
serverItems = []
recipes = {
  "Stick Pile":"2 Sticks",
  "Stick":"A dead bush",
  "Marker":"A stick and a bone"
}
itemNames = {
  "Stick Pile":"stickPile"
}
hunger = 20
hole = 0
gameTime = "9930BC"

@bot.command()
async def look(ctx):
  global meat
  test = random.randint(0,len(pickItems) - 1)
  await ctx.send("You found " + pickItems[test] + "!")
  if pickItems[test] == "a deer":
    meat = 1
    await ctx.send("Type !kill deer to kill it!")
  elif pickItems[test] == "a goat":
    meat = 2
    await ctx.send("Type !kill goat to kill it!")
  elif pickItems[test] == "a chicken":
    meat = 3
    await ctx.send("Type !kill chicken to kill it!")
  else:
    serverItems.append(pickItems[test])

@bot.command()
async def items(ctx):
  print("Hello")
  allItemsNum = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  for j in range(len(allItems)):
    for i in range(len(serverItems)):
      print(i)
      if serverItems[i] == allItems[j]:
        allItemsNum[j] += 1
  embed=discord.Embed(title="Items", description="These are everyone's items", color=0x00ff00)
  for i in range(len(allItems)):
    embed.add_field(name=allItems[i], value=f"There are {allItemsNum[i]} {allItemsPlural[i]}", inline=False)
  await ctx.send(embed=embed)

@bot.command()
async def craft(ctx):
  x = 0
  message = ctx.message
  p = message.content.split(" ", 4)
  try:
    if p[1] == "nope":
      await ctx.send("Hello! You found an easter egg!")
      return
  except:
    await ctx.send("You didn't send an item. Here's a list:\n`stickpile`\n`pickaxe`")
  if p[1].lower() == "stickpile" or p[1].lower == "stick pile":
    for i in range(len(serverItems)):
      if serverItems[i] == "a stick":
        serverItems.pop(i)
        x = 1
        break
      print(str(i) + ", " + serverItems[i])
    if x != 1:
      await ctx.send("You don't have enough sticks!")
      return
    x = 0
    for i in range(len(serverItems)):
      if serverItems[i] == "a stick":
        serverItems.pop(i)
        x = 1
        break
    if x != 1:
      await ctx.send("You don't have enough sticks!")
      return
    await ctx.send("You made a stick pile! Use this to make a fireplace!")
    serverItems.append("a stick pile")
  elif p[1].lower() == "pickaxe":
    for i in range(len(serverItems)):
      if serverItems[i] == "a rock":
        serverItems.pop(i)
        x = 1
        break
    if x != 1:
      await ctx.send("You don't have enough rocks!")
      return
      x = 0
    for i in range(len(serverItems)):
      if serverItems[i] == "a rock":
        serverItems.pop(i)
        x = 1
        break
    if x != 1:
      await ctx.send("You don't have enough sticks!")
      return
    x = 0
    for i in range(len(serverItems)):
      if serverItems[i] == "a stick":
        serverItems.pop(i)
        x = 1
        break
    if x != 1:
      await ctx.send("You don't have enough sticks!")
      return
    serverItems.append("a pickaxe")
    await ctx.send("You made a pickaxe! You can mine faster and are immune to breaking it.")
      
    
      
      
@bot.command()
async def recipe(ctx):
  await ctx.send("Stick Pile: 2 Sticks")
  await ctx.send("Pickaxe: 2 Rocks, 1 Stick")

@bot.command()
async def eat(ctx):
  x = 0
  for i in range(len(serverItems) - 1):
    if serverItems[i] == "a grapevine":
      await ctx.send("The food rejuvenates you")
      x = 1
      return
  if x == 0:
    await ctx.send("You didn't find any food!")
  
@bot.command()
async def dig(ctx):
  global hole
  y = 0
  for i in range(len(serverItems)):
    if serverItems[i] == "a rock":
      hole += random.randint(0, 1)
      x = random.randint(0,3)
      await ctx.send("You used a rock.")
      await ctx.send("You got " + str(x) + " dirt!")
      await ctx.send("The hole you dug is now " + str(hole) + " feet deep.")
      for j in range(x):
        serverItems.append("a piece of dirt")
      if hole == 1 or x >= 2:
        serverItems.pop(i)
        await ctx.send("The rock you used is now too dull to dig. You got rid of it.")
      y = 1
      return
    if serverItems[i] == "a pickaxe":
      hole += random.randint(2, 4)
      x = random.randint(2,5)
      await ctx.send("You mined with your pick.")
      await ctx.send("You got " + str(x) + " dirt!")
      await ctx.send("The hole you dug is now " + str(hole) + " feet deep.")
      if random.randint(0,1) == 1:
        await ctx.send("You found a piece of coal!")
        serverItems.append("a piece of coal")
      if random.randint(0,3) == 3:
        await ctx.send("You found a piece of copper!")
        serverItems.append("a piece of copper")
      if random.randint(0,5) == 5:
        await ctx.send("You found a piece of iron!")
        serverItems.append("a piece of iron")
      if random.randint(0,8) == 8:
        await ctx.send("You found a piece of gold!")
        serverItems.append("a piece of gold")
      for j in range(x):
        serverItems.append("a piece of dirt")
      y = 1
      return
  if y == 0:
    await ctx.send("You don't have a rock or a pickaxe!")

@bot.command(aliases = ["attack"])
async def kill(ctx):
  global meat
  message = ctx.message
  p = message.content.split(" ",1)
  try:
    if p[1] == "deer" and meat == 1:
      await ctx.send("You got deer meat!")
      serverItems.append("deer meat")
      meat = 0
    elif p[1] == "goat" and meat == 2:
      await ctx.send("You got goat meat!")
      serverItems.append("goat meat")
      meat = 0
    elif p[1] == "chicken" and meat == 3:
      await ctx.send("You got chicken!")
      serverItems.append("chicken")
      meat = 0
    else:
      await ctx.send(f"You killed {p[1]}!")
      await ctx.send("They somehow came back to life!")
  except:
    await ctx.send("You killed yourself!")
    await ctx.send("You somehow came back to life!")

@bot.command() 
async def timeline(ctx):
  global gameTime
  message = ctx.message
  p = message.content.split(" ",1)
  await ctx.send(f"You're in {gameTime}\nUpdate log:")
  if p[1] == "1":
    await ctx.send("10000BC:\n-Added basic commands\n9990BC:\n-Added !eat, !dig, !recipe, !craft\n-Very buggy\n9980BC:\n-Added 'Killing'\n-Added searching for an item\n9970BC:\n-Fixed !craft\n-Made !timeline display all updates.\n9960BC:\n-Added animals to kill\n9950BC:\n-Added a recipe for the pickaxe\n-Fixed saving\n-Made !items better\n9940BC:\n-Added plant life to !look\n-Added alias to !kill '!attack'\n9935BC:\n-Added a way better '!items'")
  elif p[1] == "2":
    await ctx.send("9930BC:\n-Added more items to '!dig'")
  try:
    if int(p[1]) > 2:
      await ctx.send("That's too big of a page number!")
    elif int(p[1]) < 1:
      await ctx.send("That's too small of a page number!")
  except:
    await ctx.send("Please do '!timeline <page>'")

@bot.command()
async def what(ctx):
  await ctx.send("Everyone here is part of a community, so you all share the same resources. You can do !look to try and find items, and you can craft them into things using !craft. You can view all of your items using !items")

@bot.event
async def on_message(message):
  with open("serverItems.txt", "w") as filehandle:
    for i in serverItems:
      filehandle.write("%s\n" % i)
  print("File Saved!")
  await bot.process_commands(message)

@bot.event
async def on_ready():
  global serverItems
  print('We have logged in as {0.user}'.format(bot))
  with open('serverItems.txt', 'r') as filehandle:
    for line in filehandle:
      currentPlace = line[:-1]
      serverItems.append(currentPlace)
  print(serverItems)

bot.run(os.getenv("TOKEN"))