import random 
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        options = ["California and Texas", "California", "Texas"],
        value = "California and Texas",
        id = "histogram-dropdown",
        style={'width': '50%', 'display': 'inline-block'}
    ),

    html.Div(
        dcc.Graph(
            id = "histogram-graph"
        )
    )

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


if __name__ == '__main__':
    app.run_server(debug=True)
