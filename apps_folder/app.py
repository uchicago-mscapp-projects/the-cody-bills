import random
import base64
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, get_asset_url, dash_table

app = Dash(__name__)

datatable_california = pd.read_csv("apps_folder/assets/table_california.txt").to_dict("records")
datatable_texas = pd.read_csv("apps_folder/assets/table_texas.txt").to_dict("records")

app.layout = html.Div([
    # Histograms
    html.Div([
    dcc.Dropdown(
        options = ["California and Texas", "California", "Texas"],
        value = "California and Texas",
        id = "histogram-dropdown",
        style={'width': '50%', 'display': 'inline-block'}
    ),

    html.Div(
        dcc.Graph(
            id = "histogram-graph",
            style={'width': '80%', 'display': 'inline-block'}
        )
    )
# Closing parenthesis for histogram html
]),

# Tables
html.Div([
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
        style_table={'width': '75%', 'height': '300px', 'overflowY': 'auto'})
       
])

# Closing parenthesis for table html
]),

# Wordclouds
html.Div([
    html.Div([
    dcc.Dropdown(
        options = ["Words", "Bigrams"],
        value = "Words",
        id = "wordcloud-dropdown",
        style={'width': '50%', 'display': 'inline-block'}
    )

]),
html.Div([
    html.Img(
        style={'width': '40%', 'display': 'inline-block'},
        id = "wordcloud-california"
    ),
    html.Img(
        style={'width': '40%', 'display': 'inline-block'},
        id = "wordcloud-texas"
    )

])
# closing parenthesis for wordcloud html
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
        image_path_california = "apps_folder/assets/words_california.png"
    else:
        image_path_california = "apps_folder/assets/bigrams_california.png"
       
    encoded_image = base64.b64encode(open(image_path_california, 'rb').read())

    return 'data:image/png;base64,{}'.format(encoded_image.decode())

@app.callback(
    Output(component_id = "wordcloud-texas", component_property = "src"),
    Input(component_id = "wordcloud-dropdown", component_property = "value")
)
def display_wordclouds_texas(ngram_type):
    if ngram_type == "Words":
        image_path_texas = "apps_folder/assets/words_texas.png"
    else:
        image_path_texas = "apps_folder/assets/bigrams_texas.png"

    encoded_image = base64.b64encode(open(image_path_texas, 'rb').read())

    return 'data:image/png;base64,{}'.format(encoded_image.decode())


if __name__ == '__main__':
    app.run_server(debug=True)

## Source on how to display images on Dash dashboard
# https://community.plotly.com/t/how-to-embed-images-into-a-dash-app/61839