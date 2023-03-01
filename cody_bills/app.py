import json
import random
import base64
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, get_asset_url, dash_table

with open("cody_bills/assets/table_pennsylvania.json", "r") as file:
    datatable_pennsylvania = json.load(file)

with open("cody_bills/assets/table_texas.json", "r") as file:
    datatable_texas = json.load(file)
# SPACELAB
app = Dash(external_stylesheets=[dbc.themes.SIMPLEX])
app.layout = html.Div([
    # Dashboard Explanation
    html.Div([

        html.H1("Energy Policy Text Analysis", style = {'textAlign': 'center'}),
        html.P(""" 
            This dashboard presents graphs and a table that show the results of 
            the Energy Policy Index, calculated as a normalized frequency found
            in legislative bills from Illinois and Texas (CHANGE IF NECESSARY).
            The results of the index are presented in a histogram and a table, 
            for each state. 
            There are also clouds of the most frequent words and bigrams of 
            the bills for each state, and descriptive graphs per state 
            concerning different official energy metrics. 
        """)

    ]),

    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([

                    html.H3("Histograms - Energy Policy Index", style = {'textAlign': 'center'}),

                    dcc.Dropdown(
                        options = ["Pennsylvania", "Texas"],
                        value = "Pennsylvania",
                        id = "histogram-dropdown",
                        style={'width': '100%'}
                    ),

                    html.P("""
                        The histograms show the distribution of the Energy Policy
                        Index, for each state.
                    
                    """, style = {'textAlign': 'center'}),
                ], width = 4),

                dbc.Col([
                    dcc.Graph(
                        id = "histogram-graph")
                        # id = "histogram-graph")], style={'width': '70%', 'display': 'inline-block'})
                    
                ], width=8)
            ], align='center'),
            
            dbc.Row([
                dbc.Col([
                    html.H3("Tables - Bills Metadata and Index", style = {'textAlign': 'center'}),

                    html.Div([
                        dcc.Dropdown(
                            options = ["Pennsylvania", "Texas"],
                            value = "Pennsylvania",
                            id = "table-dropdown",
                            style = {'width': '100%'}
                        )

                    ]),

                    html.P("""
                    The tables show the name of each bill, the description and 
                    the Energy Policy Index. It is sorted by the index from 
                    greater to lowest. 
                    """, style = {'textAlign': 'center'}),
                ], width = 4),
                # Column of table
                dbc.Col([
                        dash_table.DataTable( 
                        id = "data-table",
                        page_size = 30,
                        fixed_rows = {'headers': True},
                        # filter_action='native',
                        # style_data = {'minWidth': '180px', 'width': '180px', 'maxWidth': '180px', 'height': 'auto', 'overflowY': 'auto'} ,
                        # style_table = {'width': '75%', 'height': '300px', 'overflowY': 'auto'})
                    )
                    
                ], width = 8)
            ], align='center'),

            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H3("Word Clouds by State"),

                    dcc.Dropdown(
                        options = ["Words", "Bigrams"],
                        value = "Words",
                        id = "wordcloud-dropdown",
                        style={'width': '100%'}
                    ),
                        html.P("""
                        The clouds present the frequency of words and bigrams of the totality of bills
                        inside a state. The bigger the gram, the more frequent it is in the bills.  
                        """)

                    ]),

                ], width=4),
                dbc.Col([
                    html.H3("Pennsylvania", style={'textAlign': 'center'}),
                    html.Img(
                        style={'width': '100%', 'display': 'inline-block'},
                        id = "wordcloud-pennsylvania",
                        title = "Pennsylvania"
                        )], width=4),

                dbc.Col([
                    html.H3("Texas", style={'textAlign': 'center'}),
                    html.Img(
                        style={'width': '100%', 'display': 'inline-block', },
                        id = "wordcloud-texas",
                        title = "Texas"
                    )
                ], width=4)

            ], align='center'),
        
            dbc.Row([
                dbc.Col([
                    html.H3("Energy and CO2 Emission Barcharts", style = {'textAlign': 'center'}),
                    dcc.Dropdown(
                        options = ["Total Energy - Total Carbon Dioxide", "Energy Consumed - Energy Expenditure"],
                        value = "Total Energy - Total Carbon Dioxide",
                        id = "barchart-dropdown",
                        style={'width': '100%'}
                        )

                ], width=4),

                dbc.Col([
                    dcc.Graph(
                        id = "barchart-graph-totals")], 
                        width=4),

                dbc.Col([
                    dcc.Graph(
                        id = "histogram-graph-percapita")], 
                        width=4),

            ], align='center')


        ])
    ),
])



@app.callback(
    Output(component_id = "histogram-graph", component_property = "figure"),
    Input(component_id = "histogram-dropdown", component_property = "value")
)
def graph_histogram(state):
    list_int_1 = [random.randint(0, 101) for i in range(1000)]
    list_int_2 = [random.randint(0, 101) for i in range(1000)]
    list_state_1 = ["Pennsylvania" for i in range(1000)]
    list_state_2 = ["Texas" for i in range(1000)]

    if state == "Pennsylvania":
        fig = px.histogram(list_int_1)
    elif state == "Texas":
        fig = px.histogram(list_int_2)
    else:
        list_ints = list_int_1 + list_int_2
        list_states = list_state_1 + list_state_2
        df = pd.DataFrame({"state": list_states, "energy_index": list_ints})

        fig = px.histogram(df, x = "energy_index", color = "state", barmode = "overlay")

    return fig

@app.callback(
    Output(component_id = "data-table", component_property = "data"),
    Input(component_id = "table-dropdown", component_property = "value")
)
def create_table(state):
    if state == "Pennsylvania":
        datatable = datatable_pennsylvania
    else:
        datatable = datatable_texas
    
    return datatable

@app.callback(
    Output(component_id = "wordcloud-pennsylvania", component_property = "src"),
    Input(component_id = "wordcloud-dropdown", component_property = "value")
)
def display_wordclouds_pennsylvania(ngram_type):
    if ngram_type == "Words":
        image_path_pennsylvania = "cody_bills/assets/words_pennsylvania.png"
    else:
        image_path_pennsylvania = "cody_bills/assets/bigrams_pennsylvania.png"
       
    encoded_image = base64.b64encode(open(image_path_pennsylvania, 'rb').read())

    return 'data:image/png;base64,{}'.format(encoded_image.decode())

@app.callback(
    Output(component_id = "wordcloud-texas", component_property = "src"),
    Input(component_id = "wordcloud-dropdown", component_property = "value")
)
def display_wordclouds_texas(ngram_type):
    if ngram_type == "Words":
        image_path_texas = "cody_bills/assets/words_texas.png"
    else:
        image_path_texas = "cody_bills/assets/bigrams_texas.png"

    encoded_image = base64.b64encode(open(image_path_texas, 'rb').read())

    return 'data:image/png;base64,{}'.format(encoded_image.decode())

# @app.callback(
#     Output(component_id = "barchart-graph-totals", component_property = "figure"),
#     Input(component_id = "barchart-dropdown", component_property = "value")
# )
# def graph_barchart(subjects):
    


app.run_server()

# poetry add -dev (wordcloud, preprocessing, etc.)

