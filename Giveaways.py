# Standart imports
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random
import glob, os, os.path
import sys
import fileinput
import asyncio
import datetime
from secrets import TOKEN

# Standart config
client: Bot = commands.Bot(command_prefix='?')
client.remove_command('help')
# Reaction emoji


# Standart event(s)
@client.event
async def on_ready():
   await  client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Giveaways | ?help'))
   print(f"Logged in as {client.user} (ID: {client.user.id})")


# Standart help command
@client.command()
async def help(ctx):
    embed = discord.Embed(color=0x7289DA, title='Commands', description=f"Prefix: `?` \nTime format: `hours` \nMin. perms to create a giveaway: `ban members` \n \n`?start <time> <prize>` ● Start a Giveaway \n`?enter <giveaway ID>` ● Participate in a giveaway \n`?reroll <giveaway ID>` ● Re-roll a giveaway \n`?help` ● Shows this help message \n \n[Invite the bot!](https://discord.com/api/oauth2/authorize?client_id=710271590411010092&permissions=388160&scope=bot)")
    embed.set_footer(text=f"Invoked by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
 

@client.command()
@commands.has_permissions(ban_members=True)
async def start(ctx, atime: int = None, *, prize = None):
    guild = ctx.message.guild
    max_time = 48
    if atime == None:
        await ctx.send('Please enter a valid time.')
        return
    if prize == None:
        await ctx.send('Please enter a valid prize.')
        return
    if atime >= max_time:
        await ctx.send('Sorry, but the max giveaway time is 48 hours.')
        return
    nums1 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    nums2 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    nums3 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    nums4 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    nums5 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    n1 = random.choice(nums1)
    n2 = random.choice(nums2)
    n3 = random.choice(nums3)
    n4 = random.choice(nums4)
    n5 = random.choice(nums5)
    prize_id = f"{n1}{n2}{n3}{n4}{n5}"
    hours = atime - 2
    ts = datetime.datetime.now() + datetime.timedelta(hours=hours)
    e = discord.Embed(color=0x2BFF06, title=f"{prize}", description=f'Type **!enter {prize_id}** to enter this giveaway! \n \nTime: **{atime} hour(s)** \n \nHosted by: {ctx.message.author.mention}', timestamp=ts)
    e.set_footer(text=f"!enter {prize_id} | Ends at")
    msg = await ctx.send(embed=e)
    prize_id_logs = open(f"./Giveaways/{guild.id}-{prize_id}-giveaway.txt", "w")
    prize_id_logs.write(f"{ctx.message.author.id}")
    prize_id_logs.close()
    await asyncio.sleep(atime * 3600)
    at = file_len(f"./Giveaways/{guild.id}-{prize_id}-giveaway.txt")
    if at <= 3:
        await ctx.send('Sorry, but there have to be at least 3 attendees to make a giveaway.')
        open(f"./Giveaways/{guild.id}-{prize_id}-giveaway.txt", 'w').close()
        await asyncio.sleep(1)
        os.remove(f"./Giveaways/{guild.id}-{prize_id}-giveaway.txt") 
        return
    lines = open(f"./Giveaways/{guild.id}-{prize_id}-giveaway.txt").read().splitlines()
    winner_id = random.choice(lines)
    winner = await client.fetch_user(winner_id)
    e1 = discord.Embed(color=0xF30700, title=f"{prize}", description=f"Giveaway has ended! \n \n**Winner:** {winner.mention}", timestamp=ts)
    e1.set_footer(text=f"Prize ID {prize_id} | Ended at")
    await asyncio.sleep(atime * 10)
    await msg.edit(embed=e1)
    await ctx.send('If you want to reroll this giveaway, you have 1 hour to do so.')
    await asyncio.sleep(3600)
    open(f"./Giveaways/{guild.id}-{prize_id}-giveaway.txt", 'w').close()
    await asyncio.sleep(1)
    os.remove(f"./Giveaways/{guild.id}-{prize_id}-giveaway.txt") 



@client.command()
async def enter(ctx, prize_id: int = None):
    guild = ctx.message.guild
    if prize_id == None:
        await ctx.send('Please enter a valid prize ID.')
        return
    if not os.path.exists(f"./Giveaways/{guild.id}-{prize_id}-giveaway.txt"):
        await ctx.send('Sorry, but either this giveaway has ended or a giveaway with this ID never existed.')
        return
    if os.path.exists(f"./Giveaways/{guild.id}-{prize_id}-giveaway.txt"):
        with open(f"./Giveaways/{guild.id}-{prize_id}-giveaway.txt") as f2:
            if str(ctx.message.author.id) in f2.read():
                await ctx.send('Sorry, but you already entered this giveaway.')
                return
        f = open(f"./Giveaways/{guild.id}-{prize_id}-giveaway.txt", "a")
        f.write(f"\n{ctx.message.author.id}")
        f.close()
        await ctx.message.author.send('Succesfully entered the giveaway')




@client.command()
@commands.has_permissions(ban_members=True)
async def reroll(ctx, prize_id: int = None):
    guild = ctx.message.guild
    if prize_id == None:
        await ctx.send('Please enter a valid prize ID.')
        return
    if not os.path.exists(f"./Giveaways/{guild.id}-{prize_id}-giveaway.txt"):
        await ctx.send('Sorry, but a giveaway with that ID does not exist.')
        return
    if os.path.exists(f"./Giveaways/{guild.id}-{prize_id}-giveaway.txt"):
        lines = open(f"./Giveaways/{guild.id}-{prize_id}-giveaway.txt").read().splitlines()
        winner_id = random.choice(lines)
        winner = await client.fetch_user(winner_id)
        await ctx.send(f'**New Winner(s):** {winner.mention}')
        return
    


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Error: command not found...')
        return
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(F"Sorry, but you don't have permissions to do this action.")
        return
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send(F"Sorry, but I don't have permissions to do this action.")
        return



client.run(TOKEN)
