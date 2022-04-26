from discord.ext import commands
import discord
from hentai import Tag, Format, Hentai
from emoji import EMOJI_ALIAS_UNICODE_ENGLISH as Emoji

from services.hentai_service import getHentaiById, getPopularHentaisByTag, getRandomHentai

class HentaiBot(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_reaction_add(self,reaction, user):
        message = reaction.message
        message_content = message.embeds[0].to_dict()
        
        # Check if the one who reacted is a bot or nah
        if not user.bot and (len(message_content['fields']) >= 4) and message_content['fields'][3]['value'] == 'Read':
            # TODO: remove these two lines after the bot is done
            
            # If the user wants to read the next page
            if reaction.emoji == '➡️':
                # Change the Current Page field 
                for field in message_content['fields']:
                    if field['name'] == 'Current Page':
                        Current_Page = int(field['value'])
                        
                        # Check if the current page is equal to the total page number
                        if Current_Page == int(message_content['fields'][2]['value']):
                            break
                        else:
                            field['value'] = str(Current_Page+1)
                            # Change the image url based on the Current Page field
                            hentaiResult = Hentai(int(message_content['fields'][2]['value']))
                            message_content['image']['url'] = hentaiResult.image_urls[Current_Page+1]
            
            # If the user wants to go back to the previous page
            if reaction.emoji == '⬅️':
                Current_Page = int(message_content['fields'][0]['value'])
                
                # Check if the current page is the first page or nah
                if Current_Page == 1:
                    await message.edit(embed=message_content)
                else:
                    message_content['fields'][0]['value'] = str(Current_Page-1)
                    # Change the image url based on the current page
                    hentaiResult = Hentai(int(message_content['fields'][2]['value']))
                    message_content['image']['url'] = hentaiResult.image_urls[Current_Page-1]
            
            # Change the description header of the message
            curr = message_content['fields'][0]['value']
            total = message_content['fields'][1]['value']
            
            message_content['description'] = 'Page {} of {}'.format(curr, total)
            
            embed = discord.Embed.from_dict(message_content)
            
            # Remove the reaction so users can click it many time
            await message.remove_reaction(reaction.emoji, user)
            await message.edit(embed=embed)
            
        
    
    @commands.command(aliases=['look'])
    async def hlookup(self, ctx, id):
        result = getHentaiById(id)
        if result is False:
            await ctx.send("Invalid id: {}".format(id))
        
        embed = discord.Embed(title=result.title(Format.Pretty),  url=result.url, color=discord.Color.red())
        embed.add_field(name="Author", value=Tag.get(result.artist, 'name'))
        embed.add_field(name="Favorites", value=f"❤ {result.num_favorites}")
        embed.add_field(name="Pages", value=f"📕 {result.num_pages}")
        embed.set_thumbnail(url=result.thumbnail)
        # embed.set_footer(text=f"Tags: {', '.join(Tag.get_names(result.tag))}")
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(f"Now reading {result.title(Format.Pretty)}🥰"))
        await ctx.send(embed=embed)   
    
    #TODO: add command for generating random hentai and get the most popular hentai of the week
    
    @commands.command(aliases=['read'])
    async def read_id(self, ctx, id: int):
        if getHentaiById(id) is False:
            await ctx.send("Error: Invalid ID.")
        else:
            doujin = getHentaiById(id)
            reactions = {
                'prev' : Emoji[':arrow_left:'],
                'next' : Emoji[':arrow_right:']
            }

            embed = discord.Embed(title=doujin.title(Format.Pretty), description=f"Page 1 of {doujin.num_pages}", color=discord.Color.red())
            embed.set_image(url=doujin.image_urls[0])
            embed.add_field(name="Current Page",value=1)
            embed.add_field(name="Total Pages",value=doujin.num_pages)
            embed.add_field(name="ID", value = id)
            embed.add_field(name="Action", value='Read')
            
            # TODO: implement emoji reaction event handler for pagination
            message = await ctx.send(embed=embed)
            self.reader_id = message.id
            
            for emoji in reactions.values():
                await message.add_reaction(emoji)
   
    @commands.command(aliases=['rand'])
    async def get_random(self, ctx):
        result = getRandomHentai()
        
        embed = discord.Embed(title=result.title(Format.Pretty),  url=result.url, color=discord.Color.red())
        
        embed.add_field(name="Author", value=Tag.get(result.artist, 'name'))
        embed.add_field(name="Favorites", value=f"❤ {result.num_favorites}")
        embed.add_field(name="Pages", value=f"📕 {result.num_pages}")
        embed.set_thumbnail(url=result.thumbnail)
        
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(f"Now reading {result.title(Format.Pretty)}🥰"))
        await ctx.send(embed=embed)   
        
    @commands.command(aliases=['list'])
    async def get_popular_items(self, ctx, tag):
        items = getPopularHentaisByTag(tag)
        
        if len(items) == 0: 
            await ctx.send("Couldn't find anything with this tag: {0}".format(tag))
            
        else:
            count = 1
            embed = discord.Embed(title='Top {0}'.format(len(items)), color=discord.Color.blue())
            for item in items:
                embed.add_field(name='{0}'.format(count), value=item.title(Format.Pretty), inline= False)
                count += 1
            embed.set_thumbnail(url="https://ih1.redbubble.net/image.536624306.1571/flat,750x,075,f-pad,750x1000,f8f8f8.u1.jpg")
            await ctx.send(embed=embed)
        
        

def setup(client):
    client.add_cog(HentaiBot(client))