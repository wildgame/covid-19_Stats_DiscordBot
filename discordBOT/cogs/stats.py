import discord
from discord.ext import commands
from setup import *
import urllib.request
import urllib.error
import pandas as pd
from datetime import date
from datetime import timedelta
import string
import re

class stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Commands
    @commands.command(aliases=['stats', 'Stats'])
    async def data(self, ctx, *, location):
        time = grab_date()
        links = grab_link(**time)
        current_df = pd.read_csv(links[1], error_bad_lines=False)
        previous_df = pd.read_csv(links[0], error_bad_lines=False)
        target = grab_location(location)

        # 1 Input:
        if len(target) == 1:
            embed = discord.Embed(
                color=discord.Color.dark_green(),
                title=f"""Coronavirus Cases for {target[0]}""",
            )
            if target[0] in prov_state:
                print("prov " + str(location))
                currentConfirmedTotal = current_df['Confirmed'][current_df.Province_State == target[0]].sum()
                currentDeathTotal = current_df['Deaths'][current_df.Province_State == target[0]].sum()
                currentRecoveredTotal = current_df['Recovered'][current_df.Province_State == target[0]].sum()
                currentActiveTotal = current_df['Active'][current_df.Province_State == target[0]].sum()

                previousConfirmedTotal = previous_df['Confirmed'][previous_df.Province_State == target[0]].sum()
                previousDeathTotal = previous_df['Deaths'][previous_df.Province_State == target[0]].sum()
                previousRecoveredTotal = previous_df['Recovered'][previous_df.Province_State == target[0]].sum()
                previousActiveTotal = previous_df['Active'][previous_df.Province_State == target[0]].sum()

                cConfirmed = f'**{currentConfirmedTotal}** (+{currentConfirmedTotal - previousConfirmedTotal})'
                cDeath = f'**{currentDeathTotal}** (+{currentDeathTotal - previousDeathTotal})'
                cRecovered = f'**{currentRecoveredTotal}** (+{currentRecoveredTotal - previousRecoveredTotal})'
                cActive = f'**{currentActiveTotal}** (+{currentActiveTotal - previousActiveTotal})'

            elif target[0] in country_Region:
                print("region " + str(location))
                currentConfirmedTotal = current_df['Confirmed'][current_df.Country_Region == target[0]].sum()
                currentDeathTotal = current_df['Deaths'][current_df.Country_Region == target[0]].sum()
                currentRecoveredTotal = current_df['Recovered'][current_df.Country_Region == target[0]].sum()
                currentActiveTotal = current_df['Active'][current_df.Country_Region == target[0]].sum()

                previousConfirmedTotal = previous_df['Confirmed'][previous_df.Country_Region == target[0]].sum()
                previousDeathTotal = previous_df['Deaths'][previous_df.Country_Region == target[0]].sum()
                previousRecoveredTotal = previous_df['Recovered'][previous_df.Country_Region == target[0]].sum()
                previousActiveTotal = previous_df['Active'][previous_df.Country_Region == target[0]].sum()

                cConfirmed = f'**{currentConfirmedTotal}** (+{currentConfirmedTotal - previousConfirmedTotal})'
                cDeath = f'**{currentDeathTotal}** (+{currentDeathTotal - previousDeathTotal})'
                cRecovered = f'**{currentRecoveredTotal}** (+{currentRecoveredTotal - previousRecoveredTotal})'
                cActive = f'**{currentActiveTotal}** (+{currentActiveTotal - previousActiveTotal})'
            else:
                await ctx.send("Location not found")
        if len(target) == 2:
            embed = discord.Embed(
                color=discord.Color.dark_green(),
                title=f"""Coronavirus Cases for {target[0]}, {target[1]}""",
            )
            if target[1] in prov_state:
                print("prov " + str(location))
                currentConfirmedTotal = current_df['Confirmed'][(current_df.Province_State == target[1]) & (current_df.Admin2 == target[0])].sum()
                currentConfirmedTotal = current_df['Confirmed'][(current_df.Province_State == target[1]) & (current_df.Admin2 == target[0])].sum()
                currentDeathTotal = current_df['Deaths'][(current_df.Province_State == target[1]) & (current_df.Admin2 == target[0])].sum()
                currentRecoveredTotal = current_df['Recovered'][(current_df.Province_State == target[1]) & (current_df.Admin2 == target[0])].sum()
                currentActiveTotal = current_df['Active'][(current_df.Province_State == target[1]) & (current_df.Admin2 == target[0])].sum()

                previousConfirmedTotal = previous_df['Confirmed'][(previous_df.Province_State == target[1]) & (previous_df.Admin2 == target[0])].sum()
                previousDeathTotal = previous_df['Deaths'][(previous_df.Province_State == target[1]) & (previous_df.Admin2 == target[0])].sum()
                previousRecoveredTotal = previous_df['Recovered'][(previous_df.Province_State == target[1]) & (previous_df.Admin2 == target[0])].sum()
                previousActiveTotal = previous_df['Active'][(previous_df.Province_State == target[1]) & (previous_df.Admin2 == target[0])].sum()

                cConfirmed = f'**{currentConfirmedTotal}** (+{currentConfirmedTotal - previousConfirmedTotal})'
                cDeath = f'**{currentDeathTotal}** (+{currentDeathTotal - previousDeathTotal})'
                cRecovered = f'**{currentRecoveredTotal}** (+{currentRecoveredTotal - previousRecoveredTotal})'
                cActive = f'**{currentActiveTotal}** (+{currentActiveTotal - previousActiveTotal})'

            elif target[1] in country_Region:
                print("region " + str(location))
                currentConfirmedTotal = current_df['Confirmed'][(current_df.Country_Region == target[1]) & (current_df.Province_State == target[0])].sum()
                currentDeathTotal = current_df['Deaths'][(current_df.Country_Region == target[1]) & (current_df.Province_State == target[0])].sum()
                currentRecoveredTotal = current_df['Recovered'][(current_df.Country_Region == target[1]) & (current_df.Province_State == target[0])].sum()
                currentActiveTotal = current_df['Active'][(current_df.Country_Region == target[1]) & (current_df.Province_State == target[0])].sum()

                previousConfirmedTotal = previous_df['Confirmed'][(previous_df.Country_Region == target[1]) & (current_df.Province_State == target[0])].sum()
                previousDeathTotal = previous_df['Deaths'][(previous_df.Country_Region == target[1]) & (current_df.Province_State == target[0])].sum()
                previousRecoveredTotal = previous_df['Recovered'][(previous_df.Country_Region == target[1]) & (current_df.Province_State == target[0])].sum()
                previousActiveTotal = previous_df['Active'][(previous_df.Country_Region == target[1]) & (current_df.Province_State == target[0])].sum()

                cConfirmed = f'**{currentConfirmedTotal}** (+{currentConfirmedTotal - previousConfirmedTotal})'
                cDeath = f'**{currentDeathTotal}** (+{currentDeathTotal - previousDeathTotal})'
                cRecovered = f'**{currentRecoveredTotal}** (+{currentRecoveredTotal - previousRecoveredTotal})'
                cActive = f'**{currentActiveTotal}** (+{currentActiveTotal - previousActiveTotal})'
            else:
                await ctx.send("Location not found")


        embed.add_field(name = 'Confirmed: ', value= cConfirmed , inline = True)
        embed.add_field(name = 'Deaths: ', value= cDeath, inline = True)
        embed.add_field(name = 'Recovered: ', value= cRecovered, inline = True)
        embed.add_field(name = 'Active: ', value= cActive, inline = True)

        embed.set_footer(text=f'''All data is sourced from John Hopkins University | Data from {time.get("yesterday")}
                                \nThis bot is purely for educational purposes.''')

        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(stats(bot))