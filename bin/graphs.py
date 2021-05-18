import pandas as pd, seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.dates import DateFormatter
from matplotlib import rcParams
from matplotlib.colors import ListedColormap, Normalize, TwoSlopeNorm
from matplotlib.cm import ScalarMappable
from bin.helperMethods import yLabel, returnCMAP, poll_std, cleanYTicks
final_df = pd.read_csv('data/final_df.csv')



##return colormap based on pollutant
def colormapAndNorm(p, df, final_df=final_df):
    cc_cmap = returnCMAP(p)
    cmap = ListedColormap(cc_cmap)
    if p != 'pH':
        norm = Normalize(vmin=df[p].min(), vmax=df[p].max())
    else:
        norm = TwoSlopeNorm(vmin=final_df[p].min(), vcenter=7, vmax=final_df[p].max())

    return cmap, norm


def yLim(p, relative, filtered_df, final_df=final_df):
    #relative boolean dictates if to use all values or current values
    if relative:
        df = filtered_df
    else:
        df=final_df
    ymax = df[p].max() * 1.05
    #ymin
    if p == 'pH' or df[p].min() > 50:
        ymin = df[p].min() * .95
    else:
        ymin = 0
    return ymin, ymax

#point = 11; p = 'P-PO4'; df = final_df; rain_df=df_daily_rain; relative=True
def graphPollutantRain(point, p, df, rain_df, relative):
    # print("graphPollutantRain")

    rcParams['axes.spines.right'] = True
    rcParams['font.size'] = 14


    p_df_sel = df.loc[df.id==point,['sample_date',p]].dropna().reset_index(drop=True)
    p_df_sel.sample_date = pd.to_datetime(p_df_sel.sample_date)
    fig, ax = plt.subplots(figsize=(10,5))

    plt.subplots_adjust(right=0.83, bottom=0.165)

    axt = ax.twinx()
    ax.set_zorder(axt.get_zorder()+1)
    ax.patch.set_visible(False)  # hide the 'canvas'
    axt.set_yticks([0,25,50,75])

    ####cmap
    cmap, norm = colormapAndNorm(p, p_df_sel)
    ax.scatter('sample_date', p, data=p_df_sel, c=p_df_sel[p], s=100, cmap=cmap, norm=norm, edgecolors='purple')
    cbaxes = fig.add_axes([0.91, 0.12, 0.02, 0.76], yticks=[], xticks=[])

    fig.colorbar(ScalarMappable(norm=norm, cmap=cmap),
                 cax=cbaxes, fraction=.1, orientation='vertical')


    # ax.plot('sample_date',p, marker='o', data = p_df_sel, markersize =10, color='purple', linestyle='none', alpha=0.8)
    ylabel = yLabel(p)
    ax.set_ylabel(ylabel, color='purple', weight='bold')
    axt.bar('date', 'rain_mm', color='lightblue', data=rain_df.reset_index(), label='Daily rain (nahalal)')
    axt.set_ylabel('Daily Rain (mm) [Neve Yaar-IMS]', color='grey', weight='bold', path_effects=[path_effects.Stroke(linewidth=.75, foreground='lightblue', alpha=.8)])

    ###ylim
    ymin, ymax = yLim(p, relative, p_df_sel)
    ax.set_ylim(ymin, ymax)

    ax.set_xlim('2019-10-15', ax.get_xlim()[1])
    ax.set_xlabel('Date', weight='bold')

    ax.set_title('{} for point {} and daily rain'.format(ylabel,point), weight='bold')
    ax.set_xticks(p_df_sel['sample_date'])
    ##error - fix later
    ax.set_xticklabels(ax.get_xticklabels(), rotation=60, fontdict=(dict(fontsize=10)))
    ax.xaxis.set_major_formatter(DateFormatter("%d-%m"))

    ax.set_xticks(['2020-01-01'], minor=True)
   # ax.set_xticklabels(ax.get_xticklabels(), rotation=90, minor=True, fontdict=(dict(fontsize=9)))
    ax.xaxis.set_minor_formatter(DateFormatter("%Y"))

    pd.to_datetime('2020-01-01').strftime('%m-%y')
    # axt.set_yticklabels(axt.get_yticklabels(), color='lightblue', weight='bold')
    # ax.set_xticks(['2020-01-01'], minor=True)
    # ax.set_xticklabels(["2020"], rotation=90, minor=True, weight='bold')
    # print("graph test")
    plt.close("all")

    return fig

# date = '2020-02-03'
def graphPollutantByDate(date, p, df, relative):
    rcParams['font.size'] = 14

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
    ax.set_ylabel(ylabel, color='purple', weight='bold')
    ###ylim
    ymin, ymax = yLim(p, relative, p_df_sel)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel('Point', weight='bold')

    clean_date = pd.to_datetime(date).strftime('%d/%m/%Y')
    ax.set_title('{} on {}'.format(ylabel, clean_date), weight='bold')
    ax.set_xticks(p_df_sel['id'])

    plt.tight_layout()
    plt.close("all")

    return fig


# df = final_df; points=[2, 3]; ps = 'pH, EC, Cl, Na, Ca, Mg, TOC, IC'; p='EC'; relative=True

## MULTI GRAPHS
def graphPollutantsByPointMulti(df, points, ps, relative):
    df.sample_date = pd.to_datetime(df.sample_date, format='%Y-%m-%d')

    ps_list = ps.split(', ')
    rcParams['xtick.labelsize'] = 8
    tick_dates = pd.Series(df['sample_date'].unique()).sort_values()
    pol_df = pd.DataFrame(data=ps_list, columns=['p'])
    cmap = sns.color_palette("Set1", len(points))
    g = sns.FacetGrid(pol_df, col='p', col_wrap=3, aspect=1.5, sharey=False, sharex=True)

    # p = ps_list[0]; ax =g.axes[0]
    for p, ax in zip(ps_list, g.axes):
        # print(p)
        ##add standard
        try:
            std = poll_std[p]
            ax.axhline(std, color='grey', linewidth=2, linestyle='--', label='{} ({} mg/l)'.format(p, std))
            han, lab = ax.get_legend_handles_labels()
            ax.legend(labels=[lab[-1]], handles=[han[-1]], loc='best', frameon=False)
        except:
            pass
        # print(ax)
        for i, id in enumerate(points):
            # print(id)
            df_id = df.loc[df.id == id, ['sample_date', 'id', p]].sort_values(
                by='sample_date').dropna().reset_index(drop=True)
            ax.plot('sample_date', p, '', data=df_id, color=cmap[i], label=id, marker='o',fillstyle='none', alpha=0.7)
        ### if not relative use all results for ylim
        if not relative:
            ymin = df[p].min()*0.9
            ymax = df[p].max() * 1.1
            ax.set_ylim((ymin, ymax))

        ax.set_title(p, weight='bold')
        # convert 0 to LOQ and format yticklables
        cleanYTicks(ax)

    # TICKS and labels
    ax.set_xlim(df.sample_date.min() - pd.DateOffset(5), df.sample_date.max() + pd.DateOffset(5))
    ax.set_xticks(tick_dates)
    ax.xaxis.set_major_formatter(DateFormatter("%d/%m"))
    for ax in g.axes[-3:]:
        ax.tick_params(axis='x', labelrotation=90)
    ##add legend and ticks
    #
    # handles, labels = ax.get_legend_handles_labels()
    # ax.legend(handles, labels, title='Sample ID', title_fontsize=16, ncol=2, loc='center left', bbox_to_anchor=(1.3, 0.6), fontsize=14, frameon=False)
    ax.legend(title='Sample ID', title_fontsize=16, ncol=3, loc='center left', bbox_to_anchor=(1.2, 0.7),
              fontsize=14, frameon=False)
    plt.tight_layout()
    g.fig.subplots_adjust(wspace=0.15)

    plt.close("all")
    rcParams['xtick.labelsize'] = 12

    return g.fig

df= final_df;  dates = ['12/11/2019', '25/11/2019']; ps='pH, EC, Cl, Na, Ca, Mg, TOC, IC'

def graphPollutantsByDateMulti(df, dates, ps, relative):

    df.sample_date = pd.to_datetime(df.sample_date, format='%Y-%m-%d')
    dates = pd.to_datetime(dates, format='%d/%m/%Y')
    #ticks
    tick_ids = pd.Series(df['id'].unique()).sort_values()
    tick_ids.name='id'
    #num of values in each group
    ps_list = ps.split(', ')
    pol_df = pd.DataFrame(data=ps_list, columns=['p'])

    g = sns.FacetGrid(pol_df, col='p', col_wrap=3, aspect=1.6, sharey=False, sharex=True)
    cmap = sns.color_palette("Set1", len(dates))
    for p, ax in zip (ps_list, g.axes):
        ##add standard
        try:
            std = poll_std[p]
            ax.axhline(std, color='grey', linewidth=2, linestyle='--', label='{} ({} mg/l)'.format(p, std))
            han, lab = ax.get_legend_handles_labels()
            ax.legend(labels=[lab[-1]], handles=[han[-1]], loc='best', frameon=False)
        except:
            pass
        for i, date in enumerate(dates):
            df_date = df.loc[df.sample_date==date,['sample_date','id',p]].sort_values(by='id').dropna().reset_index(drop=True)
            if len(df_date)>0:
                ## add missing ids
                df_date = df_date.merge(tick_ids, on='id', how='right')
                df_date['sample_date'] = df_date['sample_date'].ffill()
                df_date = df_date.sort_values(by='id')
                #plot
                sns.stripplot('id', p, data=df_date, jitter=0.1, size=7, ax=ax, color=cmap[i], marker='o', facecolors='none', label=date.strftime('%d/%m/%y'), alpha=0.7)
                ax.set_xlabel('')
        if not relative:
            ymin = df[p].min()*0.9
            ymax = df[p].max() * 1.1
            ax.set_ylim((ymin, ymax))
        ax.set_title(p, weight='bold')
        # print('a')
        cleanYTicks(ax)

    for ax in g.axes[-3:]:
        ax.set_xlabel('Point ID', weight='bold')
    # ax.set_xticklabels('')


    handles, labels = g.axes[0].get_legend_handles_labels()
    ax.legend(handles[::13], labels[::13], title='Sample Date', title_fontsize=16, ncol=2, loc='center left', bbox_to_anchor=(1.15, 0.8), fontsize=14, frameon=False)

    plt.tight_layout()
    g.fig.subplots_adjust(wspace=0.25)

    plt.close("all")

    return g.fig