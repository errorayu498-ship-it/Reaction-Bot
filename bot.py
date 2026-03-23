import discord
from discord.ext import commands
import json
import os
import asyncio
from dotenv import load_dotenv

from core.token_manager import TokenManager
from core.reaction_manager import ReactionManager
from core.server_manager import ServerManager
from utils.embeds import *

load_dotenv()

TOKEN = os.getenv("MAIN_BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

with open("config.json") as f:
    config = json.load(f)

prefix = config["prefix"]

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix=prefix, intents=intents)

token_manager = TokenManager()
reaction_manager = ReactionManager(token_manager)
server_manager = ServerManager(token_manager)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Latency: {round(bot.latency*1000)}ms")


# ---------------- HELP ---------------- #

@bot.command()
async def help(ctx):

    tokens = token_manager.count_tokens()

    embed = discord.Embed(
        title="Bot Control Panel",
        color=config["embed_color"]
    )

    embed.add_field(name="Prefix", value=prefix)
    embed.add_field(name="Tokens Loaded", value=tokens)
    embed.add_field(name="Latency", value=f"{round(bot.latency*1000)} ms")

    embed.add_field(
        name="Commands",
        value="""
help
addtoken
tokenstat
joinserver
checkserver
leaveserver
react
stopreact
""",
        inline=False
    )

    embed.set_footer(text=f"Owner: <@{OWNER_ID}>")

    await ctx.send(embed=embed)


# ---------------- ADD TOKENS ---------------- #

@bot.command()
async def addtoken(ctx):

    if ctx.author.id != OWNER_ID:
        return

    await ctx.send("Send tokens (line by line). Type `done` when finished.")

    tokens = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    while True:
        msg = await bot.wait_for("message", check=check)

        if msg.content.lower() == "done":
            break

        tokens.append(msg.content)

    added = token_manager.add_tokens(tokens)

    await ctx.send(f"Added {added} tokens.")


# ---------------- TOKEN STATUS ---------------- #

@bot.command()
async def tokenstat(ctx):

    results = await token_manager.check_tokens()

    working = sum(1 for r in results if r)
    dead = len(results) - working

    embed = discord.Embed(
        title="Token Status",
        color=config["embed_color"]
    )

    embed.add_field(name="Working", value=working)
    embed.add_field(name="Invalid", value=dead)

    await ctx.send(embed=embed)


# ---------------- JOIN SERVER ---------------- #

@bot.command()
async def joinserver(ctx, invite):

    msg = await ctx.send("Joining servers...")

    stats = await server_manager.join_servers(invite)

    embed = discord.Embed(
        title="Join Results",
        color=config["embed_color"]
    )

    embed.add_field(name="Joined", value=stats["joined"])
    embed.add_field(name="Failed", value=stats["failed"])

    await msg.edit(embed=embed)


# ---------------- REACT ---------------- #

@bot.command()
async def react(ctx, message_id: int, emoji):

    await ctx.send("Starting reactions...")

    await reaction_manager.start(ctx.channel.id, message_id, emoji)


# ---------------- STOP REACT ---------------- #

@bot.command()
async def stopreact(ctx):

    reaction_manager.stop()

    await ctx.send("Reaction stopped.")


bot.run(TOKEN)
