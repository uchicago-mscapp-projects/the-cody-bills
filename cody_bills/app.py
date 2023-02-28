import random
import base64
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, get_asset_url, dash_table

app = Dash(__name__)

datatable_california = pd.read_csv("cody_bills/assets/table_california.txt").to_dict("records")
datatable_texas = pd.read_csv("cody_bills/assets/table_texas.txt").to_dict("records")

app.layout = html.Div([
    # Dashboard Explanation
    html.Div([
        html.H1("Energy Policy Text Analysis", style={'textAlign': 'center'}),
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

    # Histograms
    html.Div([
        # html.Div([
            html.H3("Histograms - Energy Policy Index"),
            html.P("""
            The histograms show the distribution of the Energy Policy
            Index, for each state.
            
            """,
            style={'width': '70%'}),
            dcc.Dropdown(
                options = ["California and Texas", "California", "Texas"],
                value = "California and Texas",
                id = "histogram-dropdown"
                # style={'width': '40%'}
                ),
                # ]),
                # ], style={'width': '25%', 'display': 'inline-block', 'margin-bottom': '100'}),
            
        # html.Div(        
            dcc.Graph(
                id = "histogram-graph", style={'width': '70%'})
                # id = "histogram-graph")], style={'width': '70%', 'display': 'inline-block'})

    ]),


# Tables
html.Div([
    html.Div([
        html.H3("Tables - Bills Metadata and Index"),
        html.P("""
        The tables show the name of each bill, the description and 
        the Energy Policy Index. It is sorted by the index from 
        greater to lowest. 
        """),
    ]),

    html.Div([
        dcc.Dropdown(
            options = ["California", "Texas"],
            value = "California",
            id = "table-dropdown",
            style={'width': '50%', 'display': 'inline-block'}
        )

    ]),

    html.Div([
        dash_table.DataTable( 
        id = "data-table",
        page_size = 30,
        fixed_rows={'headers': True},
        # filter_action='native',
        style_table={'width': '75%', 'height': '300px', 'overflowY': 'auto'})
       
])

# Closing parenthesis for table html
]),

# Wordclouds
html.Div([
    html.Div([
        html.H3("Word Clouds by State"),
        html.P("""
        The clouds present the frequency of words and bigrams of the totality of bills
        inside a state. The bigger the gram, the more frequent it is in the bills.  
        """)

    ]),

    html.Div([
    dcc.Dropdown(
        options = ["Words", "Bigrams"],
        value = "Words",
        id = "wordcloud-dropdown",
        style={'width': '50%', 'display': 'inline-block'}
    )

]),
html.Div([
    html.Div([
        html.H3("California", style={'textAlign': 'center'}),
        html.Img(
            style={'width': '100%', 'display': 'inline-block'},
            id = "wordcloud-california",
            title = "California"
        )
    
    ], style={'display': 'inline-block'}),
    html.Div([
        html.H3("Texas", style={'textAlign': 'center'}),
        html.Img(
            style={'width': '100%', 'display': 'inline-block', },
            id = "wordcloud-texas",
            title = "Texas"

        )
        ], style={'display': 'inline-block'}),

])
# closing parenthesis for wordcloud html
]),

# Bargraphs
html.Div([
    html.Div([
    dcc.Dropdown(
        options = ["Total Carbon Dioxide Emissions", "Total Energy Consumed Per Capita", "Total Energy Expenditure Per Capita", "Total Energy Production"],
        value = "Total Carbon Dioxide Emissions",
        id = "barplot-dropdown",
        style={'width': '50%', 'display': 'inline-block'}
        )
        
    ])
# Closing parenthesis for bargraphs
])

# Closing parenthesis for whole layout
])


@app.callback(
    Output(component_id = "histogram-graph", component_property = "figure"),
    Input(component_id = "histogram-dropdown", component_property = "value")
)
def graph_histogram(state):
    list_int_1 = [random.randint(0, 101) for i in range(1000)]
    list_int_2 = [random.randint(0, 101) for i in range(1000)]
    list_state_1 = ["California" for i in range(1000)]
    list_state_2 = ["Texas" for i in range(1000)]

    if state == "California":
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
    if state == "California":
        datatable = datatable_california
    else:
        datatable = datatable_texas
    
    return datatable


@app.callback(
    Output(component_id = "wordcloud-california", component_property = "src"),
    Input(component_id = "wordcloud-dropdown", component_property = "value")
)
def display_wordclouds_california(ngram_type):
    if ngram_type == "Words":
        image_path_california = "cody_bills/assets/words_california.png"
    else:
        image_path_california = "cody_bills/assets/bigrams_california.png"
       
    encoded_image = base64.b64encode(open(image_path_california, 'rb').read())

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


if __name__ == '__main__':
    app.run_server(debug=True)

## Source on how to display images on Dash dashboard
# https://community.plotly.com/t/how-to-embed-images-into-a-dash-app/61839