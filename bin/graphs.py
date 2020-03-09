import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import DateFormatter
from matplotlib import rcParams
import colorcet as cc
from matplotlib.colors import ListedColormap, Normalize
from matplotlib.cm import ScalarMappable

cmap = ListedColormap(cc.fire[:-4][::-1])

# from pandas.plotting import register_matplotlib_converters
# register_matplotlib_converters()

def yLabel(p):
    if p == 'pH':
        return p
    elif p == 'EC':
        return 'EC (μS/cm)'
    else:
        return '{} concentration (mg/l)'.format(p)

#point = 11; p = 'P-PO4'; df = final_df; rain_df=df_daily_rain
def graphPollutantRain(point, p, df, rain_df):
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

    if p != 'pH':
        ax.set_ylim(0, ax.get_ylim()[1])
    # # limits
    # if p == 'N-NO3':
    #
    #     ax.set_ylim(0, 100)
    # elif p == 'Cl':
    #     ax.set_ylim(0, 1200)

    ax.set_xlim('2019-10-15', ax.get_xlim()[1])
    ax.set_xlabel('Date')

    ax.set_title('{} for point {} and daily rain'.format(ylabel,point), weight='bold')
    ax.set_xticks(p_df_sel['sample_date'])
    ax.set_xticklabels(ax.get_xticklabels(), rotation=15)
    ax.xaxis.set_major_formatter(DateFormatter("%d-%m-%y"))

    # axt.set_yticklabels(axt.get_yticklabels(), color='lightblue', weight='bold')
    # ax.set_xticks(['2020-01-01'], minor=True)
    # ax.set_xticklabels(["2020"], rotation=90, minor=True, weight='bold')

    plt.close("all")

    return fig

# date = '2020-02-03'
def graphPollutantByDate(date, p, df):
    #rcParams['axes.spines.right'] = False
    pd.to_datetime(df.sample_date).unique()
    p_df_sel = df.loc[df.sample_date == date, ['id', p]].dropna().reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.scatter('id', p, data=p_df_sel, c=p_df_sel[p], s=100, cmap=cmap)
    # cbaxes = fig.add_axes([0.05, 0.1, 0.03, 0.8])
    norm = Normalize(vmin=p_df_sel[p].min(), vmax=p_df_sel[p].max())

    fig.colorbar(ScalarMappable(norm=norm, cmap=cmap),
                 ax=ax, fraction=.1, orientation='vertical')
    #ax.plot('id', p, marker='o', data=p_df_sel, markersize=10, color='purple', linestyle='none', alpha=0.8)
    ylabel = yLabel(p)

    ax.set_ylabel(ylabel, color='black')


    if p != 'pH':
        ax.set_ylim(0, ax.get_ylim()[1])
    # # limits
    # if p == 'N-NO3':
    #
    #     ax.set_ylim(0, 100)
    # elif p == 'Cl':
    #     ax.set_ylim(0, 1200)

    ax.set_xlabel('Points')

    clean_date = pd.to_datetime(date).strftime('%d/%m/%Y')
    ax.set_title('{} on {}'.format(ylabel, clean_date), weight='bold')
    ax.set_xticks(p_df_sel['id'])

    plt.tight_layout()
    plt.close("all")

    return fig