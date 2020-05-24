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
   # await  client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Giveaways | ?help'))
   print(f"Logged in as {client.user} (ID: {client.user.id})")


# Standart help command
@client.command()
async def help(ctx):
    msg = ctx.message.channel.last_message
    await msg.add_reaction('<:Party:714144280142151692>')
    await ctx.message.author.send(f"<:Party:714144280142151692> **__Giveaways commands:__** \n \n**?invite** - get an invite link for the bot \n**?ping** - shows the bot's latency \n**?help** - shows this help message \n \n<:Party:714144280142151692> **__Host a Giveaway__:** \n \n**?start <duration in hours> <prize>** - starts a giveaway in the current channel \n**?end <message ID>** - ends the specified giveaway \n**?reroll <message ID>** - re-rolls the specified giveaway \n**?past** - shows a list of the past giveaways \n \n`< >` indicates required arguments.")



@client.event
async def on_guild_join(guild):
    past_giveaway_list = open(f"./PastGiveaways/{guild.id}-past-giveaways.txt", "w")
    past_giveaway_list.write(f"`{guild.name}`")
    past_giveaway_list.close()


def file_len(fname): # get lenght of a file 
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1



@client.command()
async def ping(ctx):
    msg = await ctx.send('<a:Loading:714147946932732025> Loading...')
    await asyncio.sleep(3)
    await msg.edit(content=f"Current ping: **{round (client.latency * 1000)}ms**")

 

@client.command()
@commands.has_permissions(ban_members=True)
async def start(ctx, atime: int = None, *, prize = None):
    max_time = 48
    if atime == None:
        await ctx.send('Error: enter a valid time.')
        return
    if prize == None:
        await ctx.send('Error: enter a valid prize.')
        return
    if atime >= max_time:
        await ctx.send('Error: max time is 48 hours.')
        return
    hours = atime - 2
    ts = datetime.datetime.now() + datetime.timedelta(hours=hours)
    e = discord.Embed(color=0x2BFF06, title=f"{prize}", description=f'React with 🎉 to enter this giveaway! \nTime: **{atime}** hour(s) \nHosted by: {ctx.message.author.mention}', timestamp=ts)
    e.set_footer(text="Ends at")
    msg = await ctx.send(embed=e)
    await msg.add_reaction('🎉')
    jump = msg.jump_url
    f = open(f"./Giveaways/{msg.id}-test.txt", "w")
    f.write(f"{ctx.message.author.id}")
    f.close()
    await asyncio.sleep(atime * 3600)
    at = file_len(f"./Giveaways/{msg.id}-test.txt")
    if not os.path.exists(f"./Giveaways/{msg.id}-test.txt"):
        await msg.edit(f"This giveaway has been canceled! \n{jump}")
        return
    if os.path.exists(f"./Giveaways/{msg.id}-test.txt"):
        if at <= 1:
            await ctx.send(f'Sorry, but there have to be at least 3 attendees to make a giveaway. Only **{at}** user(s) entered this giveaway. \n{jump}')
            open(f"./Giveaways/{msg.id}-test.txt", 'w').close()
            await asyncio.sleep(1)
            os.remove(f"./Giveaways/{msg.id}-test.txt") 
            return
        lines = open(f"./Giveaways/{msg.id}-test.txt").read().splitlines()
        winner_id = random.choice(lines)
        winner = await client.fetch_user(winner_id)
        e1 = discord.Embed(color=0xF30700, title=f"{prize}", description=f"Giveaway has ended! \n \n**Winner:** {winner.mention}", timestamp=ts)
        e1.set_footer(text="Ended at")
        await asyncio.sleep(int(atime) * 10)
        await msg.edit(embed=e1)
        await ctx.send(f"🎉 Congratulations {winner.mention} you won **{prize}**")
        await asyncio.sleep(1)
        await ctx.message.author.send(f"Giveaway **{prize}** has ended. If you want to reroll this giveaway, you have 1 hour to do so. \n{jump}")
        await asyncio.sleep(3600)
        open(f"./Giveaways/{msg.id}-test.txt", 'w').close()
        await asyncio.sleep(1)
        os.remove(f"./Giveaways/{msg.id}-test.txt")
        past_giveaway_list = open(f"./PastGiveaways/{guild.id}-past-giveaways.txt", "a")
        past_giveaway_list.write(f"\n \n`{prize}`")
        past_giveaway_list.close()



@client.command()
@commands.has_permissions(ban_members=True)
async def end(ctx, msg_id: int = None):
    if msg_id == None:
        await ctx.send('Please enter a valid giveaway ID.')
        return
    if not os.path.exists(f"./Giveaways/{msg_id}-test.txt"):
        await ctx.send('Sorry, but either this giveaway has ended or a giveaway with this ID never existed.')
        return
    if os.path.exists(f"./Giveaways/{msg_id}-test.txt"):
        open(f"./Giveaways/{msg_id}-test.txt", 'w').close()
        os.remove(f"./Giveaways/{msg_id}-test.txt")
        await ctx.send(f'Succesfully ended the giveaway! (**{msg_id}**)')
        return



@client.command()
@commands.has_permissions(ban_members=True)
async def reroll(ctx, msg_id: int = None):
    if msg_id == None:
        await ctx.send('Please enter a valid prize ID.')
        return
    if not os.path.exists(f"./Giveaways/{msg_id}-test.txt"):
        await ctx.send('Sorry, but a giveaway with that ID does not exist.')
        return
    if os.path.exists(f"./Giveaways/{msg_id}-test.txt"):
        lines = open(f"./Giveaways/{msg_id}-test.txt").read().splitlines()
        winner_id = random.choice(lines)
        winner = await client.fetch_user(winner_id)
        await ctx.send(f'**New Winner(s):** {winner.mention}')
        open(f"./Giveaways/{msg_id}-test.txt", 'w').close()
        os.remove(f"./Giveaways/{msg_id}-test.txt")
        return



@client.command()
@commands.has_permissions(ban_members=True)
async def past(ctx):
    guild = ctx.message.guild
    past_giveaway_list = open(f"./PastGiveaways/{guild.id}-past-giveaways.txt", "r")
    past_giveaways = past_giveaway_list.read()
    embed = discord.Embed(color=0x7289DA, description=f"{past_giveaways}")
    embed.set_author(name='Past Giveaways', icon_url=guild.icon_url)
    await ctx.send(embed=embed)




@client.command()
async def invite(ctx):
    await ctx.send('<:Party:714144280142151692> You want to invite **Giveaways** to your server? \nYou can do that by simply using this link! \n \n🔗 **<https://discord.com/oauth2/authorize?client_id=710271590411010092&permissions=268823616&scope=bot>**')





@client.command()
@commands.is_owner()
async def oss(ctx):
    await ctx.send(f"GitHub Repo: https://github.com/EzZz1337/Giveaway-Bot")



@client.command()
@commands.is_owner()
async def guilds(ctx):
    await ctx.send(f"Guilds: **{len(client.guilds)}** \nUsers: **{len(set(client.get_all_members()))}**")



@client.event
async def on_reaction_add(reaction, user):
    msg = reaction.message
    if not os.path.exists(f"./Giveaways/{msg.id}-test.txt"):
        return
    if os.path.exists(f"./Giveaways/{msg.id}-test.txt"):
        with open(f"./Giveaways/{msg.id}-test.txt") as f2:
            if str(user.id) in f2.read():
                return
        f = open(f"./Giveaways/{msg.id}-test.txt", "a")
        f.write(f"\n{user.id}")
        return
    


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(F"Error: missing user permissions.")
        return
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send(F"Error: missing bot permissions.")
        return



client.run(TOKEN)
