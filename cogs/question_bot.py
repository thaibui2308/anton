from discord.ext import commands
import discord

from services.wolfram_service import free_form_question, scientific_question, short_answer

class QuestionBot(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(aliases=['ask'])
    async def free_form_question(self, ctx, *args):
        if len(args) == 0:
            await ctx.send("Please provide a question.")
        else:
            answer = free_form_question('{}'.format(' '.join(args)))
            if not answer:
                await ctx.send("I can not answer this question!")
            else:
                embed = discord.Embed(title='{}'.format(' '.join(args)), color=discord.Color.red())
                embed.add_field(name='Answer', value=answer)
                
                await ctx.send(embed=embed)
                
    @commands.command(aliases=['solve'])
    async def equation_solver(self, ctx, *args):
        if len(args) == 0:
            await ctx.send("Please provide a valid equation")
        else:
            answer = scientific_question('Solve {}'.format(' '.join(args)))
            if not answer:
                await ctx.send("I can not answer this question!")
            else:
                count = 1
                steps = answer.split('\n')
                embed = discord.Embed(title=steps[0], color=discord.Color.blue())
                for step in steps[1:]:
                    if step.startswith('Answer'):
                        embed.add_field(name='Answer', value=steps[-1]+'|')
                        break
                    embed.add_field(name='Step {}'.format(count), value=step, inline=False)
                    count += 1
                
                await ctx.send(embed=embed)
                
    @commands.command(aliases=['short'])
    async def short_answer(self, ctx, *args):
        if len(args) == 0:
            await ctx.send("Please provide a question.")
        else:
            answer = short_answer('{}'.format(' '.join(args)))
            if not answer:
                await ctx.send("I can not answer this question!")
            else:
                embed = discord.Embed(title='{}'.format(' '.join(args)), color=discord.Color.green())
                embed.add_field(name='Answer', value=answer)
                
                await ctx.send(embed=embed)

def setup(client):
    client.add_cog(QuestionBot(client))