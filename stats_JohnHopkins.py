import pandas as pd
from datetime import date
from datetime import timedelta

currentDate = date.today()
previousDate = currentDate - timedelta(days = 1)
currentDate = currentDate.strftime("%m-%d-%Y")
previousDate = previousDate.strftime("%m-%d-%Y")

url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'\
      + str(previousDate) + '.csv'
og_df = pd.read_csv(url, error_bad_lines=False)

# Data frame columns
# FIPS | Admin2 | Province_State | Country_Region | Last_Update | Lat | Long_ | Confirmed | Deaths | Recovered | Active | Combined_Key

Coun_Reg = input("Enter your Country: ")
Prov_State = input("Enter your state: ")
df = og_df.drop(['FIPS', 'Combined_Key'], axis=1)
confirmedStateTotal = df['Confirmed'][df.Province_State == Prov_State].sum()
confirmedRegionTotal = df['Confirmed'][df.Country_Region == Coun_Reg].sum()

print("Confirmed: " + str(confirmedRegionTotal))
print("Confirmed: " + str(confirmedStateTotal))