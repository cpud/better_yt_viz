import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
#from .make_tree import make_df

default_url = "https://www.youtube.com/watch?v=Rx-hgqChgic"
#videos = make_df(default_url)
#videos.to_csv("data/videos.csv")

stuff = pd.read_csv('data/friends.csv')

layout = html.Div([

    #html.Div([]),
    html.Div([
    html.Center([
    html.H3("Select a TV show to see a potential YouTube rabbit hole!"),

    dcc.Dropdown(id = 'show',
                 options = [
                     {'label': 'Community', 'value': 'community_paintball.csv'},
                     {'label': 'The Office', 'value': 'prison_mike.csv'},
                     {'label': 'Parks And Recreation', 'value': 'coffee_pot.csv'},
                     {'label': 'Friends', 'value': 'friends.csv'},
                     {'label': '30 Rock', 'value': '30rock.csv'}
             ],
                 value = 'friends.csv',
             style = {'width': '60%',
                      'text-align': 'left',
                      'padding-left': '420px',
                      #'display': 'inline-block',
                     }),
        html.Ul([
            html.Li('The starting node will have a "Depth" of 1. The node will be a \
                dark purple, so please locate that node to follow the graph.'),
            html.Li('The nodes with multiple connections are "selected" videos, while \
                the other videos will be related videos that were not "selected".'),
            html.Li("Selected videos were chosen randomly from the videos recommended on \
                the page with the previous video."),
            html.Li("The algorithm used to collect the recommended videos only considers \
                the first 10 recommended videos on the YouTube video page.")
            ], style = {'text-align': 'left',
                        'padding-left': '520px',
                        'padding-up': '50px'}),
        ]),
    #html.Li('The video you submitted will have a "depth" of 1. The node will be \
     #       dark purple, so please locate that node to properly follow the graph.'),
    ], style = {'width': '98%',
                'display': 'inline-block',
                #'text-align' : 'center'
                #'padding-left': '80px',
                #'padding-top': '20px',
               }),

    #html.Div(id='container-button-basic',
    #children=[html.Ul(children = [
    #             html.Li('The video you submitted will have a "depth" of 1. The node will be \
    #              dark purple, so please locate that node to properly follow the graph.'),
    #              html.Li('The nodes with multiple connections are "selected" videos, while \
    #          the other videos will be related videos that were not "selected".'),
    #              html.Li('Video selection is random.'),
    #              html.Li("I'd like to include more videos per node, but this app uses up youtube's API \
    #              quota quickly, so I've limited it to 5."),
    #              html.Li("I've included a default dataset (Tennis) to display in the case that the API quota \
    #              has been maxed out, so if you submit a link and it doesn't change, you can assume \
    #              that the API quota limit has been exceeded."),
    #              html.Li("'Polarity' refers to the polarity of the title. These polarities come from TextBlob.")
    #        ]),
    #    ],
    #style = {#'padding-left': '80px',
    #         'width': '49%',
    #         'display': 'inline-block'
    #        }),

    # tree plot
    html.Div([
        #dcc.Graph(figure=fig),
        dcc.Graph(id = 'tree'),
        dcc.Graph(id = 'minutes'),
        dcc.Graph(id = 'channels'),
        #dcc.Graph(figure = fig),
        #dcc.Graph(figure = fig2),
        #dcc.Graph(figure = fig3),
        #dcc.Graph(figure = fig4),
        #dcc.Graph(figure = fig5),
    ], style = {'width': '49%',
                'display': 'inline-block'
               }
    ),

    html.Div([
        #dcc.Graph(figure = fig2),
        dcc.Graph(id = 'likes'),
        #dcc.Graph(figure = fig4),
        dcc.Graph(id = 'views'),
        #dcc.Graph(figure = fig6)
        dcc.Graph(id = 'comments'),
    ], style = {'width': '49%',
                'display': 'inline-block'
               }
    ),

    #html.Div(id = 'table',
    #         style = {'width': '98%',
    #            #'display': 'inline-block'
    #            }
    #),

    html.Div([
    dash_table.DataTable(
        id = 'table',
        columns = [{"name": i, "id": i} for i in stuff.columns[1:12]],
        #data = stuff.to_dict('records'),
        #data = [],
        style_header={'backgroundColor': 'rgb(30, 30, 30)'},
        style_cell={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white',
        'textAlign': 'center'
    },)
    ], style = {'width': '98%',
                'display': 'inline-block'
                }
    ),




], #style = {'columnCount': '2'}
)
