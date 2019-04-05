import os
import discord
import json
from discord.ext import commands

os.chdir(r"C:\Users\Miro\Desktop\DiscordBots\Ada")


def isDonald(ctx):
    return ctx.message.author.id == "289890066514575360"

def isOwner(ctx):
    return ctx.message.author == ctx.message.server.owner

def isStaff(ctx):
    with open('adaconfig.json') as f:
        config = json.load(f)
    return config.get('staffid') in [y.id for y in ctx.message.author.roles] or ctx.message.author.id in config.get("ownerid") or config.get('adminid') in [y.id for y in ctx.message.author.roles]

def isAdmin(ctx):
    with open('adaconfig.json') as f:
        config = json.load(f)
    return config.get('adminid') in [y.id for y in ctx.message.author.roles] or ctx.message.author.id in config.get("ownerid")
