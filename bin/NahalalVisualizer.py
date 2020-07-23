import param
import panel as pn
import pandas as pd
import numpy as np

from bin.graphs import graphPollutantRain, graphPollutantByDate
from bin.maps import mapPoint, mapDate
from bin.meteoData import df_daily_rain
from bin.helperMethods import yLabel


final_df = pd.read_csv('data/final_df.csv')

class NahalalVisuzalizer(param.Parameterized):
    #all results
    #dates
    dates_list = pd.to_datetime(final_df.sample_date.unique()).sort_values().strftime('%d/%m/%Y')
    pol_list = ['EC', 'pH', 'N-NO3','P-PO4','Cl','S-SO4','N-NO2','N-NH4','TOC', 'Na', 'K', 'Ca', 'Mn', 'Mg', 'Fe',
                'Zn','Cd', 'Co', 'Cr', 'Cu', 'Mo', 'B', 'Al', 'Ni', 'Pb', 'As', 'Hg']
    #params
    view_type = param.Selector(default="By Point", objects=['By Date','By Point'])

    dates = param.Selector(default=dates_list[-1], objects=dates_list)
    points = param.Selector(default=11, objects=np.arange(1,14))
    pollutant = param.Selector(default='EC', objects=pol_list)

    relative_scale = param.Boolean(default=False)

    def pnPollConcByPoint(self, view_fn=graphPollutantRain):
        # print("pnPollConcByPoint")
        return view_fn(
            point=self.points,
            p=self.pollutant,
            df=final_df,
            rain_df=df_daily_rain,
            relative=self.relative_scale
        )


    def pnPollConcByDate(self, view_fn=graphPollutantByDate):

        clean_date = pd.to_datetime(self.dates, format='%d/%m/%Y').strftime('%Y-%m-%d')
        return view_fn(
            date=clean_date,
            p=self.pollutant,
            df=final_df,
            relative=self.relative_scale
        )


    def pnPointMap(self, view_fn=mapPoint):
        return view_fn(
            id=self.points,
        )


    def pnDateMap(self, view_fn=mapDate):
        clean_date = pd.to_datetime(self.dates, format='%d/%m/%Y').strftime('%Y-%m-%d')

        # adate = '08/01/2020'
        # clean_date = pd.to_datetime(adate, format='%d/%m/%Y').strftime('%Y-%m-%d')
        # pol = 'Cl'

        df = final_df.loc[final_df.sample_date==clean_date, ['id',self.pollutant]].reset_index(drop=True)
        # df = final_df.loc[final_df.sample_date==clean_date, ['id',pol]].reset_index(drop=True)

        return view_fn(
            df=df
        )

    @pn.depends(
        "view_type", "points", "dates", "pollutant", "relative_scale"
    )
    def returnGraph(self):
        # print("returnGraph")
        if self.view_type=='By Point':
            return self.pnPollConcByPoint()
        elif self.view_type=='By Date':
            return self.pnPollConcByDate()

    @pn.depends(
        "view_type", "points", "dates", "pollutant"
    )
    def returnMap(self):
        # print("returnMap")
        if self.view_type=='By Point':
            print("byPoint")
            return self.pnPointMap()
        elif self.view_type=='By Date':
            print("byDate")

            return self.pnDateMap()


    @param.depends("view_type", "dates", "points", "pollutant")
    def view_header(self):

        #determines wether to display current point or date
        def returnDatePoint(self):
            if self.view_type == 'By Date':
                return self.dates
            else:
                return self.points
        header = "## Nahalal Stream Water Quality Viewer - {} ({}) - {}".format(self.view_type,returnDatePoint(self), yLabel(self.pollutant))

        return pn.pane.Markdown(header, width=750)

    @param.depends("view_type")
    def widgets(self):
        #         y_wid = pn.Param(
        #             self.param.y_value, width=200, widgets={"y_value": pn.widgets.Select}
        #         )
        #type_wid = pn.Param(self.param.view_type, widgets={"view_type": pn.widgets.RadioButtonGroup})
        type_wid = self.param.view_type
        if self.view_type == 'By Point':
            select_wid = self.param.points
        else:
            select_wid = self.param.dates

        pol_wid = self.param.pollutant
        rel_wid = self.param.relative_scale
        # reset_b = pn.widgets.Button(name="Reset", button_type="warning", width=50)
        # def b_reset(event):
        #     self.crop_category = "All Crops"
        #     self.update_crop_category()
        #
        # reset_b.on_click(b_reset)

        return pn.WidgetBox(
            type_wid,
            select_wid,
            pol_wid,
            rel_wid,
            width=150,
        )



