import json
import pandas as pd

def process_input_json(json_file):
    """
    This function does a minor preprocessing of the input JSON file 
    with the Energy Policy Index and metadata, in order to create a
    dataframe ordered by the index.

    Input:
        json_file(json): the JSON file with the information
    Returns:

    """
    with open(json_file, "r") as file:
        df = pd.DataFrame(json.load(file))

    df["Energy Policy Index"] = (df["Norm_EPol_Index"] * 100).round(4)
    df.drop(columns = ["Norm_EPol_Index", "Bill ID", "State"], axis = 1, inplace = True)
    df = df.sort_values(by = "Energy Policy Index", ascending = False)
    df.rename(columns = {"url": "URL"}, inplace = True)

    return df
