import discord
import random
import asyncio
from discord.ext import commands
from random import shuffle
import json
import os

os.chdir("F:\\html\\html\\openo1\\ai")

prefix = "g!"
bot = commands.Bot(command_prefix = prefix)
token = ""
async def on_message(message):
    global msg
    msg = message.author

    bal = message.author.bal = 0

@bot.event
async def on_ready():
	print("Ready.")
	await bot.change_presence(activity=discord.Game(name="g!games | Let's play! "))


@bot.command()
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    wallet_amt = users[str(user.id)]["token"]
    #bank_amt = users[str(user.id)]["bank"]



    em = discord.Embed(title= f"{ctx.author.name}'s balance")

    em.add_field(name = "Token", value = wallet_amt)
    #em.add_field(name = "Bank", value = bank_amt)
    await ctx.send(embed = em)


async def open_account(user):


    users = await get_bank_data()

    with open("mainbank.json", 'r') as f:
        users = json.load(f)
    
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["token"] = 0
        #users[str(user.id)]["bank"] = 0

    with open("mainbank.json", 'w') as f:
        json.dump(users,f)
    return True
    


async def get_bank_data():
    with open("mainbank.json", 'r') as f:
        users = json.load(f)
    return users

  
@bot.command()
async def beg(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()
    user = ctx.author

    earnings = random.randrange(21)
    await ctx.send(f"Someone gave you {earnings} coins!!")



    users[str(user.id)]["token"] += earnings 
    with open("mainbank.json", 'w') as f:
        json.dump(users,f)

@bot.command(name= "casino")
async def casino(ctx, Ucolor: str, tokens:int):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author

    if tokens > users[str(user.id)]["token"]:
        embed = discord.Embed(title = "You're playing with tokens that you don't have!")
        await ctx.send(embed = embed)
        return False
    
    else:

        color = ["red","black", "black", "red", "red", "black", "red", "black", "black", "red"]

        random.shuffle(color)
        
        if Ucolor == color[0]:
            embed = discord.Embed(title = "**Casino Token**", description = f"The color is... {color[0]}! You won the double!")
            
            users[str(user.id)]["token"] += tokens 
            with open("mainbank.json", 'w') as f:
                json.dump(users,f)
        else:
            embed = discord.Embed(title = "**Casino Token**", description = f"The color is... {color[0]}! You lost!")
            users[str(user.id)]["token"] -= tokens
            with open("mainbank.json", 'w') as f:
                json.dump(users,f)
        await ctx.send(embed = embed)
	
  
  
@bot.command(name = "roll")
async def roll(ctx, dice:int, tokens: int):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author

    if tokens > users[str(user.id)]["token"]:
        embed = discord.Embed(title = "You're playing with tokens that you don't have!")
        await ctx.send(embed = embed)
        return False

    else:
        rd = random.randint(1, 5)
        if dice == rd:
            embed = discord.Embed(title = "**Roll Token**", description = f"The number is... {rd}! You won the triple!")
            
            earnings = tokens * 2
            users[str(user.id)]["token"] += earnings 
            with open("mainbank.json", 'w') as f:
                json.dump(users,f)

            await ctx.send(embed = embed)


        else:
            embed = discord.Embed(title = "**Roll Token**", description = f"The number is... {rd}! You lost but leave with +10 tokens!")
            users[str(user.id)]["token"] -= tokens + 10
            with open("mainbank.json", 'w') as f:
                json.dump(users,f)
            await ctx.send(embed = embed)

@bot.command(name= "games")
async def games(ctx):
    embed = discord.Embed(title = "**Games list**", description = "List of every games to win tokens!")
    #embed.set_thumbnail(url = "https://images.emojiterra.com/google/android-11/512px/1f40d.png")
    embed.add_field(name = "g!casino red/black tokens", value = "Bet on a color (red or black) and amount of tokens. You win = double of tokens!", inline = False)
    embed.add_field(name = "g!roll 1-5 tokens", value = "Bet on a number from 1 to 5 and amount of tokens. You have the correct number = triple of tokens!", inline = False)
    embed.add_field(name = "g!games", value = "List of every games to win tokens!", inline = False)
    #embed.add_field(name = "", value = "", inline = False)
    await ctx.send(embed = embed)



bot.run(token)
#   _____                       _       _     _      _____         ____                    ____  __                                  
#  / ____|                     (_)     | |   | |    / ____|       / __ \                  / __ \/_ |                                 
# | |     ___  _ __  _   _ _ __ _  __ _| |__ | |_  | |           | |  | |_ __   ___ _ __ | |  | || |                                 
# | |    / _ \| '_ \| | | | '__| |/ _` | '_ \| __| | |           | |  | | '_ \ / _ \ '_ \| |  | || |                                 
# | |___| (_) | |_) | |_| | |  | | (_| | | | | |_  | |____       | |__| | |_) |  __/ | | | |__| || |                                 
#  \_____\___/| .__/ \__, |_|  |_|\__, |_| |_|\__|  \_____|       \____/| .__/ \___|_| |_|\____/ |_|                                 
#             | |     __/ |        __/ |                                | |                                                          
#  _          |_|____|___/        |___/____                   _______   |_|             _             _           _                  
# | |           |___  /            |__   __|                 |__   __|  | |            (_)           | |         | |                 
# | |__  _   _     / / ___ _   _  __ _| |___ _   _   ______     | | ___ | | _____ _ __  _ _ __   __ _| |__   ___ | |_   _ __  _   _  
# | '_ \| | | |   / / / _ \ | | |/ _` | / __| | | | |______|    | |/ _ \| |/ / _ \ '_ \| | '_ \ / _` | '_ \ / _ \| __| | '_ \| | | | 
# | |_) | |_| |  / /_|  __/ |_| | (_| | \__ \ |_| |             | | (_) |   <  __/ | | | | | | | (_| | |_) | (_) | |_ _| |_) | |_| | 
# |_.__/ \__, | /_____\___|\__, |\__,_|_|___/\__,_|             |_|\___/|_|\_\___|_| |_|_|_| |_|\__, |_.__/ \___/ \__(_) .__/ \__, | 
#         __/ |             __/ |                                                                __/ |                 | |     __/ | 
#        |___/             |___/                                                                |___/                  |_|    |___/  
