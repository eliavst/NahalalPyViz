import pandas as pd, numpy as np
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns

# Date time conversion registration
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

ny = pd.read_csv('data/NeveYaar10m.csv', encoding='windows-1255')

ims_df = ny
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

def monthlyAndDailyRain(df):
    df_monthly = df.groupby(['year', 'month'])['rain_mm'].sum()
    df_daily = df.groupby('date')['rain_mm'].sum()
    df_daily = pd.DataFrame(df_daily)
    df_daily['rain_mm_cumsum'] = df_daily.cumsum()
    return df_daily, df_monthly

ims_df=cleanIMSTable(ims_df)
df_daily_rain, df_monthly_rain = monthlyAndDailyRain(ims_df)




