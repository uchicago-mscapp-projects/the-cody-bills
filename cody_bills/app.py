# The code of this file was done by Pablo Montenegro Helfer

import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, dash_table
from cody_bills.utils import helper_functions
from cody_bills.energy_states import energy_dataviz

# Open the json files with the metadata and index, 
# and do minor preprocess for visualization
datatable_pennsylvania = helper_functions.process_input_json("cody_bills/assets/table_pennsylvania.json")
datatable_texas = helper_functions.process_input_json("cody_bills/assets/table_texas.json")

# Create dataframe table with descriptive statistics 
# of the Energy Policy Index for each state
descr_penn = datatable_pennsylvania.describe().rename(columns = 
                        {"Energy Policy Index": "Pennsylvania"}).round(4)

descr_tex = datatable_texas.describe().rename(columns = 
                        {"Energy Policy Index": "Texas"}).round(4)
                        
descr_table = pd.concat([descr_penn, descr_tex], axis = 1).T.reset_index()
list_metrics = ["State", "No. of bills", "Mean", "Standard Deviation", 
                "Minimum", "25th Percentile", "Median", 
                "75th percentile", "Maximum"]

descr_table.columns = list_metrics

# Create tables without without the indexes 
# with zeros (used in histogram)
datatable_pennsylvania_no_0 = datatable_pennsylvania[datatable_pennsylvania["Energy Policy Index"] > 0]
datatable_texas_no_0 = datatable_texas[datatable_texas["Energy Policy Index"] > 0]

# app object creation and style definition
app = Dash(external_stylesheets=[dbc.themes.SIMPLEX])
# app layout, whole design goes here
app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([  
            # Dashboard Explanation
            dbc.Row([
                html.Div([

                    html.H1("Energy Policy Text Analysis", 
                        style = {'textAlign': 'center'}),

                    html.Br(),
                    html.P(""" 
                        This dashboard presents graphs and tables 
                        that show the results of the Energy Policy 
                        Index, calculated as a normalized frequency found
                        in legislative bills from Pennsylvania and Texas. 
                        It also shows clouds of the most frequent words and 
                        bigrams of the bills for each state, and 
                        descriptive graphs per state concerning different 
                        official energy metrics, as well as a table with 
                        the metadata and index of each bill. 

                        The Energy Policy Index ranges from 0 to 100. 
                        A bill with an index of 0 has no keywords related 
                        to energy policy. The greater the index, the more 
                        related it is with energy policy. The bill with 
                        an index of 100 has the most keywords (relative 
                        to its size) related to energy policy. 
                    """),
                    html.Br(),
                ]),  
            ]),
            
            html.Br(),
            # Descriptive Statistics of the Energy Index
            dbc.Row([
                dbc.Col([
                    html.H3("Energy Policy Index - Descriptive Statistics", 
                        style = {'textAlign': 'center'}),

                    html.Br(),
                    html.P("""
                        This table shows some descriptive metrics calculated 
                        for the Energy Policy Index. This way it is 
                        possible to see the distribution of de index 
                        and its mean in each state. 
                        """)
                
                ], width = 4),

                dbc.Col([
                        dash_table.DataTable( 
                        descr_table.to_dict('records'),
                        page_size = 15,
                        style_table = {'width': '100%', 'overflowY': 'auto'},
                        style_data = {'textAlign': 'center'},
                        fill_width=False,

                        style_header={
                            'backgroundColor': 'green',
                            'color': 'white',
                            'fontWeight': 'bold',
                            'textAlign': 'center'
                            },
                    )

                ], width = 8, style = {'textAlign': 'center'})

            ]),

            html.Br(),
            # Histograms of the Energy Index
            dbc.Row([
                dbc.Col([

                    html.H3("Histograms - Energy Policy Index", 
                            style = {'textAlign': 'center'}),

                    html.Br(),
                    dcc.Dropdown(
                        options = ["Pennsylvania", "Pennsylvania - No Zeros", 
                                "Texas", "Texas - No Zeros"],
                        value = "Pennsylvania",
                        id = "histogram-dropdown",
                        style={'width': '100%', 'textAlign': 'center'}
                    ),

                    html.Br(),
                    html.P("""
                        The histograms show the distribution of the 
                        Energy Policy Index, for each state, and 
                        with the option of not showing 
                        the bills that contained no keywords 
                        (option "No Zeros").
                    
                    """, style = {'textAlign': 'left'}),
                ], width = 4),

                dbc.Col([
                    dcc.Graph(
                        id = "histogram-graph")
                    
                ], width=8)
            ], align='center'),

            html.Br(),
            # Wordclouds
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
                        The clouds present the frequency of words and 
                        bigrams of the totality of bills
                        inside a state. The bigger the gram, 
                        the more frequent it is in the bills.  
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
            # Barcharts
            dbc.Row([
                dbc.Col([
                    html.H3("Energy and CO2 Emission Barcharts", 
                        style = {'textAlign': 'center'}),
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

                    html.Br(),
                    html.P("""
                        There are 4 variables related to energy policy, 
                        which are presented in each bar chart for each 
                        state. The graphs also show the ranking of the 
                        state, compared to every US state. Each variable 
                        is selected from the above dropdown. 
                        """)

                ], width=4),

                dbc.Col([
                    dcc.Graph(
                        id = "barchart-graph-totals")], 
                        width=8),

            ], align='center'),

            html.Br(),
            # Table
            dbc.Row([
                dbc.Col([
                    html.H3("Tables - Bills Metadata and Index", 
                        style = {'textAlign': 'center'}),

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
                    The tables show the description, chamber 
                    (Senate or House), date of issue, the Energy 
                    Policy Index and the URL to access the original 
                    bill. It is sorted by the index from greatest to 
                    lowest. 
                    """, style = {'textAlign': 'left'}),
                ], width = 4),

                dbc.Col([
                        dash_table.DataTable( 
                        id = "data-table",
                        page_size = 15,
                        fixed_rows = {'headers': True},
                        style_cell = {"whiteSpace": "pre-line", 
                            'textAlign': 'left'},
                        style_table={'minWidth': '100%'},
                        style_data = {'minWidth': '100px', 'maxWidth': '400px', 
                            'height': 'auto', 'overflowY': 'auto'} ,
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
            ], align='center')

        ])
    ),
])


# All the callbacks require the function below to have a structure
# with "def" and "return" statements (not able to import a function
# and use it)
@app.callback(
    Output(component_id = "data-table", component_property = "data"),
    Input(component_id = "table-dropdown", component_property = "value")
)
def create_table(state):
    """ 
    Create a dictionary from the Pandas input dataframe with the 
    Pandas method "to_dict", depending on the state selection
    from the user. This dictionary is the input Dash needs to 
    display the table. 

    Inputs:
        state(str): the state selected by the user
    Returns:
        datatable(dict): the datatable from the selected
            state as a dictionary

    """
    if state == "Pennsylvania":
        datatable = datatable_pennsylvania.to_dict("records")
    else:
        datatable = datatable_texas.to_dict("records")
    
    return datatable


@app.callback(
    Output(component_id = "histogram-graph", component_property = "figure"),
    Input(component_id = "histogram-dropdown", component_property = "value")
)

def get_histogram(dropdown_select):
    """
    Generates a histogram for each state following the 
    distribution of the Normalized Energy Policy Index 
    depending on some conditions to use on the dashboard.

    Inputs: 
        dropdown_select(str): state selected by 
            user in the dropdown selection, 
            specifying if graph should not include bills 
            where no keyword was found.

    Returns: 
        fig(Plotly Express Figure): the histogram graph figure
            from Plotly Express

    """
    if dropdown_select == "Pennsylvania":
        fig = helper_functions.get_histogram(dropdown_select, 
                                        datatable_pennsylvania)

    elif dropdown_select == "Pennsylvania - No Zeros":
        fig = helper_functions.get_histogram(dropdown_select, 
                                    datatable_pennsylvania_no_0)

    elif dropdown_select == "Texas":
        fig = helper_functions.get_histogram(dropdown_select, 
                                                datatable_texas)
    
    else:
         fig = helper_functions.get_histogram(dropdown_select, 
                                            datatable_texas_no_0)       

    return fig


@app.callback(
    Output(component_id = "wordcloud-pennsylvania", component_property = "src"),
    Input(component_id = "wordcloud-dropdown", component_property = "value")
)

def display_wordclouds_pennsylvania(ngram_type):
    """
    Create the corresponding image object to display 
    in the dashboard for Pennsylvania

    Inputs:
        ngram_type(str): Words or Bigrams

    Returns: 
        image(PNG - base64): the image of the cloud
    """
    image = helper_functions.display_wordclouds(ngram_type, "Pennsylvania")

    return image


@app.callback(
    Output(component_id = "wordcloud-texas", component_property = "src"),
    Input(component_id = "wordcloud-dropdown", component_property = "value")
)

def display_wordclouds_texas(ngram_type):
    """
    Create the corresponding image object to display 
    in the dashboard for Texas

    Inputs:
        ngram_type(str): Words or Bigrams

    Returns: 
        image(PNG - base64): the image of the cloud
    """
    image = helper_functions.display_wordclouds(ngram_type, "Texas")

    return image


@app.callback(
    Output(component_id = "barchart-graph-totals", component_property = "figure"),
    Input(component_id = "barchart-dropdown", component_property = "value")
)

def graph_barchart(subject):
    """
    Create the figure of the barchart from the function 
    of the energy_states data visualization folder. 

    Inputs:
        subject(str): the subject from the bar chart 
        dropdown, selected by the user. 

    Returns: 
        fig(Plotly Express Figure): the bar graph figure
        from Plotly Express
    """
    fig = energy_dataviz.dash_bar_graph(subject)
    
    return fig


app.run_server(port = 38456)