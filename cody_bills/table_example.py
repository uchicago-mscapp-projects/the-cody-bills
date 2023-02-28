from dash import Dash, dash_table
import pandas as pd
import numpy as np

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
random_california = np.random.randint(low=2, high=10, size=(1000,3))
cols = ["Bill", "Description", "Energy Policy Index"]
df_california = pd.DataFrame(random_california, columns = cols)


app = Dash(__name__)

app.layout = dash_table.DataTable(df_california.to_dict('records'))
# app.layout = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])


if __name__ == '__main__':
    app.run_server(debug=True)