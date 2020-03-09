import param
import panel as pn
import pandas as pd
import numpy as np

from bin.graphs import graphPollutantRain, graphPollutantByDate
from bin.maps import mapPoint, mapDate, smp_pnt, nahalal, nahalal_sub
from bin.meteoData import df_daily_rain


import os
os.getcwd()


folder =  'C:/Users/eliav.ARO/Documents/IsraelWFP/Code/Python/Nahalal/PyViz/'


class NahalalVisuzalizer(param.Parameterized):
    #all results
    #dates
    final_df = pd.read_csv(folder + 'data/final_df.csv')

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
            df=self.final_df,
            rain_df=df_daily_rain
        )


    def pnPollConcByDate(self, view_fn=graphPollutantByDate):

        clean_date = pd.to_datetime(self.dates, format='%d/%m/%Y').strftime('%Y-%m-%d')
        return view_fn(
            date=clean_date,
            p=self.pollutant,
            df=self.final_df,
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

        df = self.final_df.loc[self.final_df.sample_date==clean_date, ['id',self.pollutant]].reset_index(drop=True)
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
        # if self.view_type=='By Date':
        #     clean_date = pd.to_datetime(self.dates, format='%d/%m/%Y').strftime('%Y-%m-%d')
        #     clean_date = pd.to_datetime('28/10/19', format='%d/%m/%Y').strftime('%Y-%m-%d')
        #
        #     final_df
        #     return self.pnPointMap()


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
    # @param.depends("crop_category", "crop_type", "y_value", "region")
    # def view_header(self):
    #
    #     def agg_value(gt = self.growth_type, ct = self.crop_type, gct = self.general_crop_type, cc_cat=self.crop_category,
    #                   y = self.y_value):
    #         #filter data by crop type level
    #         if gt != 'Choose...':
    #             df = data.loc[data.growth_name_heb == gt]
    #         elif ct != 'Choose...':
    #             df = data.loc[data.crop_name == ct]
    #         elif gct != 'Choose...':
    #             df = data.loc[data.general_crop_name == gct]
    #         elif cc_cat == "All Crops":
    #             df = data
    #         elif cc_cat == "Plantations/Citrus":
    #             df = data.loc[data.crop_category_name.isin(["Plantations","Citrus"])]
    #         elif cc_cat == "Vegetables/Herbs":
    #             df = data.loc[data.crop_category_name.isin(["Vegetables","Herbs"])]
    #         elif cc_cat == "Field Crops/Flowers":
    #             df = data.loc[data.crop_category_name.isin(["Field Crops","Flowers"])]
    #
    #
    #
    #         ### get agg by yvalue
    #         y_agg = None
    #         if y=="m3 per dunam":
    #             y_agg = np.round(df['m3_per_dunam'].mean(),1)
    #         elif y == "m3 per yield":
    #             y_agg = np.round(df['m3_per_yield'].mean(),1)
    #         elif y == "Area (square km)":
    #             y_agg = np.round(df['dunam'].sum()/1000,1)
    #         elif y == "Water Use (MCM/year)":
    #             y_agg = np.round(df['total_m3'].sum()/10**6,1)
    #
    #         return y_agg
    #
    #
    #     # wus = waterUseSource(data, self.crop_type)
    #
    #     def returnCropNameCategory(cc=self.crop_category, gct=self.general_crop_type, ct=self.crop_type, gt=self.growth_type):
    #         if gt!='Choose...':
    #             return '{} ({})'.format(ct, gt)
    #         elif ct != 'Choose...':
    #             return ct
    #         elif gct != 'Choose...':
    #             return gct
    #         else:
    #             return cc
    #
    #     header1 = "## {};".format(returnCropNameCategory())
    #     header2 = "## {} - {};".format(self.y_value, agg_value())
    #     header3 = "## {};".format(self.region)
    #
    #     # header4 = (
    #     #     "## {};".format(self.general_crop_type)
    #     #     if self.general_crop_type != "Choose..."
    #     #     else ""
    #     # )
    #     # header5 = (
    #     #     "## {};".format(self.crop_type)
    #     #     if self.crop_type != "Choose..."
    #     #     and self.crop_type != self.general_crop_type
    #     #     else ""
    #     # )
    #     # header6 = (
    #     #     "## {};".format(self.growth_type) if self.growth_type != "Choose..." else ""
    #     # )
    #     header6 = (
    #         "##Yield: {} ton/dunam;".format(self.crop_yield) if self.crop_yield != 0 else ""
    #     )
    #
    #     return pn.Row(
    #         pn.pane.Markdown(header1),
    #         pn.pane.Markdown(header2),
    #         pn.pane.Markdown(header3),
    #         # pn.pane.Markdown(header4),
    #         # pn.pane.Markdown(header5),
    #         # pn.pane.Markdown(header5),
    #         pn.pane.Markdown(header6)
    #     )

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

