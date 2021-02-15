from discord.ext import commands
from setup import *
import numpy as np
from datetime import date
from datetime import timedelta
import matplotlib.pyplot as plt
import re

class graph(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Commands
    @commands.command(aliases=['7','mva'])
    async def movingaverage(self, ctx, *, location):

        # Grab Data
        confirmedUS_TS = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
        deathsUS_TS = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv'
        confirmedGlob_TS = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
        deathGlob_TS = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
        confirmedUS_df = pd.read_csv(confirmedUS_TS).drop(['FIPS', 'iso2', 'iso3', 'code3', 'UID'], axis=1)
        deathsUS_df = pd.read_csv(confirmedUS_TS).drop(['FIPS', 'iso2', 'iso3', 'code3', 'UID'], axis=1)
        confirmedGLob_df = pd.read_csv(confirmedGlob_TS)
        deathsGlob_df = pd.read_csv(deathGlob_TS)

        target = grab_location(location)

        if len(target) == 1:
            #state only
            if target[0] in prov_state:
                pass
            #country only:
            if target[0] in country_Region:
                pass

        if len(target) == 2:
            # county, state in US
            if target[0] in county_US and target[1] in prov_state:
                pass

            # providence, country
            if target[0] in prov_state and target[1] in country_Region:
                pass

        await ctx.send(f"{location[0]}")


def setup(bot):
    bot.add_cog(graph(bot))