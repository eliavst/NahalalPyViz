import param
import panel as pn
import pandas as pd
import numpy as np

from bin.graphs import graphPollutantRain, graphPollutantByDate, yLabel
from bin.maps import mapPoint, mapDate, smp_pnt, nahalal, nahalal_sub
from bin.meteoData import df_daily_rain


import os
os.getcwd()


folder =  'C:/Users/eliav.ARO/Documents/IsraelWFP/Code/Python/Nahalal/PyViz/'


final_df = pd.read_csv(folder + 'data/final_df.csv')

class NahalalVisuzalizer(param.Parameterized):
    #all results
    #dates

    dates_list = pd.to_datetime(final_df.sample_date.unique()).sort_values().strftime('%d/%m/%Y')
    pol_list = ['EC', 'pH', 'N-NO3','P-PO4','Cl','S-SO4','N-NO2','N-NH4','TOC']
    #params
    view_type = param.Selector(default="By Point", objects=['By Date','By Point'])

    dates = param.Selector(default=dates_list[-1], objects=dates_list)
    points = param.Selector(default=11, objects=np.arange(1,14))
    pollutant = param.Selector(default='EC', objects=pol_list)

    def pnPollConcByPoint(self, view_fn=graphPollutantRain):
        return view_fn(
            point=self.points,
            p=self.pollutant,
            df=final_df,
            rain_df=df_daily_rain
        )


    def pnPollConcByDate(self, view_fn=graphPollutantByDate):

        clean_date = pd.to_datetime(self.dates, format='%d/%m/%Y').strftime('%Y-%m-%d')
        return view_fn(
            date=clean_date,
            p=self.pollutant,
            df=final_df,
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
        "view_type", "points", "dates", "pollutant"
    )
    def returnGraph(self):
        if self.view_type=='By Point':
            return self.pnPollConcByPoint()
        elif self.view_type=='By Date':
            return self.pnPollConcByDate()

    @pn.depends(
        "view_type", "points", "dates", "pollutant"
    )
    def returnMap(self):
        if self.view_type=='By Point':
            return self.pnPointMap()
        elif self.view_type=='By Date':
            return self.pnDateMap()






    # @pn.depends(
    #     "general_crop_type", "crop_type", "growth_type", "crop_category", "y_value", "region"
    # )
    # def pnCropRegionMap(self, view_fn=cropByRegionMap):
    #     return view_fn(
    #         data,
    #         kc_zone_gdf,
    #         general_crop_type=self.general_crop_type,
    #         crop_type=self.crop_type,
    #         growth_type=self.growth_type,
    #         cc_cat=self.crop_category,
    #         y_value=self.y_value,
    #         region = self.region
    #     )
    #
    # @param.depends(
    #     "general_crop_type",
    #     "crop_type",
    #     "growth_type",
    #     "crop_category",
    #     "y_value",
    #     "region",
    #     watch=True,
    # )
    # def view_bar(self, **kwargs):
    #     #print("view_bar")
    #     bar = self.pnCropBar()
    #     map = self.pnCropRegionMap()
    #     return pn.Row(pn.layout.HSpacer(), pn.Column(bar, width=700), pn.Column(map,width=500, height=800))
    #
    @param.depends("view_type", "dates", "points", "pollutant")
    def view_header(self):


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
        type_wid = self.param.view_type
        if self.view_type == 'By Point':
            select_wid = self.param.points
        else:
            select_wid = self.param.dates

        pol_wid = self.param.pollutant

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
            width=150,
        )

    # @param.depends("crop_category", watch=True)
    # def update_crop_category(self):
    #     # print("update_crop_category")
    #     cc_cat = self.crop_category
    #
    #     full_crop_list, growth_list, crop_list, general_crop_list = growthAndCropLists(
    #         crops, self.crop_category
    #     )
    #
    #     self.param.general_crop_type.objects = general_crop_list
    #     self.general_crop_type = "Choose..."
    #
    #     self.param.crop_type.objects = crop_list
    #     self.crop_type = "Choose..."
    #
    #     self.param.growth_type.objects = growth_list
    #     self.growth_type = "Choose..."
    #
    #     self.crop_yield = 0
    #
    # @param.depends("general_crop_type", watch=True)
    # def update_general_crop_type(self):
    #     #         print("update_general_crop_type")
    #
    #     if self.general_crop_type != "Choose...":
    #         sel_crop_list = self.full_crop_list.loc[
    #             self.full_crop_list["general_crop_name"] == self.general_crop_type
    #         ]
    #
    #         new_crop_list = list(sorted(sel_crop_list["crop_name"].unique()))
    #         new_crop_list.insert(0, "Choose...")
    #         self.param.crop_type.objects = list(new_crop_list)
    #
    #         if len(new_crop_list) == 2:
    #             self.crop_type = new_crop_list[1]
    #         else:
    #             self.crop_type="Choose..."
    #
    #         new_growth_list = list(sorted(sel_crop_list["growth_name_heb"].unique()))
    #         new_growth_list.insert(0, "Choose...")
    #         self.param.growth_type.objects = list(new_growth_list)
    #
    #         ###set yield
    #         self.crop_yield = np.round(data.loc[data.general_crop_name == self.general_crop_type, 'yield_per_dunam'].mean(), 1)
    #
    #         if len(new_growth_list) == 2:
    #             self.growth_type = new_growth_list[1]
    #         else:
    #             self.growth_type="Choose..."
    #
    #     else:
    #         # print("call update_crop_category")
    #         self.update_crop_category()
    #
    # @param.depends("crop_type", watch=True)
    # def update_crop_type(self):
    #     #         print("update_crop_type")
    #
    #     if self.crop_type != "Choose...":
    #         sel_crop_list = self.full_crop_list.loc[
    #             self.full_crop_list["crop_name"] == self.crop_type
    #         ]
    #
    #         # new_general_crop_list = list(
    #         #     sorted(sel_crop_list["general_crop_name"].unique())
    #         # )
    #         # if len(new_general_crop_list) == 1:
    #         #     self.general_crop_type = new_general_crop_list[0]
    #         # # new_general_crop_list.insert(0, "Choose...")
    #         # # self.param.general_crop_type.objects = list(new_general_crop_list)
    #
    #         new_growth_list = list(sorted(sel_crop_list["growth_name_heb"].unique()))
    #         new_growth_list.insert(0, "Choose...")
    #         self.param.growth_type.objects = list(new_growth_list)
    #         ###set yield
    #         self.crop_yield = np.round(data.loc[data.crop_name == self.crop_type, 'yield_per_dunam'].mean(), 1)
    #
    #         if len(new_growth_list) == 2:
    #             self.growth_type = new_growth_list[1]
    #         else:
    #             self.growth_type="Choose..."
    #
    #     else:
    #         self.growth_type = "Choose..."
    #         # print("call update_crop_category")
    #
    #         # self.update_crop_category()
    #
    # @param.depends("growth_type", watch=True)
    # def update_growth_type(self):
    #     #         print("update_growth_type")
    #
    #     if self.growth_type != "Choose...":
    #         sel_crop_list = self.full_crop_list.loc[
    #             self.full_crop_list["growth_name_heb"] == self.growth_type
    #         ]
    #         new_general_crop_list = list(
    #             sorted(sel_crop_list["general_crop_name"].unique())
    #         )
    #         self.general_crop_type = new_general_crop_list[0]
    #         # new_general_crop_list.insert(0, "Choose...")
    #         # self.param.general_crop_type.objects = new_general_crop_list
    #         new_crop_list = list(sorted(sel_crop_list["crop_name"].unique()))
    #         self.crop_type = new_crop_list[0]
    #
    #         new_crop_list.insert(0, "Choose...")
    #         self.param.crop_type.objects = new_crop_list
    #
    #
    #         ###set yield
    #         self.crop_yield = np.round(data.loc[data.growth_name_heb==self.growth_type, 'yield_per_dunam'].mean(),1)
    #
    #
    #     else:
    #         pass
    #         #           print("call update_crop_category")
    #         # self.update_crop_category()

