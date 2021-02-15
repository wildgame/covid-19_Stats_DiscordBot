# Setup
import urllib.request
import urllib.error
import pandas as pd
from datetime import date
from datetime import timedelta
import string
import re


# Data frame columns
# FIPS|Admin2|Province_State|Country_Region|Last_Update|Lat|Long|Confirmed|Deaths|Recovered|Active |Combined_Key

# FUNCTIONS
#---------------------------------------------------------------
# Grabbing Current and Previous Date
def grab_date():
    currentDate = date.today()
    previousDate = currentDate - timedelta(days=1)
    currentDate = currentDate.strftime("%m-%d-%Y")
    previousDate = previousDate.strftime("%m-%d-%Y")
    datedict = {"today": currentDate, "yesterday": previousDate}
    return datedict


# verify today's .csv
def latestData(url):
    try:
        conn = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        return '{}'.format(e.code)  # site returns error code
    else:
        return 200  # site is up


# get day's link
def grab_link(today, yesterday):
    currentDate = today
    previousDate = yesterday
    currentData_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/' \
                      + str(currentDate) + '.csv'
    if latestData(currentData_url) == 200:
        previousData_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/' \
                           + str(previousDate) + '.csv'
        ref_date = date.today()
    else:
        previousDate1 = date.today() - timedelta(days=2)
        previousDate1 = previousDate1.strftime("%m-%d-%Y")
        currentData_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/' \
                          + str(previousDate) + '.csv'
        previousData_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/' \
                           + str(previousDate1) + '.csv'
        ref_date = date.today() - timedelta(days=1)
        return [previousData_url, currentData_url, ref_date]


def grab_location(location):
    location = string.capwords(location)  # Uppercase the beginning of all the words in location
    m = re.search(',', location)
    if m:  # if location has two inputs
        location = location.split(',')
        location = [re.sub(r"^[ ]*", "", word) for word in location]
        if (len(location[1])) == 2:
            location[1] = location[1].upper()
    else:  # one input location
        location = [location]
    return location


sampleD = grab_date()
sampleL = grab_link(*sampleD)
dfs = pd.read_csv(sampleL[0], error_bad_lines=False)

country_Region = []
prov_state = []
county_US = []

for r in dfs['Country_Region']:
    if r not in country_Region:
        country_Region.append(r)

for c in dfs['Province_State']:
    if c not in prov_state:
        prov_state.append(c)

for c in dfs['Admin2']:
    if c not in county_US:
        county_US.append(c)
