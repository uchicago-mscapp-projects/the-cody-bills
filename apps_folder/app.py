import random 
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import base64

app = Dash(__name__)

app.layout = html.Div([
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
    Output(component_id = "wordcloud-california", component_property = "src"),
    Input(component_id = "wordcloud-dropdown", component_property = "value")
)
def display_image(ngram_type):
    if ngram_type == "Words":
        image_path_california = "apps_folder/wordcloud_images/words_california.png"
    else:
        image_path_california = "apps_folder/wordcloud_images/bigrams_california.png"
       
    encoded_image = base64.b64encode(open(image_path_california, 'rb').read())

    return 'data:image/png;base64,{}'.format(encoded_image.decode())

@app.callback(
    Output(component_id = "wordcloud-texas", component_property = "src"),
    Input(component_id = "wordcloud-dropdown", component_property = "value")
)
def display_image(ngram_type):
    if ngram_type == "Words":
        image_path_texas = "apps_folder/wordcloud_images/words_texas.png"
    else:
        image_path_texas = "apps_folder/wordcloud_images/bigrams_texas.png"

    encoded_image = base64.b64encode(open(image_path_texas, 'rb').read())

    return 'data:image/png;base64,{}'.format(encoded_image.decode())


if __name__ == '__main__':
    app.run_server(debug=True)
