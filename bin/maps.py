import numpy as np
import geopandas as gpd
import geoviews as gv
import geoviews.tile_sources as gts
import colorcet as cc
from bokeh.models import HoverTool
from bin.helperMethods import yLabel


def cmapAndPName(p):
    if p!='pH':
        cmap = cc.fire[:-4][::-1]
        symmetric=False
        pname=p
    else:
        cmap = cc.gwv
        symmetric=True
        pname = 'pH0'
    return cmap, symmetric, pname

smp_pnt = gpd.read_file("data/sampling_points4326.gpkg")
nahalal = gpd.read_file("data/nahalal4326.gpkg")
nahalal_sub = gpd.read_file("data/nahalal_sub4326.gpkg")
nahalal_basin = gpd.read_file("data/nahalal_basin.gpkg")
kishon = gpd.read_file("data/kishon.gpkg")

def boundingBox(basin ,minxbuffer=.01, maxxbuffer=0, minybuffer=.01, maxybuffer=0):
    '''

    :param basin:
    :param minxbuffer:
    :param maxxbuffer:
    :param minybuffer:
    :param maxybuffer:
    :return: bounding box of basin with buffer
    '''
    minx = np.round(basin.bounds['minx'].iloc[0] - minxbuffer, 2)
    maxx = np.round(basin.bounds['maxx'].iloc[0] + maxxbuffer, 2)
    miny = np.round(basin.bounds['miny'].iloc[0] - minybuffer, 2)
    maxy = np.round(basin.bounds['maxy'].iloc[0] + maxybuffer, 2)
    # print('x: {},{}, y: {}, {}'.format(minx, maxx, miny, maxy))
    return minx, maxx, miny, maxy

def mapPoint(id=11):

    #bbox
    minx, maxx, miny, maxy = boundingBox(nahalal_basin)

    current_pnt = gv.Points(smp_pnt.query("id=={}".format(id)))
    pnts = gv.Points(smp_pnt, vdims=["id", "description"])
    basin = gv.Contours(nahalal_basin)

    # hovertool
    hover = HoverTool(tooltips=[
        ("Point #", "@id"),
        ("Description", '@description')]
    )

    points_map = (
        (
                gts.EsriImagery.opts(alpha=0.4)
                * gts.OSM.opts(alpha=0.4)
                * basin.opts(color='chocolate', line_width=1.5, alpha=.5)
                * gv.Path(kishon).opts(line_width=3.5, alpha=0.4, line_color="darkblue", line_dash="dashed")
                * gv.Path(nahalal).opts(line_width=2.5, alpha=0.4, line_color="blue")
                * gv.Path(nahalal_sub).opts(
            line_width=2, line_dash="dashdot", alpha=0.4, line_color="blue")
                * pnts.opts(size=13, alpha=0.6, tools=[hover])
                * current_pnt.opts(size=20, color="purple")
            # * gv.Contours(interest_zone).opts(alpha=0)
        )
            .opts(width=500, height=375)
            .redim.range(Longitude=(minx, maxx), Latitude=(miny, maxy))
    )

    return points_map

def mapDate(df):
    smp_pnt_df = smp_pnt.merge(df, on='id').dropna().reset_index(drop=True)

    basin = gv.Contours(nahalal_basin)

    # bbox
    minx, maxx, miny, maxy = boundingBox(nahalal_basin)
    #valid results
    if len(smp_pnt_df) > 0:
        #clean column names
        smp_pnt_df.columns = smp_pnt_df.columns.map(lambda x: x.replace('-','_'))

        pol = smp_pnt_df.columns[-1]
        # cmap/symmetric
        if pol=='pH':
            smp_pnt_df['pH0'] = smp_pnt_df['pH'] - 7
        cmap, symmetric, pname = cmapAndPName(pol)
        #vdims
        vdims = ["id", "description", pol]
        if pol == 'pH':
            vdims = vdims + ['pH0']
        #pnts
        pnts = gv.Points(smp_pnt_df, vdims=vdims)
        if pol == 'pH':
            pnts = gv.Points(smp_pnt_df, vdims=vdims)

        hover = HoverTool(tooltips=[
            ("Point #", "@id"),
            ("Description", '@description'),
            #("{}".format(yLabel(pol)), '(@{})'.format(pol))]
            ("{}".format(yLabel(pol)).replace('_','-'),'@{}'.format(pol))]
        )

        ##map
        points_map = (
            (gts.EsriImagery.opts(alpha=0.4)
             * gts.OSM.opts(alpha=0.4)
             * basin.opts(color='chocolate', line_width=1.5, alpha=.5)
             * gv.Path(kishon).opts(line_width=3.5, alpha=0.4, line_color="darkblue", line_dash="dashed")
             * gv.Path(nahalal).opts(line_width=2.5, alpha=0.4, line_color="blue")
             * gv.Path(nahalal_sub).opts(
                        line_width=2, line_dash="dashdot", alpha=0.4, line_color="blue")
             * pnts.opts(size=15, alpha=0.8, tools=[hover], color_index=pname, cmap = cmap, line_color='purple', symmetric=symmetric)
             )
                .opts(width=500, height=375)
                .redim.range(Longitude=(minx, maxx), Latitude=(miny, maxy))
        )
    else:
        points_map = (
        (gts.EsriImagery.opts(alpha=0.4)
         * gts.OSM.opts(alpha=0.4)
         * basin.opts(color='chocolate', line_width=1.5, alpha=.5)
         * gv.Path(kishon).opts(line_width=3.5, alpha=0.4, line_color="darkblue", line_dash="dashed")
         * gv.Path(nahalal).opts(line_width=2.5, alpha=0.4, line_color="blue")
         * gv.Path(nahalal_sub).opts(line_width=2, line_dash="dashdot", alpha=0.4, line_color="blue")
         ).opts(width=500, height=375).redim.range(Longitude=(minx, maxx), Latitude=(miny, maxy))
    )

    return points_map

