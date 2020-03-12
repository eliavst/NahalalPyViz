import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import DateFormatter
from matplotlib import rcParams
import colorcet as cc
from matplotlib.colors import ListedColormap, Normalize, TwoSlopeNorm
from matplotlib.cm import ScalarMappable
from bin.helperMethods import yLabel
final_df = pd.read_csv('data/final_df.csv')



##return colormap based on pollutant
def colormapAndNorm(p, df, final_df=final_df):
    if p != 'pH':
        cmap = ListedColormap(cc.fire[:-4][::-1])
        norm = Normalize(vmin=df[p].min(), vmax=df[p].max())
    else:
        cmap = ListedColormap(cc.gwv)
        norm = TwoSlopeNorm(vmin=final_df[p].min(), vcenter=7, vmax=final_df[p].max())

    return cmap, norm




#colormap

# from pandas.plotting import register_matplotlib_converters
# register_matplotlib_converters()


        #return '{} {}(mg/l)'.format(p, 'concentration ' if conc else '')

def yLim(p, relative, filtered_df, final_df=final_df):
    #relative boolean dictates if to use all values or current values
    if relative:
        df = filtered_df
    else:
        df=final_df
    ymax = df[p].max() * 1.05
    if p == 'pH':
        ymin = df[p].min() * .95
    else:
        ymin = 0
    return ymin, ymax

#point = 11; p = 'P-PO4'; df = final_df; rain_df=df_daily_rain
def graphPollutantRain(point, p, df, rain_df, relative):
    rcParams['axes.spines.right'] = True

    p_df_sel = df.loc[df.id==point,['sample_date',p]].dropna().reset_index(drop=True)
    p_df_sel.sample_date = pd.to_datetime(p_df_sel.sample_date)
    fig, ax = plt.subplots(figsize=(10,5))

    axt = ax.twinx()
    ax.set_zorder(axt.get_zorder()+1)
    ax.patch.set_visible(False)  # hide the 'canvas'
    axt.set_yticks([0,25,50,75])


    ax.plot('sample_date',p, marker='o', data = p_df_sel, markersize =10, color='purple', linestyle='none', alpha=0.8)
    ylabel = yLabel(p)
    ax.set_ylabel(ylabel, color='purple')
    axt.bar('date', 'rain_mm', color='lightblue', data=rain_df.reset_index(), label='Daily rain (nahalal)')
    axt.set_ylabel('Rain (mm) - Neve Yaar IMS', color='lightblue')

    ###ylim
    ymin, ymax = yLim(p, relative, p_df_sel)
    ax.set_ylim(ymin, ymax)

    ax.set_xlim('2019-10-15', ax.get_xlim()[1])
    ax.set_xlabel('Date')

    ax.set_title('{} for point {} and daily rain'.format(ylabel,point), weight='bold')
    ax.set_xticks(p_df_sel['sample_date'])
    ax.set_xticklabels(ax.get_xticklabels(), rotation=20)
    ax.xaxis.set_major_formatter(DateFormatter("%d-%m-%y"))

    # axt.set_yticklabels(axt.get_yticklabels(), color='lightblue', weight='bold')
    # ax.set_xticks(['2020-01-01'], minor=True)
    # ax.set_xticklabels(["2020"], rotation=90, minor=True, weight='bold')

    plt.close("all")

    return fig

# date = '2020-02-03'
def graphPollutantByDate(date, p, df, relative):
    #rcParams['axes.spines.right'] = False
    pd.to_datetime(df.sample_date).unique()
    p_df_sel = df.loc[df.sample_date == date, ['id', p]].dropna().reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(10, 5))

    #return colormap and norm
    cmap, norm = colormapAndNorm(p, p_df_sel)

    ax.scatter('id', p, data=p_df_sel, c=p_df_sel[p], s=100, cmap=cmap, norm=norm, edgecolors='purple')
    # cbaxes = fig.add_axes([0.05, 0.1, 0.03, 0.8])

    #norm = Normalize(vmin=p_df_sel[p].min(), vmax=p_df_sel[p].max())

    fig.colorbar(ScalarMappable(norm=norm, cmap=cmap),
                 ax=ax, fraction=.1, orientation='vertical')
    #ax.plot('id', p, marker='o', data=p_df_sel, markersize=10, color='purple', linestyle='none', alpha=0.8)

    ylabel = yLabel(p)
    ax.set_ylabel(ylabel, color='purple')

    ###ylim
    ymin, ymax = yLim(p, relative, p_df_sel)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel('Points')

    clean_date = pd.to_datetime(date).strftime('%d/%m/%Y')
    ax.set_title('{} on {}'.format(ylabel, clean_date), weight='bold')
    ax.set_xticks(p_df_sel['id'])

    plt.tight_layout()
    plt.close("all")

    return fig