import param
import panel as pn
import pandas as pd
import numpy as np

from bin.graphs import graphPollutantRain, graphPollutantByDate, graphPollutantsByPointMulti, graphPollutantsByDateMulti
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
    pol_categories = ['pH, EC, Cl, Na, Ca, Mg, TOC, IC',
                      'P-PO4, N-NO3, N-NO2, N-NH4, TN, TON, K, S-SO4',
                      'B, Al, Fe, Cd, Co, Cu, Zn',
                      'Mn, Mo, Ni, Cr, As, Pb, Hg']
    #params
    view_type = param.Selector(default="By Point", objects=['By Date','By Point','By Date - Multi', 'By Point - Multi'])

    dates = param.Selector(default=dates_list[-1], objects=list(dates_list))
    points = param.Selector(default=11, objects=list(np.arange(1,14)))
    multi_dates = param.ListSelector(default=list(dates_list)[-3:-1], objects=list(dates_list))
    multi_points = param.ListSelector(default=[10,11], objects=list(np.arange(1, 14)))
    pollutant = param.Selector(default='EC', objects=pol_list)
    pollutant_group = param.Selector(default='pH, EC, Cl, Na, Ca, Mg, TOC, IC', objects=pol_categories)
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

    def pnPollConcByPointMulti(self, view_fn=graphPollutantsByPointMulti):
        # print("pnPollConcByPoint")
        return view_fn(
            df=final_df,
            points=self.multi_points,
            ps=self.pollutant_group,
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

    def pnPollConcByDateMulti(self, view_fn=graphPollutantsByDateMulti):
        # print("pnPollConcByPoint")
        return view_fn(
            df=final_df,
            dates=self.multi_dates,
            ps=self.pollutant_group,
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
        "view_type", "points", "multi_points", "dates", "multi_dates", "pollutant", "pollutant_group", "relative_scale"
    )
    def returnGraph(self):
        # print("returnGraph")
        if self.view_type=='By Point':
            return self.pnPollConcByPoint()
        elif self.view_type=='By Date':
            return self.pnPollConcByDate()
        if self.view_type=='By Point - Multi':
            return pn.Row(pn.layout.HSpacer(), self.pnPollConcByPointMulti(), pn.layout.HSpacer())
        elif self.view_type=='By Date - Multi':
            return pn.Row(pn.layout.HSpacer(), self.pnPollConcByDateMulti(), pn.layout.HSpacer())

    @pn.depends(
        "view_type", "points", "dates", "pollutant"
    )
    def returnMap(self):
        # print("returnMap")
        if self.view_type=='By Point':
            # print("byPoint")
            return self.pnPointMap()
        elif self.view_type=='By Date':
            # print("byDate")
            return self.pnDateMap()


    @param.depends("view_type", "dates", "points", "multi_dates", "multi_points", "pollutant", "pollutant_group",)
    def view_header(self):

        #determines wether to display current point or date
        def returnDatePoint(self):
            if 'Multi' in self.view_type:
                if 'Date' in self.view_type:
                    return ','.join([x.strftime('%d/%m') for x in pd.to_datetime(self.multi_dates, format='%d/%m/%Y')])
                else:
                    return ','.join(map(lambda x: str(x), self.multi_points))
            else:
                if self.view_type == 'By Date':
                    return self.dates
                else:
                    return self.points

        if 'Multi' in self.view_type:
            p_header = ','.join(self.pollutant_group.split(', ')[:2])+'...'
        else:
            p_header = yLabel(self.pollutant)

        header = "## Nahalal Stream Water Quality Viewer - {} ({}) - {}".format(self.view_type,returnDatePoint(self), p_header)

        return pn.pane.Markdown(header, width=1350, style={"text-align":"center"})

    @param.depends("view_type")
    def widgets(self):
        #         y_wid = pn.Param(
        #             self.param.y_value, width=200, widgets={"y_value": pn.widgets.Select}
        #         )
        #type_wid = pn.Param(self.param.view_type, widgets={"view_type": pn.widgets.RadioButtonGroup})
        type_wid = self.param.view_type


        ## MULTI POLLUTANT VIEW
        if 'Multi' in self.view_type:
            # print("Multi")
            pol_wid = self.param.pollutant_group
            if 'Point' in self.view_type:
                # select_wid = pn.panel(self.param, widgets={'multi_points': pn.widgets.CheckBoxGroup})
                select_wid = self.param.multi_points
            else:
                select_wid = self.param.multi_dates
        ## SINGLE POLLUTANT VIEW
        else:
            # print("Single")
            pol_wid = self.param.pollutant
            if self.view_type == 'By Point':
                select_wid = self.param.points
            else:
                select_wid = self.param.dates

        rel_wid = self.param.relative_scale

        pol_cat_wid = self.param.pollutant_group
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



