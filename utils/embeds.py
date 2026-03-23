import discord
import json

with open("config.json") as f:
    config = json.load(f)

COLOR = config["embed_color"]


def success_embed(title, description):
    embed = discord.Embed(
        title=f"✅ {title}",
        description=description,
        color=COLOR
    )
    return embed


def error_embed(title, description):
    embed = discord.Embed(
        title=f"❌ {title}",
        description=description,
        color=COLOR
    )
    return embed


def info_embed(title, description):
    embed = discord.Embed(
        title=f"ℹ️ {title}",
        description=description,
        color=COLOR
    )
    return embed


def stats_embed(title, stats: dict):
    embed = discord.Embed(
        title=title,
        color=COLOR
    )

    for key, value in stats.items():
        embed.add_field(
            name=str(key),
            value=str(value),
            inline=False
        )

    return embed
