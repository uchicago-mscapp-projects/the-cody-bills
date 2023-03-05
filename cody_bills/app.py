import json
import random
import base64
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, get_asset_url, dash_table

datatable_pennsylvania = pd.read_csv("cody_bills/assets/table_pennsylvania.txt")
datatable_texas = pd.read_csv("cody_bills/assets/table_texas.txt")

datatable_pennsylvania_no_0 = datatable_pennsylvania[datatable_pennsylvania["Energy Policy Index"] > 0]
datatable_texas_no_0 = datatable_texas[datatable_texas["Energy Policy Index"] > 0]

total_energy_produced = pd.read_csv("cody_bills/assets/total_energy_production.txt")
total_carbon_dioxide = pd.read_csv("cody_bills/assets/total_carbon_dioxide.txt")
capita_energy_expenditure = pd.read_csv("cody_bills/assets/per_capita_energy_expenditure.txt")
capita_energy_consumed = pd.read_csv("cody_bills/assets/per_capita_energy_consumed.txt")

app = Dash(external_stylesheets=[dbc.themes.SIMPLEX])
app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([  
            dbc.Row([
                # Dashboard Explanation
                html.Div([

                    html.H1("Energy Policy Text Analysis", style = {'textAlign': 'center'}),

                    html.Br(),
                    html.P(""" 
                        This dashboard presents graphs and a table that show the results of 
                        the Energy Policy Index, calculated as a normalized frequency found
                        in legislative bills from Pennsylvania and Texas.
                        The results of the index are presented in a table and histograms, 
                        for each state. 
                        There are also clouds of the most frequent words and bigrams of 
                        the bills for each state, and descriptive graphs per state 
                        concerning different official energy metrics. 
                    """),
                    html.Br()
                ]),
            ]),

            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.H3("Tables - Bills Metadata and Index", style = {'textAlign': 'center'}),

                    html.Br(),
                    html.Div([
                        dcc.Dropdown(
                            options = ["Pennsylvania", "Texas"],
                            value = "Pennsylvania",
                            id = "table-dropdown",
                            style = {'width': '100%', 'textAlign': 'center'}
                        )

                    ]),

                    html.Br(),
                    html.P("""
                    The tables show the description, chamber (Senate or House),
                    date of issue, the Energy Policy Index. It is sorted by the index from 
                    greater to lowest. 
                    """, style = {'textAlign': 'left'}),
                ], width = 4),

                # Column of table
                dbc.Col([
                        dash_table.DataTable( 
                        id = "data-table",
                        page_size = 15,
                        fixed_rows = {'headers': True},
                        # filter_action = 'native',
                        style_cell = {"whiteSpace": "pre-line", 'textAlign': 'left'},
                        style_table={'minWidth': '100%'},
                        style_data = {'minWidth': '100px', 'maxWidth': '400px', 'height': 'auto', 'overflowY': 'auto'} ,
                        # style_table = {'width': '75%', 'overflowY': 'auto'},
                        fill_width=False,
                        style_cell_conditional = [
                            {'if': {'column_id': 'Description'},
                            'width': '400px'},
                            {'if': {'column_id': 'Chamber'},
                            'width': '100px'},
                            {'if': {'column_id': 'Created Date'},
                            'width': '200px%'},
                            {'if': {'column_id': 'Energy Policy Index'},
                            'width': '200px%'},
                            {'if': {'column_id': 'url'},
                            'width': '100px%'}
                        ],
                        style_header={
                            'backgroundColor': 'green',
                            'color': 'white',
                            'fontWeight': 'bold',
                            'textAlign': 'center'
                            },
                    )
                    
                ], width = 8)
            ], align='center'),

            html.Br(),
            dbc.Row([
                dbc.Col([

                    html.H3("Histograms - Energy Policy Index", style = {'textAlign': 'center'}),

                    html.Br(),
                    dcc.Dropdown(
                        options = ["Pennsylvania", "Pennsylvania - No Zeros", "Texas", "Texas - No Zeros"],
                        value = "Pennsylvania",
                        id = "histogram-dropdown",
                        style={'width': '100%', 'textAlign': 'center'}
                    ),

                    html.Br(),
                    html.P("""
                        The histograms show the distribution of the Energy Policy
                        Index, for each state.
                    
                    """, style = {'textAlign': 'left'}),
                ], width = 4),

                dbc.Col([
                    dcc.Graph(
                        id = "histogram-graph")
                        # id = "histogram-graph")], style={'width': '70%', 'display': 'inline-block'})
                    
                ], width=8)
            ], align='center'),

            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H3("Word Clouds by State", 
                            style = {'textAlign': 'center'}),
                    
                    html.Br(),
                    dcc.Dropdown(
                        options = ["Words", "Bigrams"],
                        value = "Words",
                        id = "wordcloud-dropdown",
                        style = {'width': '100%', 'textAlign': 'center'}
                    ),

                    html.Br(),
                    html.P("""
                        The clouds present the frequency of words and bigrams of the totality of bills
                        inside a state. The bigger the gram, the more frequent it is in the bills.  
                        """, style = {'textAlign': 'left'})

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
        
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.H3("Energy and CO2 Emission Barcharts", style = {'textAlign': 'center'}),
                    html.Br(),
                    dcc.Dropdown(
                        options = ["Percentage of U.S. Total Energy Production", 
                                    "Percentage of U.S. Total Carbon Dioxide Emissions", 
                                    "Energy Expenditure Per Capita", 
                                    "Energy Consumed Per Capita"],
                        value = "Percentage of U.S. Total Energy Production",
                        id = "barchart-dropdown",
                        style={'width': '100%', 'textAlign': 'center'}
                        ),
                    html.Br()

                ], width=4),

                dbc.Col([
                    dcc.Graph(
                        id = "barchart-graph-totals")], 
                        width=8),

            ], align='center')


        ])
    ),
])


@app.callback(
    Output(component_id = "data-table", component_property = "data"),
    Input(component_id = "table-dropdown", component_property = "value")
)
def create_table(state):
    if state == "Pennsylvania":
        datatable = datatable_pennsylvania.to_dict("records")
    else:
        datatable = datatable_texas.to_dict("records")
    
    return datatable


@app.callback(
    Output(component_id = "histogram-graph", component_property = "figure"),
    Input(component_id = "histogram-dropdown", component_property = "value")
)

def get_histogram(state):
    """
    Generates a histogram for each state following the distribution of the Normalized Energy
    Policy Index depending on some conditions to use on the dashboard:
    Inputs: 
            state: Name of the state we want to Plot the histogram of(str). The same string
                found in the dropdown of the histogram plot. Specifies if bills where no 
                keyword was found are to be included in histogram. 
    """
    if state == "Pennsylvania":
        fig = px.histogram(datatable_pennsylvania, 
                        x = "Energy Policy Index",
                        color_discrete_sequence = ["mediumpurple"],
                        pattern_shape_sequence = ["+"],
                        nbins = 40,
                        hover_data = datatable_pennsylvania.columns)

    elif state == "Pennsylvania - No Zeros":
        fig = px.histogram(datatable_pennsylvania_no_0, 
                        x = "Energy Policy Index",
                        color_discrete_sequence = ["mediumpurple"],
                        pattern_shape_sequence = ["+"],
                        nbins = 50,
                        hover_data=datatable_pennsylvania_no_0.columns)

    elif state == "Texas":
        fig = px.histogram(datatable_texas, 
                        x = "Energy Policy Index",
                        color_discrete_sequence = ["red"],
                        pattern_shape_sequence = ["x"],
                        nbins = 40,
                        hover_data=datatable_texas.columns)

    elif state == "Texas - No Zeros":
        fig = px.histogram(datatable_texas_no_0, 
                        x = "Energy Policy Index",
                        color_discrete_sequence = ["red"],
                        pattern_shape_sequence = ["x"],
                        nbins = 50,
                        hover_data=datatable_pennsylvania_no_0.columns)
    
    return fig


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
    """
    Docstring
    """
    if ngram_type == "Words":
        image_path_texas = "cody_bills/assets/words_texas.png"
    else:
        image_path_texas = "cody_bills/assets/bigrams_texas.png"

    encoded_image = base64.b64encode(open(image_path_texas, 'rb').read())

    return 'data:image/png;base64,{}'.format(encoded_image.decode())


@app.callback(
    Output(component_id = "barchart-graph-totals", component_property = "figure"),
    Input(component_id = "barchart-dropdown", component_property = "value")
)
def graph_barchart(subject):
    if subject == "Percentage of U.S. Total Energy Production":
        data = total_energy_produced
        y_variable = "Percentage of U.S. Total Energy Production"
        added_hover_variable = "Percentage of U.S. Total Energy Production"
        title_section = "<b>Percengage Energy Production by Pennsylvania & Texas</b>"

    elif subject == "Percentage of U.S. Total Carbon Dioxide Emissions":
        data = total_carbon_dioxide
        y_variable = "Percentage Carbon Dioxide Emissions"
        added_hover_variable = "Percentage of U.S. Total Carbon Dioxide Emissions"
        title_section = "<b>Carbon Dioxide Emissions from Pennsylvania & Texas</b>"

    elif subject == "Energy Expenditure Per Capita":
        data = capita_energy_expenditure
        y_variable = "Total Energy Expenditures per Capita, $"
        added_hover_variable = "Percentage of U.S. Total Energy Expenditures per Capita"
        title_section = "<b>Energy Expenditures for Pennsylvania & Texas</b>"

    else:
        data = capita_energy_consumed
        y_variable = "Total Energy Consumed per Capita, million Btu"
        added_hover_variable = "Percentage of U.S. Total Energy Consumed per Capita"
        title_section = "<b>Energy Consumed by Pennsylvania & Texas</b>"
    
    fig = px.bar(data, x = "State", y = y_variable, text = "Rank",  
        color = "State", color_discrete_sequence = ["mediumpurple", "red"], 
        pattern_shape = "State", pattern_shape_sequence=["+", "x"],
        hover_data = [added_hover_variable]
        )

    fig.update_traces(textposition = 'outside')
    
    fig.update_layout(showlegend = False,  font = dict(size = 17),
            title = {"text": title_section
            , "y": 0.96, "x": 0.5, "xanchor": "center", "yanchor": "top"}
            )

    return fig



app.run_server(port = 38456)