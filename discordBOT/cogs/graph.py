import discord
from discord.ext import commands
from setup import *
import numpy as np
from datetime import date
from datetime import timedelta
import matplotlib.pyplot as plt
import io

date_range = []
date_urls = []

#for day in range(30):
    #insertDate = ref_date - timedelta(days = day)
    #insertDate = insertDate.strftime("%m-%d-%Y")
    #date_range.append(insertDate)
    #insertURL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/' \
    #  + str(date_range[day]) + '.csv'
    #date_urls.append(insertURL)

#flip the list in ascending order
date_range = date_range[::-1]
date_urls = date_urls[::-1]

class graph(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Commands
    @commands.command(aliases=['g'])
    async def graph(self, ctx, *, location):
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
        cases = []
        dates = []

        if len(target) == 1:
            # state only
            if target[0] in prov_state:
                dfGraph = confirmedUS_df.loc[(confirmedUS_df['Province_State'] == target[0])]
                for x in range(6, len(dfGraph.columns)):
                    columns = dfGraph.iloc[:, x].sum()
                    dates.append(confirmedUS_df.columns[x])
                    cases.append(columns)
                for x in range(0, len(dates)):
                    slim = dates[x]
                    slim = slim[:-3]
                    dates[x] = slim
                plt.clf()
                fig = plt.figure(figsize=(6, 9))
                plt.style.use('dark_background')
                fig, ax = plt.subplots()
                ax.plot(dates, cases)
                plt.xticks(dates[::7])
                fig.autofmt_xdate()
                plt.savefig('images/graph.png', transparent=True)
                plt.close(fig)
            # country only:
            if target[0] in country_Region:
                dfGraph = confirmedGLob_df.loc[(confirmedGLob_df['Country/Region'] == target[0])]
                for x in range(6, len(dfGraph.columns)):
                    columns = dfGraph.iloc[:, x].sum()
                    dates.append(confirmedGLob_df.columns[x])
                    cases.append(columns)
                for x in range(0, len(dates)):
                    slim = dates[x]
                    slim = slim[:-3]
                    dates[x] = slim
                plt.clf()
                fig = plt.figure(figsize=(6, 9))
                plt.style.use('dark_background')
                fig, ax = plt.subplots()
                ax.plot(dates, cases)
                plt.xticks(dates[::7])
                fig.autofmt_xdate()
                plt.savefig('images/graph.png', transparent=True)
                plt.close(fig)

        if len(target) == 2:
            # county, state in US
            if target[0] in county_US and target[1] in prov_state:
                dfGraph = confirmedUS_df.loc[(confirmedUS_df['Province_State'] == target[1])
                                             & (confirmedUS_df['Admin2'] == target[0])]
                for x in range(6, len(dfGraph.columns)):
                    columns = dfGraph.iloc[:, x].sum()
                    dates.append(confirmedUS_df.columns[x])
                    cases.append(columns)
                for x in range(0, len(dates)):
                    slim = dates[x]
                    slim = slim[:-3]
                    dates[x] = slim
                plt.clf()
                fig = plt.figure(figsize=(6, 9))
                plt.style.use('dark_background')
                fig, ax = plt.subplots()
                ax.plot(dates, cases)
                plt.xticks(dates[::7])
                fig.autofmt_xdate()
                plt.savefig('images/graph.png', transparent=True)
                plt.close(fig)

            # providence, country
            if target[0] in prov_state and target[1] in country_Region:
                dfGraph = confirmedGLob_df.loc[(confirmedGLob_df['Province/State'] == target[0])
                                               & (confirmedGLob_df['Country/Region'] == target[1])]
                for x in range(6, len(dfGraph.columns)):
                    columns = dfGraph.iloc[:, x].sum()
                    dates.append(confirmedUS_df.columns[x])
                    cases.append(columns)
                for x in range(0, len(dates)):
                    slim = dates[x]
                    slim = slim[:-3]
                    dates[x] = slim
                plt.clf()
                fig = plt.figure(figsize=(6, 9))
                plt.style.use('dark_background')
                fig, ax = plt.subplots()
                ax.plot(dates, cases)
                plt.xticks(dates[::7])
                fig.autofmt_xdate()
                plt.savefig('images/graph.png', transparent=True)
                plt.close(fig)

        with open('images/graph.png', 'rb') as f:
            file = io.BytesIO(f.read())

        image = discord.File(file, filename='graph.png')
        embed = discord.Embed(title=location)
        embed.set_image(url=f'attachment://graph.png')
        await ctx.send(file=image, embed=embed)

    @commands.command(aliases=[])
    async def loggraph(self, ctx, *, location):
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
        cases = []
        dates = []

        if len(target) == 1:
            # state only
            if target[0] in prov_state:
                dfGraph = confirmedUS_df.loc[(confirmedUS_df['Province_State'] == target[0])]
                for x in range(6, len(dfGraph.columns)):
                    columns = dfGraph.iloc[:, x].sum()
                    dates.append(confirmedUS_df.columns[x])
                    cases.append(columns)
                for x in range(0, len(dates)):
                    slim = dates[x]
                    slim = slim[:-3]
                    dates[x] = slim
                plt.clf()
                fig = plt.figure(figsize=(6, 9))
                plt.style.use('dark_background')
                fig, ax = plt.subplots()
                ax.plot(dates, cases)
                plt.yscale('log')
                plt.xticks(dates[::7])
                fig.autofmt_xdate()
                plt.savefig('images/graph.png', transparent=True)
                plt.close(fig)
            # country only:
            if target[0] in country_Region:
                dfGraph = confirmedGLob_df.loc[(confirmedGLob_df['Country/Region'] == target[0])]
                for x in range(6, len(dfGraph.columns)):
                    columns = dfGraph.iloc[:, x].sum()
                    dates.append(confirmedGLob_df.columns[x])
                    cases.append(columns)
                for x in range(0, len(dates)):
                    slim = dates[x]
                    slim = slim[:-3]
                    dates[x] = slim
                plt.clf()
                fig = plt.figure(figsize=(6, 9))
                plt.style.use('dark_background')
                fig, ax = plt.subplots()
                ax.plot(dates, cases)
                plt.yscale('log')
                plt.xticks(dates[::7])
                fig.autofmt_xdate()
                plt.savefig('images/graph.png', transparent=True)
                plt.close(fig)

        if len(target) == 2:
            # county, state in US
            if target[0] in county_US and target[1] in prov_state:
                dfGraph = confirmedUS_df.loc[(confirmedUS_df['Province_State'] == target[1])
                                               & (confirmedUS_df['Admin2'] == target[0])]
                for x in range(6, len(dfGraph.columns)):
                    columns = dfGraph.iloc[:, x].sum()
                    dates.append(confirmedUS_df.columns[x])
                    cases.append(columns)
                for x in range(0, len(dates)):
                    slim = dates[x]
                    slim = slim[:-3]
                    dates[x] = slim
                plt.clf()
                fig = plt.figure(figsize=(6, 9))
                plt.style.use('dark_background')
                fig, ax = plt.subplots()
                ax.plot(dates, cases)
                plt.yscale('log')
                plt.xticks(dates[::7])
                fig.autofmt_xdate()
                plt.savefig('images/graph.png', transparent=True)
                plt.close(fig)

            # providence, country
            if target[0] in prov_state and target[1] in country_Region:
                dfGraph = confirmedGLob_df.loc[(confirmedGLob_df['Province/State'] == target[0])
                                             & (confirmedGLob_df['Country/Region'] == target[1])]
                for x in range(6, len(dfGraph.columns)):
                    columns = dfGraph.iloc[:, x].sum()
                    dates.append(confirmedUS_df.columns[x])
                    cases.append(columns)
                for x in range(0, len(dates)):
                    slim = dates[x]
                    slim = slim[:-3]
                    dates[x] = slim
                plt.clf()
                fig = plt.figure(figsize=(6, 9))
                plt.style.use('dark_background')
                fig, ax = plt.subplots()
                ax.plot(dates, cases)
                plt.yscale('log')
                plt.xticks(dates[::7])
                fig.autofmt_xdate()
                plt.savefig('images/graph.png', transparent=True)
                plt.close(fig)

        with open('images/graph.png', 'rb') as f:
            file = io.BytesIO(f.read())

        image = discord.File(file, filename='graph.png')
        embed = discord.Embed(title=location)
        embed.set_image(url=f'attachment://graph.png')
        await ctx.send(file=image, embed=embed)


    @commands.command(aliases=[])
    async def growth(self, ctx, *, location):
        # Grab Data
        confirmedUS_TS = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
        deathsUS_TS = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv'
        confirmedGlob_TS = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
        deathGlob_TS = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
        confirmedUS_df = pd.read_csv(confirmedUS_TS).drop(['FIPS', 'iso2', 'iso3', 'code3', 'UID'], axis=1)
        deathsUS_df = pd.read_csv(confirmedUS_TS).drop(['FIPS', 'iso2', 'iso3', 'code3', 'UID'], axis=1)
        confirmedGLob_df = pd.read_csv(confirmedGlob_TS)
        deathsGlob_df = pd.read_csv(deathGlob_TS)


def setup(bot):
    bot.add_cog(graph(bot))