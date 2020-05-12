import pandas as pd, numpy as np
import json
import requests

#load from API
def loadDataFromIMSAPI():
    api_token = open("SECRETS/API_TOKEN.txt", "r").read()
    headers = {
        'Authorization': 'ApiToken {}'.format(api_token)
    }
    #get last date
    final_df= pd.read_csv('data/final_df.csv')
    final_date = final_df['sample_date'].sort_values().iloc[-1]
    #add a day to final_date
    new_date = (pd.to_datetime(final_date)  + pd.DateOffset(days=1))

    #extract year/month/day
    final_year = "{:04d}".format(new_date.year)
    final_month = "{:02d}".format(new_date.month)
    final_day = "{:02d}".format(new_date.day)

    #load data from api
    url = 'https://api.ims.gov.il/v1/envista/stations/186/data/1/?FROM=2019/10/15&to={}/{}/{}'.format(final_year, final_month, final_day)
    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text.encode('utf8'))
    df = pd.DataFrame(data['data'])
    df['rain_mm'] = [x[0]['value'] for x in df['channels']]
    datetime_col = pd.to_datetime(df['datetime'], utc=True)
    df['date'] = datetime_col.dt.date
    df['month'] = datetime_col.dt.month
    df['year'] = datetime_col.dt.year
    df['day'] = datetime_col.dt.day
    print("rain sum: {}".format(np.round(df['rain_mm'].sum(), 1)))

    return df[['datetime','date','month','year','day','rain_mm']]

#Clean downloaded IMS FILE
def cleanIMSTable(ims_df):

    df_clean = ims_df.rename(columns={'תאריך':'date','שעה':'hour','כמות גשם(מ"מ)':'rain_mm'})[['date','rain_mm']]

    #datetime
    df_clean['date'] = pd.to_datetime(df_clean['date'], format='%d-%m-%Y')
    df_clean['month'] = df_clean['date'].dt.month
    df_clean['year'] = df_clean['date'].dt.year
    df_clean['day'] = df_clean['date'].dt.day

    ##rain

    df_clean['rain_mm'] = df_clean['rain_mm'].astype('float32')
    print( "rain sum: {}".format( np.round(df_clean['rain_mm'].sum(),1) ) )
    return df_clean

#group by month and date
def monthlyAndDailyRain(df):
    df_monthly = df.groupby(['year', 'month'])['rain_mm'].sum()
    df_daily = df.groupby('date')['rain_mm'].sum()
    df_daily = pd.DataFrame(df_daily)
    df_daily['rain_mm_cumsum'] = df_daily.cumsum()
    return df_daily, df_monthly

# INITALIZE DATa

def initalizeRainData():

    ### LOAD FILE FROM MANUAL DOWNLAD - migrated to new API download function
    # ny = pd.read_csv('data/NeveYaar10m.csv', encoding='windows-1255')
    #
    # ims_df = ny

    # ims_df=cleanIMSTable(ims_df)

    ims_df = loadDataFromIMSAPI()

    df_daily_rain, df_monthly_rain = monthlyAndDailyRain(ims_df)

    df_daily_rain.to_csv('data/df_daily_rain.csv')
    df_monthly_rain.to_csv('data/df_monthly_rain.csv')
# initalizeRainData()

df_daily_rain = pd.read_csv('data/df_daily_rain.csv', parse_dates=['date'], index_col=0)

# df_monthly_rain = pd.read_csv('data/df_monthly_rain.csv', index_col=[0,1])








