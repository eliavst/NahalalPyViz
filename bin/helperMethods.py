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

poll_std = {'TN':10,
            'TP':1,
            'Cl':400,
            'Na':200,
            'Hg':0.0005,
            'Cr':0.05,
            'Ni':0.05,
            'Pb':0.008,
            'Cd':0.005,
            'Zn':0.2,
            'As':0.1,
            'Cu':0.02}

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



def rewriteReqFile():
    filename = 'requirments.txt'
    with open(filename, 'r') as fnr:
        text = fnr.readlines()
        print(text)

    filename2 = 'requirments2.txt'

    text = "".join([' - ' + line for line in text])
    with open(filename2, 'w') as fnw:
        fnw.write(text)

def cleanYTicks(ax):
    '''
    converts 0 to LOQ, removes negative ticks and set correct precision point
    '''
    if 0 in ax.get_yticks():
        val=0
        for x in ax.get_yticks():
            if (x>0) and (len(str(x)) < 8):
                val = x
                break


        list_yticks = list(ax.get_yticks())
        #final

        # val = float(list_yticks[list_yticks.index(0)+1])
        # find number of decimals
        if val >= 1:
            prec = 0
        else:
            prec = str(val)[::-1].find('.')
        # create list of yticks without negative
        yticks_list = ["{:.{}f}".format(x, prec) for x in list_yticks if x >= 0]
        if prec == 0:
            yticks_list = [int(y) for y in yticks_list]
        else:
            yticks_list = [float(y) for y in yticks_list]

        ax.set_yticks(yticks_list)
        # conver 0 to LOQ
        ind0 = yticks_list.index(0)
        yticks_list[ind0] = 'LOQ'
        ax.set_yticklabels(yticks_list)
