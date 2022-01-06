import discord
import os
import random
import time
from discord.utils import get
from discord.ext import commands
from keep_alive import keep_alive


bot = commands.Bot(command_prefix="!")

timerVar = 0
meat = 0

pickItems = ["a rock","nothing","a stick","a stick","a bone","a dead bush","a grapevine","nothing","a tree","a leaf","a bush","a deer","a goat","a chicken","a piece of string"]
allItems = ["nothing","a rock","a stick","a bone","a dead bush", "a grapevine","deer meat","goat meat","chicken","cooked deer","cooked goat","cooked chicken","a stick pile","a pickaxe", "a fishing rod", "a fireplace","a piece of dirt", "a leaf", "a tree", "a bush", "a piece of coal", "a piece of copper", "a piece of iron", "a piece of gold","a piece of string","a salmon","a cod","a herring","a trout"]
allItemsPlural = ["nothings :black_medium_square:","rocks :rock:","sticks :wood:","bones :bone:","dead bushes :herb:", "grapevines :grapes:","deer meat :deer:","goat meat :goat:","chicken :chicken:","cooked deer :cut_of_meat:","cooked goat :meat_on_bone:","cooked chicken :poultry_leg:","stick piles :chopsticks:","pickaxes :pick:", "fishing rods :fishing_pole_and_fish:", "fireplaces :fire:","pieces of dirt :brown_square:", "leaves :leaves:", "trees :deciduous_tree:", "bushes :potted_plant:", "pieces of coal :black_circle:", "pieces of copper :brown_circle:", "pieces of iron :purple_circle:", "pieces of gold :yellow_circle:","pieces of string :yarn:","salmon :tropical_fish:","cod :blowfish:","herring :fish:","trout :tropical_fish:"]

removeRoles = []
weatherTable = ["sunny", "sunny", "cloudy", "pretty cold", "raining", "storming", "really hot"]
serverItems = []

recipes = {
  "stickpile":["a stick","a stick"],
  "pickaxe":["a stick","a stick","a rock"],
  "fireplace":["a stick pile", "a stick"],
  "fishing rod":["a piece of string", "a piece of string", "a stick"]
}
phrase = {
  "stickpile":"Use this to make a fireplace!",
  "pickaxe":"You can mine faster and are immune to breaking it.",
  "fireplace":"Use this to cook food!",
  "fishing rod":"Use this to fish!"
}
hunger = 20
hole = 0
startTime = time.time()
gWeather = 0
gameTime = "9880BC"

@bot.command()
async def look(ctx):
  global meat
  test = random.randint(0,len(pickItems) - 1)
  sender = "You found " + pickItems[test] + "!"
  if pickItems[test] == "a deer":
    meat = 1
    sender += "\nType !kill deer to kill it!"
  elif pickItems[test] == "a goat":
    meat = 2
    sender += "\nType !kill goat to kill it!"
  elif pickItems[test] == "a chicken":
    meat = 3
    sender += "\nType !kill chicken to kill it!"
  else:
    serverItems.append(pickItems[test])
  await ctx.send(sender)

@bot.command(aliases = ["inv"])
async def items(ctx):
  message = ctx.message
  p = message.content.split(" ", 1)
  allItemsNum = []

  for i in range(len(allItems)):
    allItemsNum.append(0)

  for j in range(len(allItemsNum)):
    for i in range(len(serverItems)):
      print(i)
      if serverItems[i] == allItems[j]:
        allItemsNum[j] += 1
  try:
    j = (int(p[1]) - 1) * 25
    embed=discord.Embed(title="Items", description="Page", color=0x00ff00)
    for i in range(len(allItems) - j):
      embed.add_field(name=allItems[i+j], value=f"There are {allItemsNum[i+j]} {allItemsPlural[i+j]}", inline=False)
  except:
    embed=discord.Embed(title="Items", description="Page 1", color=0x00ff00)
    for i in range(len(allItems)):
      embed.add_field(name=allItems[i], value=f"There are {allItemsNum[i]} {allItemsPlural[i]}", inline=False)
  await ctx.send(embed=embed)

@bot.command()
async def craft(ctx):
  message = ctx.message
  p = message.content.split(" ", 1)
  check = 0
  try:
    if p[1] == "nope":
      await ctx.send("")
      return
  except:
    await ctx.send("You didn't send an item.")
    return
  for i in list(recipes.keys()):
    if p[1].lower() == i:
      print("test2")
      for j in recipes[i]:
        if j in serverItems:
          check += 1
        print(check)
      if check == len(recipes[i]):
        for j in recipes[i]:
          serverItems.remove(j)
        a = "a " + i.lower()
        serverItems.append(a)
        await ctx.send(f"You made {a}! {phrase[i]}")
      else:
        await ctx.send(f"You don't have enough materials")
      
@bot.command()
async def recipe(ctx):
  await ctx.send("Stick Pile: 2 Sticks")
  await ctx.send("Pickaxe: 2 Rocks, 1 Stick")
  await ctx.send("Fireplace: 1 stick pile, 1 stick")

@bot.command()
async def eat(ctx):
  x = 0
  randomResponse = ["It rejuvenates you","You feel energetic","That was one of the best meals you've had!","It was okay.","The food was alright","The food was kind of *off*","That wasn't the best meal, but you can live with it."]
  for i in range(len(serverItems) - 1):
    if serverItems[i] == "a grapevine":
      await ctx.send("You eat a bunch of grapes")
      serverItems.remove("a grapevine")
      x = 1
      await ctx.send(randomResponse[random.randint(0,len(randomResponse))])
      break
    elif serverItems[i] == "cooked chicken":
      await ctx.send("You eat some chicken")
      serverItems.remove("cooked chicken")
      x = 1
      await ctx.send(randomResponse[random.randint(0,len(randomResponse))])
      break
    elif serverItems[i] == "cooked deer":
      await ctx.send("You eat some deer")
      serverItems.remove("cooked deer")
      x = 1
      await ctx.send(randomResponse[random.randInt(0,len(randomResponse))])
      break
    elif serverItems[i] == "cooked goat":
      await ctx.send("You eat some goat")
      serverItems.remove("cooked goat")
      x = 1
      await ctx.send(randomResponse[random.randInt(0,len(randomResponse))])
      break

  if x == 0:
    await ctx.send("You didn't find any food!")
  
@bot.command()
async def dig(ctx):
  global hole
  y = 0
  for i in range(len(serverItems)):
    message = ctx.message
    p = message.content.split(" ", 1)
    try:
      if "a pickaxe" in serverItems[i] and p[1] == "pickaxe":
        hole += random.randint(2, 4)
        x = random.randint(2,5)
        if hole < 40:
          temp = f"You used a pickaxe.\nYou got {str(x)} dirt!\nThe hole you dug is now {str(hole)} feet deep"
        else:
          temp = f"You used a pickaxe.\nYou got {str(x)} stone!\nThe hole you dug is now {str(hole)} feet deep"
        if random.randint(0,2) == 1:
          temp += "\nYou found a piece of coal!"
          serverItems.append("a piece of coal")
        if random.randint(0,5) == 3:
          temp += "\nYou found a piece of copper!"
          serverItems.append("a piece of copper")
        if random.randint(0,8) == 5:
          temp += "\nYou found a piece of iron!"
          serverItems.append("a piece of iron")
        if random.randint(0,12) == 8:
          temp += "\nYou found a piece of gold!"
          serverItems.append("a piece of gold")
        for j in range(x):
          if hole < 40:
            serverItems.append("a piece of dirt")
          else:
            serverItems.append("a rock")
        await ctx.send(temp)
        y = 1
        return
      elif "a rock" in serverItems[i] and p[1] == "rock":
        hole += random.randint(0, 1)
        x = random.randint(0,3)
        if hole < 40:
          await ctx.send(f"You used a rock.\nYou got {str(x)} dirt!\nThe hole you dug is now {str(hole)} feet deep")
          for j in range(x):
            serverItems.append("a piece of dirt")
        if hole > 40 or x >= 2:
          serverItems.pop(i)
          await ctx.send("The rock you used is now too dull to dig. You got rid of it.")
        y = 1
        return
    except:
      if serverItems[i] == "a rock":
        hole += random.randint(0, 1)
        x = random.randint(0,3)
        if hole < 40:
          await ctx.send(f"You used a rock.\nYou got {str(x)} dirt!\nThe hole you dug is now {str(hole)} feet deep")
          for j in range(x):
            serverItems.append("a piece of dirt")
        if hole > 40 or x >= 2:
          serverItems.pop(i)
          await ctx.send("The rock you used is now too dull to dig. You got rid of it.")
        y = 1
        return
        await ctx.send(temp)
        y = 1
        return
  if y == 0:
    await ctx.send("You don't have a rock or a pickaxe!")

@bot.command()
async def fish(ctx):
  x = 0
  for i in range(len(serverItems)):
    if serverItems[i] == "a fishing rod":
      x = 1
  if x == 1:
    temp = "You start fishing!"
    salmon = random.randint(0, 2)
    cod = random.randint(0, 2)
    herring = random.randint(0, 2)
    trout = random.randint(0, 2)
    hour = random.randint(1, 4)
    await ctx.send(temp + f"\nYou spent {hour} hours fishing and caught:\n {salmon} salmon,\n{cod} cod,\n{herring} herring,\nand {trout} trout.")
    for i in range(salmon):
      serverItems.append("salmon")
  else:
    await ctx.send("You don't have a fishing rod!")


@bot.command(aliases = ["attack"])
async def kill(ctx):
  global meat
  message = ctx.message
  sender = ""
  p = message.content.split(" ",1)
  try:
    if p[1] == "deer" and meat == 1:
      sender += "You got deer meat!"
      serverItems.append("deer meat")
      meat = 0
    elif p[1] == "goat" and meat == 2:
      sender += "You got goat meat!"
      serverItems.append("goat meat")
      meat = 0
    elif p[1] == "chicken" and meat == 3:
      sender += "You got chicken!"
      serverItems.append("chicken")
      meat = 0
    else:
      sender += f"You killed {p[1]}!"
      sender += "They somehow came back to life!"
  except:
    sender += "You killed yourself!"
    sender += "You somehow came back to life!"
  await ctx.send(sender)

@bot.command() 
async def timeline(ctx):
  global gameTime
  message = ctx.message
  p = message.content.split(" ",1)
  await ctx.send(f"You're in {gameTime}\nUpdate log:")
  if p[1] == "1":
    await ctx.send("10000BC:\n-Added basic commands\n9990BC:\n-Added `!eat`, `!dig`, `!recipe`, `!craft`\n-Very buggy\n9980BC:\n-Added 'Killing'\n-Added searching for an item\n9970BC:\n-Fixed `!craft`\n-Made `!timeline` display all updates.\n9960BC:\n-Added animals to `!kill`\n9950BC:\n-Added a recipe for the pickaxe\n-Fixed saving\n-Made `!items` better\n9940BC:\n-Added plant life to !look\n-Added alias to `!kill`: `!attack`\n9935BC:\n-Added a way better `!items`")
  elif p[1] == "2":
    await ctx.send("9930BC:\n-Added more items to `!dig`\n-Added multiple pages to `!timeline`\n9920BC:\n-Added the ability to cook and eat meat.\n9910BC:\n-Added a tornado that has a 1/1000 chance of removing a food and items.\n9900BC:\n-Added `!weather` and `!time`\n9890BC:\n-Added the ability to make your own country `!makecountry`\n9880BC:\n-Added the ability to fish `!fish`\n-Fixed a bug where certain items wouldn't be added to the list of items you had:\n---Pickaxes (Crafting)\n---Fireplaces (Crafting)\n---Cooked meat (deer, goat, chicken) (Cooking)\n9870BC:\n-Added the ability to transport using `!transport`")
  elif p[1] == "3":
    await ctx.send("9870BC:\n-Added the ability to transport using `!transport`\n9865BC:\n-Added pages for `!items` and `!timeline`\n9862BC:\n-Changed servers because of bluederv.")
  try:
    if int(p[1]) > 2:
      await ctx.send("That's too big of a page number!")
    elif int(p[1]) < 1:
      await ctx.send("That's too small of a page number!")
  except:
    await ctx.send("Please do '!timeline <page>'")

@bot.command()
async def cook(ctx):
  checker = 0
  message = ctx.message
  p = message.content.split(" ",1)
  putOut = random.randint(0,4)
  for i in range(len(serverItems)):
    if serverItems[i] == "a fireplace":
      if p[1] == "chicken":
        try:
          serverItems.remove("chicken")
        except:
          await ctx.send("You don't have chicken!")
          break
        serverItems.append("cooked chicken")
        await ctx.send("You cooked some chicken!")
        break
      elif p[1] == "deer meat":
        try:
          serverItems.remove("deer meat")
        except:
          await ctx.send("You don't have deer meat!")
          break
        await ctx.send("You cooked some deer meat")
        serverItems.append("cooked deer")
        break
      elif p[1] == "goat meat":
        try:
          serverItems.remove("goat meat")
        except:
          await ctx.send("You don't have goat meat!")
          break
        await ctx.send("You cooked some goat meat")
        serverItems.append("cooked goat")
        break
      else:
        await ctx.send("You can't cook that!")
        break
      if putOut == 1:
        await ctx.send("Your fireplace burned out!")
        serverItems.remove("a fireplace")
      checker = 1
  print(checker)
  if checker == 0:
    await ctx.send("You don't have a fireplace!")

@bot.command(aliases = ["move", "transfer"])
async def transport(ctx):
  print(removeRoles)
  message = ctx.message
  p = message.content.split(" ",1)
  author = ctx.author
  try:
    if p[1] == " ":
      await ctx.send("Too many spaces!")
  except:
    await ctx.send("Send a country!")
  
  try:
    role = get(author.guild.roles, name=p[1])
    for rolermv in [r for r in ctx.guild.roles if r.id in removeRoles]:
      await author.remove_roles(rolermv)
    await author.add_roles(role)
  except:
    await ctx.send("That channel doesn't exist!")
    return
  await ctx.send(f"You are now in {role}!")

@bot.command()
async def gametime(ctx):
  temp = time.ctime()
  await ctx.send(f"The time in game is {temp}")

@bot.command()
async def weather(ctx):
  global gWeather
  global startTime
  nowTime = time.time()
  if nowTime - startTime >= 240:
    gWeather = random.randint(0, 6)
    startTime = time.time()

  print(weatherTable[gWeather])
  temp = weatherTable[gWeather]
  if nowTime - startTime >= 86400:
    await ctx.send("Wow! It's been a whole day! Time to ping @everyone!")

  await ctx.send(f"It is {temp} outside")

@bot.command()
async def makecountry(ctx, member : discord.Member, member2 : discord.Member):
  message = ctx.message
  author = ctx.author
  p = message.content.split(" ", 4)
  guild = ctx.guild
  
  await guild.create_role(name=p[3])

  category = discord.utils.get(guild.categories, name="Countries")
  admin_role = get(guild.roles, name="The God of Outside")
  role = get(guild.roles, name=p[3])
  overwrites = {
    guild.default_role: discord.PermissionOverwrite(read_messages=False),
    role: discord.PermissionOverwrite(read_messages=True),
    admin_role: discord.PermissionOverwrite(read_messages=True)
  }
  
  removeRoles.append(role.id)
  for rolermv in [r for r in ctx.guild.roles if r.id in removeRoles]:
      await author.remove_roles(rolermv)
  
  await guild.create_text_channel(name=p[3], category=category)
  await member.add_roles(role)
  await member2.add_roles(role)
  await author.add_roles(role)


@bot.command()
async def what(ctx):
  await ctx.send("Everyone here is part of a community, so you all share the same resources. You can do !look to try and find items, and you can craft them into things using !craft. You can view all of your items using !items")

@bot.event
async def on_message(message):
  global serverItems,removeRoles
  member = message.author
  sus = member.id
  textfile = open("serverItems.txt", "w")
  for element in serverItems:
    textfile.write(element + "\n")
  textfile.close()
  textfile = open("removeRoles.txt", "w")
  for element in removeRoles:
    textfile.write(element + "\n")
  textfile.close()
  print(serverItems)
  print(removeRoles)
  if sus == 779447225766903830:
    member.ban()
  await bot.process_commands(message)
  
@bot.event
async def on_ready():
  global serverItems,removeRoles
  try:
    with open('serverItems.txt', 'r') as f:
      contents = f.read()
      serverItems = contents.split("\n")
      print(serverItems)
      f.close()
    with open('removeRoles.txt', 'r') as f:
      contents = f.read()
      removeRoles = contents.split("\n")
      print(removeRoles)
      f.close()
  except:
    return
  print(serverItems)
  await bot.get_channel(905443023318577252).send("Bot is online\nRunning for: Testing for 9860BC!") # <@&905442532958306334> - bot ping role
  # keep_alive()
bot.run(os.getenv("TOKEN_TEST"))
