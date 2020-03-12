import colorcet as cc

# import seaborn as sns
# sns.palplot(cc.CET_L18[15:])

cmaps_d = {'pH': cc.gwv,
            'N-NO3' : cc.kgy[::-1],
           'N-NH4' :  cc.kgy[::-1],
           'N-NO2': cc.kgy[::-1],
           'S-SO4': cc.CET_L18[15:],
           'Cl' : cc.kbc[::-1],
           'EC' : cc.kbc[::-1],
           'P-PO4' : cc.CET_L7[::-1]}

def returnCMAP(p):
    p = p.replace('_','-')
    try:
        cmap = cmaps_d[p]
    except:
        cmap = cc.fire[:-4][::-1]

    return cmap


def yLabel(p):
    if p == 'pH':
        return p
    elif p == 'EC':
        return 'EC (μS/cm)'
    else:
        return '{} (mg/l)'.format(p)
