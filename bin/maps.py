import geopandas as gpd
import geoviews as gv
import geoviews.tile_sources as gts
import colorcet as cc

cmap = cc.fire[:-4][::-1]

import os
os.chdir('C:/Users/eliav.ARO/Documents/IsraelWFP/Code/Python/Nahalal/PyViz')
smp_pnt = gpd.read_file("data/sampling_points4326.gpkg")
nahalal = gpd.read_file("data/nahalal4326.gpkg")
nahalal_sub = gpd.read_file("data/nahalal_sub4326.gpkg")


def mapPoint(id=11):

    current_pnt = gv.Points(smp_pnt.query("id=={}".format(id)))
    pnts = gv.Points(smp_pnt, vdims=["id", "description"])

    points_map = (
        (
            gts.EsriImagery.opts(alpha=0.4)
            * gts.OSM.opts(alpha=0.4)
            * gv.Path(nahalal).opts(line_width=2.5, alpha=0.4, line_color="blue")
            * gv.Path(nahalal_sub).opts(
                line_width=2, line_dash="dashdot", alpha=0.4, line_color="blue")
            * pnts.opts(size=13, alpha=0.6, tools=["hover"])
            * current_pnt.opts(size=20,  color="purple")
        )
        .opts(width=450, height=400)
        .redim.range(Longitude=(35.13, 35.24), Latitude=(32.65, 32.74))
    )

    return points_map

def mapDate(df):
    smp_pnt_df = smp_pnt.merge(df, on='id').dropna().reset_index(drop=True)
    #valid results
    if len(smp_pnt_df) > 0:
        pol = smp_pnt_df.columns[-1]
        pnts = gv.Points(smp_pnt_df, vdims=["id", "description", pol])

        points_map = (
            (gts.EsriImagery.opts(alpha=0.4)
                * gts.OSM.opts(alpha=0.4)
                * gv.Path(nahalal).opts(line_width=2.5, alpha=0.4, line_color="blue")
                * gv.Path(nahalal_sub).opts(
                    line_width=2, line_dash="dashdot", alpha=0.4, line_color="blue")
                * pnts.opts(size=15, alpha=0.8, tools=["hover"], color_index=pol, cmap = cmap)
            )
            .opts(width=450, height=400)
            .redim.range(Longitude=(35.13, 35.24), Latitude=(32.65, 32.74))
        )
    else:
        points_map = (
            (gts.EsriImagery.opts(alpha=0.4)
                    * gts.OSM.opts(alpha=0.4)
                    * gv.Path(nahalal).opts(line_width=2.5, alpha=0.4, line_color="blue")
                    * gv.Path(nahalal_sub).opts(
                line_width=2, line_dash="dashdot", alpha=0.4, line_color="blue")
            )
                .opts(width=450, height=400)
                .redim.range(Longitude=(35.13, 35.24), Latitude=(32.65, 32.74))
        )


    return points_map

