from datetime import datetime

import os
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_html_components as html
from .make_tree import make_tree, make_bars
#from dash.dependencies import Output

#videos = pd.read_csv("data/sy.csv")
#stuff.to_csv('data/' + title + '.csv')

def register_callbacks(dashapp):
    @dashapp.callback([Output('tree', 'figure'),
                   Output('likes', 'figure'),
                   Output('minutes', 'figure'),
                   Output('views', 'figure'),
                   Output('channels', 'figure'),
                   Output('comments', 'figure')],
                  [Input('show', 'value')])
    def update_figures(show):
        stuff = pd.read_csv('data/' + show)
        fig1 = make_tree(stuff)
        fig2, fig3, fig4, fig5, fig6 = make_bars(stuff)
        return fig1, fig2, fig3, fig4, fig5, fig6

    @dashapp.callback([Output('table', 'data'),
                   #Output('table', 'columns')],
                   ],
                  [Input('show', 'value')])
    def update_table(show):
        stuff = pd.read_csv('data/' + show)
        #columns = [{"name": i, "id": i} for i in stuff.columns[:11]],
        data = stuff.to_dict('records'),
        return data
