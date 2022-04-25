from ast import arg
import discord 
from discord import client 
import os
from discord.ext import commands

class Helper(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is up and running!')
        
    @commands.command(aliases=['h'])
    async def helper(self, ctx):
        embed = discord.Embed(title="Commands", color=discord.Color.dark_orange())
        embed.add_field(name="$look id:int", value='Lookup an user-specified ID', inline=False)
        embed.add_field(name="$read id:int", value='Read an user-specified ID in chat', inline=False)
        embed.add_field(name="$rand", value='Roll a random ID', inline=False)
        embed.add_field(name="$list tag:string", value='Generate a list of 25 popular hentai of the week', inline=False)
        
        await ctx.send(embed=embed)
        
        

def setup(client):
    client.add_cog(Helper(client))