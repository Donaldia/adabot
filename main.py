import discord
import json
from discord.ext import commands
import time
import os
import checks

bot = commands.Bot(command_prefix="!")

bot.remove_command("help")

with open('adaconfig.json') as f:
    config = json.load(f)

@bot.event
async def on_ready():
    print('Ready')


@bot.listen()
async def on_message(message):
    try:
        if message.author == bot.user:
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
    server = message.server
    author = message.author
    content = message.content
    channel = message.channel
    globalchatlog = bot.get_channel(config.get('globalchatlog'))
    chatlog = discord.Embed(
    title=f"Server : {server.name}",
    description=(f"""
    Server ID: {server.id}
    Author: {author.mention}
    Channel: {channel.mention}
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
    await bot.say("Ada is a temporary bot while Donald is sleeping so he doesn't have to keep his computed on 24/7. Ada is running on Heroku for the time being.")
    await bot.say("Only commands are: `!kick`, `!ban`, `!clear`")
    await bot.say("Everything is still being logged. Every message, every command.")
    await bot.say("Main reason why im not running DOM on heroku is because it wouldn't save all the balance and XP when restarting the bot. But with Ada, it doesn't matter since it's only for emergencies")


bot.run(str(os.environ.get('TOKEN')))
