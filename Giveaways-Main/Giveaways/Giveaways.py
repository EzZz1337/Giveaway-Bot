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
    msg = ctx.message.channel.last_message
    await msg.add_reaction('<:Party:714144280142151692>')
    await ctx.message.author.send(f"<:Party:714144280142151692> **__Giveaways commands:__** \n \n**?invite** - get an invite link for the bot \n**?ping** - shows the bot's latency \n**?info** - shows some info about the bot \n**?help** - shows this help message \n \n<:Party:714144280142151692> **__Host a Giveaway__:** \n \n**?start <duration in hours> <amount of winners> <prize>** - starts a giveaway in the current channel \n**?end <message ID>** - ends the specified giveaway \n**?reroll <message ID>** - re-rolls the specified giveaway \n**?past** - shows a list of the past giveaways \n \n`< >` indicates required arguments. \nMax time: `48 hours` | Max amount of winners: `10` \nWebsite: https://giveaways--ezzz1337.repl.co")



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



def get_giveaway_amount(Directory): # get giveaway amount
    amount = [name for name in os.listdir(Directory) if os.path.isfile(os.path.join(Directory, name))]
    return len(amount)


@client.command()
async def info(ctx):
    giveaway_amount = get_giveaway_amount('./Giveaways')
    await ctx.send(f"<:Party:714144280142151692> **__Info about Giveaways#3716__** \n \nName: **{client.user}** \nID: **{client.user.id}** \nMention: {client.user.mention} \nCreator: **EzZz#0001** \nWebsite: **https://giveaways--ezzz1337.repl.co** \n \n<:Party:714144280142151692> **__Stats__** \n \nGuilds: **{len(client.guilds)}** \nUsers: **{len(set(client.get_all_members()))}** \nGiveaways: **{round(giveaway_amount/2)} right now**")




@client.command()
async def ping(ctx):
    msg = await ctx.send('<a:Loading:714147946932732025> Loading...')
    await asyncio.sleep(3)
    await msg.edit(content=f"Current ping: **{round (client.latency * 1000)}ms**")

 

@client.command()
@commands.has_permissions(ban_members=True)
async def start(ctx, atime: int = None, winners: int = None, *, prize = None):
    guild = ctx.message.guild
    max_time = 48
    max_winners = 10
    if atime == None:
        await ctx.send('Error: enter a valid time. (1 - 48)')
        return
    if prize == None:
        await ctx.send('Error: enter a valid prize.')
        return
    if atime > max_time:
        await ctx.send('Error: max time is 48 hours.')
        return
    if winners == None:
        await ctx.send('Error: please enter a valid amount of winners. (1 - 10)')
        return
    if winners > max_winners:
        await ctx.send('Error: max amount of winners is 10.')
        return
    hours = atime - 2
    ts = datetime.datetime.now() + datetime.timedelta(hours=hours)
    e = discord.Embed(color=0x7289DA, title=f"{prize}", description=f'React with 🎉 to enter this giveaway! \nWinners: **{winners}** \nTime left: **{atime}** hour(s) \nHosted by: {ctx.message.author.mention}', timestamp=ts)
    e.set_footer(text="Ends at")
    msg = await ctx.send(embed=e)
    await msg.add_reaction('🎉')
    jump = msg.jump_url
    f = open(f"./Giveaways/{guild.id}-{msg.id}-test.txt", "w")
    f.write(f"{ctx.message.author.id}")
    f.close()
    f10 = open(f"./Giveaways/{guild.id}-{msg.id}-winners.txt", "w")
    f10.write(f'{winners}')
    f10.close()
    dur = atime
    while dur > 0:
        dur -= 1
        await asyncio.sleep(3600)
        e2 = discord.Embed(color=0x7289DA, title=f"{prize}", description=f'React with :tada: to enter this giveaway! \nWinners: **{winners}** \nTime left: **{dur}** hour(s) \nHosted by: {ctx.message.author.mention}', timestamp=ts)
        e2.set_footer(text="Ends at")
        await msg.edit(embed=e2)
        if dur == 0:
            break
    at = file_len(f"./Giveaways/{guild.id}-{msg.id}-test.txt")
    if at <= winners:
        await ctx.send(f'Sorry, but a winner could not be determinated. (Not enogh attendees) \n{jump}')
        open(f"./Giveaways/{guild.id}-{msg.id}-test.txt", 'w').close()
        open(f"./Giveaways/{guild.id}-{msg.id}-winners.txt", 'w').close()
        await asyncio.sleep(1)
        e = discord.Embed(color=0x36393f, title=f"{prize}", description=f"Giveaway has been canceled! \nNot enough attendees (**{at}**)")
        await msg.edit(embed=e)
        os.remove(f"./Giveaways/{guild.id}-{msg.id}-test.txt")
        os.remove(f"./Giveaways/{guild.id}-{msg.id}-winners.txt")
        return
    lines = open(f"./Giveaways/{guild.id}-{msg.id}-test.txt").read().splitlines() #all
    winner_ids = random.sample(lines, winners) #winners
    def filterWinners(toFilter):
        if(toFilter in winner_ids):
            return True
        else:
            return False
    filtered_winners = filter(filterWinners, lines)
    for winner_id in filtered_winners:
        winner = await client.fetch_user(winner_id)
        winners_msg = await ctx.send(f"🎉 Congratulations {winner.mention} you won **{prize}**")
        link = winners_msg.jump_url
        e1 = discord.Embed(color=0x36393f, title=f"{prize}", description=f"Giveaway has ended! \nWinners: [here]({link})", timestamp=ts)
        e1.set_footer(text="Ended at")
        await msg.edit(embed=e1)
    await asyncio.sleep(1)
    await ctx.message.author.send(f"Giveaway **{prize}** has ended. If you want to reroll this giveaway, you have 1 hour to do so. \n{jump}")
    await asyncio.sleep(3600)
    open(f"./Giveaways/{guild.id}-{msg.id}-test.txt", 'w').close()
    open(f"./Giveaways/{guild.id}-{msg.id}-winners.txt", 'w').close()
    await asyncio.sleep(1)
    os.remove(f"./Giveaways/{guild.id}-{msg.id}-test.txt")
    os.remove(f"./Giveaways/{guild.id}-{msg.id}-winners.txt", 'w')
    past_giveaway_list = open(f"./PastGiveaways/{guild.id}-past-giveaways.txt", "a")
    past_giveaway_list.write(f"\n \n`{prize}`")
    past_giveaway_list.close()
    return



@client.command()
@commands.has_permissions(ban_members=True)
async def end(ctx, msg_id: int = None):
    guild = ctx.message.guild
    if msg_id == None:
        await ctx.send('Please enter a valid message ID.')
        return
    if not os.path.exists(f"./Giveaways/{guild.id}-{msg_id}-test.txt"):
        await ctx.send('Sorry, but either this giveaway has ended or a giveaway with this ID never existed.')
        return
    if os.path.exists(f"./Giveaways/{guild.id}-{msg_id}-test.txt"):
        open(f"./Giveaways/{guild.id}-{msg_id}-test.txt", 'w').close()
        open(f"./Giveaways/{guild.id}-{msg_id}-winners.txt", 'w').close()
        await ctx.send(f'Succesfully ended the giveaway! (**{msg_id}**)')
        os.remove(f"./Giveaways/{guild.id}-{msg_id}-test.txt")
        os.remove(f"./Giveaways/{guild.id}-{msg_id}-winners.txt")
        msg = await ctx.message.channel.fetch_message(msg_id)
        e = discord.Embed(color=0x36393f, description=f"Giveaway has been canceled!")
        await msg.edit(embed=e)
        return



@client.command()
@commands.has_permissions(ban_members=True)
async def reroll(ctx, msg_id: int = None):
    guild = ctx.message.guild
    if msg_id == None:
        await ctx.send('Please enter a valid message ID.')
        return
    if not os.path.exists(f"./Giveaways/{guild.id}-{msg_id}-test.txt"):
        await ctx.send('Sorry, but a giveaway with that ID does not exist.')
        return
    if os.path.exists(f"./Giveaways/{guild.id}-{msg_id}-test.txt"):
        f10 = open(f"./Giveaways/{guild.id}-{msg_id}-winners.txt", "r")
        winners = f10.readlines()
        counter = 0
        f10.close()
        for line in winners:
            conv_int = int(line)
            counter = counter + conv_int
        at = file_len(f"./Giveaways/{guild.id}-{msg_id}-test.txt")
        if at < counter:
            await ctx.send('Error: Not enough attendees.')
            open(f"./Giveaways/{guild.id}-{msg_id}-test.txt", 'w').close()
            os.remove(f"./Giveaways/{guild.id}-{msg_id}-test.txt")
            msg = await ctx.message.channel.fetch_message(msg_id)
            e = discord.Embed(color=0x36393f, description=f"Giveaway has been canceled! \n \nNot enough attendees (**{at}**).")
            await msg.edit(embed=e)
            return
        pr = open(f"./Giveaways/{guild.id}-{msg_id}-winners.txt", "r")
        kr = pr.readlines()
        pr.close()
        counter = 0
        for line in kr:
            conv_int = int(line)
            counter = counter + conv_int
        lines = open(f"./Giveaways/{guild.id}-{msg_id}-test.txt").read().splitlines() #all
        winner_ids = random.sample(lines, counter) #winners
        def filterWinners(toFilter):
            if(toFilter in winner_ids):
                return True
            else:
                return False
        filtered_winners = filter(filterWinners, lines)
        for winner_id in filtered_winners:
            winner = await client.fetch_user(winner_id)
            await ctx.send(f"🎉 New winner: {winner.mention}")
        open(f"./Giveaways/{guild.id}-{msg_id}-test.txt", 'w').close()
        open(f"./Giveaways/{guild.id}-{msg_id}-winners.txt", 'w').close()
        await asyncio.sleep(1)
        os.remove(f"./Giveaways/{guild.id}-{msg_id}-test.txt")
        os.remove(f"./Giveaways/{guild.id}-{msg_id}-winners.txt")



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
    guild = msg.guild
    bot = client.get_user(710271590411010092)
    if not os.path.exists(f"./Giveaways/{guild.id}-{msg.id}-test.txt"):
        return
    if os.path.exists(f"./Giveaways/{guild.id}-{msg.id}-test.txt"):
        with open(f"./Giveaways/{guild.id}-{msg.id}-test.txt") as f2:
            if str(user.id) in f2.read():
                return
        if user == bot:
            return
        f = open(f"./Giveaways/{guild.id}-{msg.id}-test.txt", "a")
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
