# import geoviews
# from bin.test import thisIsATest

# print("imported geoviews")
# print(thisIsATest("This is another test"))
import panel as pn
import holoviews as hv
import bin.NahalalVisualizer as nv

hv.extension("bokeh", "matplotlib")

nvc = nv.NahalalVisuzalizer()

pane = pn.panel(
    pn.Row(
        pn.layout.HSpacer(),
        pn.Column(
            pn.Row(
                pn.layout.HSpacer(),
                nvc.view_header,#'Nahalal Visualizer',
                pn.layout.HSpacer(),
                width=1400,
                background="#f2f2f2",
                
            ),
            pn.Column(
                pn.Row(
                    pn.Column(pn.layout.VSpacer(),nvc.widgets,pn.layout.VSpacer(),height=300),
                    pn.Column(
                        pn.Row(pn.Column(nvc.returnGraph),
                               pn.Column(pn.layout.VSpacer(),nvc.returnMap,pn.layout.VSpacer())),
                        pn.Row(
                            pn.pane.Markdown(
                                """Created by Eliav Shtull-Trauring in Dr. Nirit Bernstein's Lab | <br>
                                Institute of Soil, Water and Environmental Sciences | 
                                Agricultural Research Organization – Volcani Center""",
                                width=1050,
                                style={
                                    "font-family": "Courier, monospace",
                                    "font-size": "16px",
                                },
                            )
                        ),
                    ),
                    
                )
            ),
        ),
        pn.layout.HSpacer(),
    )
)
#pane.show()
pane.servable(title="Nahalal Water Quality Viz")