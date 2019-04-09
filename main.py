import discord
import json
from discord.ext import commands
import time
import checks
import data
import os
from discord.ext.commands import CommandNotFound
import random

bot = commands.Bot(command_prefix="?")

ignoredChannels = ["525468552325496848","534786299295694858","538444152354897920"]


bot.remove_command("help")

with open('adaconfig.json') as f:
    config = json.load(f)

#with open('adatoken.json') as f:
    #token = json.load(f)

@bot.event
async def on_ready():
    print('Ready')
    status=config.get('playing')
    await bot.change_presence(game=discord.Game(name=status))

@bot.command(pass_context=True)
@commands.check(checks.isDonald)
async def changeplaying(ctx, *, playing):
    try:
        await bot.change_presence(
        game=discord.Game(
        name=playing)
        )
        data.change_value('adaconfig.json', 'playing', playing)
        e=discord.Embed(
        title="Success! ✅",
        colour=0x00ff00,
        description=(f"""My playing status will be **{playing}**"""))
        await bot.say(embed=e)
    except discord.InvalidArgument as err:
        await bot.say(err)


@bot.listen()
async def on_message(message):
    try:
	if message.channel.id in ignoredChannels:
            return
        if message.author == bot.user:
            return
        if message.author.id == "540536088670896128":
            return
        embed = discord.Embed(title="Message Log",
            colour = 0x828282,
            description=(f"""
                **Sent by:** {message.author.mention}
                **Channel:** {message.channel.mention}
                **Time:** {time.strftime("%a, %d %b %H:%M:%S")}

                **Message:**
                ```{message.content}```
                """))
        await bot.send_message(bot.get_channel(config.get("chatlog")), embed=embed)
    except:
        return

@bot.command(pass_context=True)
@commands.check(checks.isStaff)
async def kick(ctx, target:discord.Member=None, reason=None):
    if target == None:
        await bot.say("please tag the user")
        return
    if reason == None:
        reason = "n/a"

    embed = discord.Embed(title=f"Kick",
        colour = 0xff5d00,
        description=(f"""
            **User:** {target.mention}
            **When:** {time.strftime("%a, %d %b %H:%M:%S")}
            **User ID:** {target.id}
            **Author:** {ctx.message.author.mention}

            **Reason:**
            ```{reason}```

            """))
    await bot.send_message(bot.get_channel(config.get('punishmentlog')), embed=embed)
    globallog = discord.Embed(
    title=f"Server : {ctx.message.server}",
    description=(f"""
    Type of punishment: **Kick**
    Who Punished: {ctx.message.author.mention}
    Who got Punished: {target.mention}
    Time and Date: {time.strftime("%a, %d %b %H:%M:%S")}
    Reason:
    ```{reason}```
    """)
    )
    await bot.send_message(bot.get_channel(mainconfig.get('globalpunishmentlog')), embed=globallog)
    try:
        dm = discord.Embed(title=f"You've been kicked from {ctx.message.server.name}",
            colour = 0xff5d00,
            description=(f"""
                **When:** {time.strftime("%a, %d %b %H:%M:%S")}
                **Moderator:** {ctx.message.author.mention}

                **Reason:**
                ```{reason}```

                """))
        await bot.send_message(target, embed=dm)
    except Exception:
        await bot.send_message(ctx.message.channel, f"I couldn't send the direct message to the user! `{target.id}`")
    await bot.kick(target)
    success = discord.Embed(title=f"{target} has been kicked ✅", description=(f"""**User ID**: {target.id}\n**Reason**:```{reason}```"""))
    await bot.say(embed=success)
    await bot.delete_message(ctx.message)
    time.sleep(5)


# Global Chat Log
@bot.listen()
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.is_private:
        return
    if message.author.id == "540536088670896128":
        return
    server = message.server
    author = message.author
    content = message.content
    globalchatlog = bot.get_channel(config.get('globalchatlog'))
    chatlog = discord.Embed(
    title=f"Server : {server.name}",
    colour=0xada49d,
    description=(f"""
    Server ID: {server.id}
    Author: {author.mention}
    Time and Date: {time.strftime("%a, %d %b %H:%M:%S")}
    
    Message:
    ```{content}```
    """)
    )
    await bot.send_message(globalchatlog, embed=chatlog)


@bot.command(pass_context=True)
@commands.check(checks.isStaff)
async def ban(ctx, target: discord.Member=None, *, reason = None):
    if target == None:
        embedError = discord.Embed(title="Error! ❌", colour = 0xff0000, description=(f"""{ctx.message.author.mention} You need to specify the user you want to ban!"""))
        embedError.set_footer(text="Example: !ban @donald#5800 Spamming")
        await bot.send_message(ctx.message.channel, embed=embedError)
        await bot.delete_message(ctx.message)
        return
    if reason == None:
        reason = "N/A"
    else:
        try:
            embed = discord.Embed(title=f"Ban",
                colour = 0x000000,
                description=(f"""
                    **User:** {target.mention}
                    **When:** {time.strftime("%a, %d %b %H:%M:%S")}
                    **User ID:** {target.id}
                    **Author:** {ctx.message.author.mention}

                    **Reason:**
                    ```{reason}```

                    """))
            await bot.send_message(bot.get_channel(config.get('punishmentlog')), embed=embed)
            globallog = discord.Embed(
            title=f"Server : {ctx.message.server}",
            description=(f"""
            Type of punishment: **Ban**
            Who Punished: {ctx.message.author.mention}
            Who got Punished: {target.mention}
            Time and Date: {time.strftime("%a, %d %b %H:%M:%S")}
            Reason:
            ```{reason}```
            """)
            )
            await bot.send_message(bot.get_channel(config.get('globalpunishmentlog')), embed=globallog)
            try:
                dm = discord.Embed(title=f"You've been banned from {ctx.message.server.name}",
                    colour = 0x000000,
                    description=(f"""
                        **When:** {time.strftime("%a, %d %b %H:%M:%S")}
                        **Moderator:** {ctx.message.author.mention}

                        **Reason:**
                        ```{reason}```

                        """))
                await bot.send_message(target, embed=dm)
            except Exception:
                await bot.send_message(ctx.message.channel, f"I couldn't send the direct message to the user! `{target.id}`")
            await bot.ban(target)
            success = discord.Embed(title=f"{target} has been banned ✅", description=(f"""**User ID**: {target.id}\n**Reason**:```{reason}```"""))
            await bot.say(embed=success)
            await bot.delete_message(ctx.message)
            time.sleep(5)
        except Exception:
            await bot.say("I was unable to ban the passed member.")
            await bot.delete_message(ctx.message)

@bot.command(pass_context=True, aliases=["c"])
@commands.check(checks.isStaff)
async def clear(ctx, amount):
    channel = ctx.message.channel
    messages = []
    async for message in bot.logs_from(channel, limit=int(amount) + 1):
        messages.append(message)
    await bot.delete_messages(messages)
    embed = discord.Embed(colour = 0x029374)
    embed.set_author(name=f"{ctx.message.author} has cleared {amount} messages ✅")
    embed.set_footer(text=ctx.message.channel)
    msg = await bot.send_message(channel, embed=embed)
    time.sleep(1)
    await bot.delete_message(msg)

@bot.command(pass_context=True)
async def help(ctx):
    helpmessage = discord.Embed(
    title="Ada Help.",
    description=(
    """
    Ada is a temporary discord bot while Dom is offline. Ada is usually running at night EU times when Donald is unable to have Dom on.
    There is going to be more features added to Ada when Donald gets to do them.


    **Currently only commands are:**

    `?kick` - Kicks the targeted user
    `?ban` - Bans the targeted user from the server
    `?clear` - Allows to clear messages from the chat.


    **Other features:**

    Punishment Logs,
    Chat Logs,
    Join-Left Logs


    If you have any problems with Ada. Please DM or Tag **donald#5800** if he is in your server.


    """),
    colour=0xcd07f9)
    await bot.send_message(ctx.message.author, embed=helpmessage)
    await bot.say(ctx.message.author.mention + " I've sent you a DM.")


CDMESSAGES = ["It is not time yet.", "'Tis not yet time.", "Not yet.",
"I need more time.", "I am not ready.", "It is not yet time."]

@bot.event
async def on_command_error(error, ctx):
	channel = ctx.message.channel
	if isinstance(error, commands.MissingRequiredArgument):
		await bot.send_message(channel, "You need give me an arugument to work with... ❌")
	elif isinstance(error, commands.BadArgument):
		await bot.send_message(channel, "You gave me a bad argument, I can't work with that. ❌")
	elif isinstance(error, commands.CommandNotFound):
		# This is almost as ugly as Manta on Medusa
		await bot.send_message(channel, "There is no command like this :thinking:")
	elif isinstance(error, commands.CommandOnCooldown):
		await bot.send_message(channel, random.choice(CDMESSAGES) + " (%ss remaining)" % int(error.retry_after))
	elif isinstance(error, commands.NoPrivateMessage):
		await bot.send_message(channel, "Truly, your wish is my command, but that order is not to be issued in secret. It must be invoked in a server.")
	else:
		try:
			await bot.send_message(channel, "I fear some unprecedented disaster has occurred which I cannot myself resolve. Methinks you would do well to consult with Master Donald on this matter.")
		except discord.NotFound:
			await bot.send_message(channel, "I fear some unprecedented disaster has occurred which I cannot myself resolve.")
		if isinstance(error, commands.CommandInvokeError):
			print(repr(error.original))


#TODO TAKE TOKEN OUT WHEN PUSHING INTO GITHUB
bot.run(str(os.environ.get('TOKEN')))
