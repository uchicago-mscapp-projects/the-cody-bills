# The process_input_json and display_wordclouds functions
# were done by Pablo Montenegro Helfer
# The get_histogram function was done by Santiago Satizábal 
# and Pablo Montenegro Helfer
import json
import pandas as pd
import base64
import plotly.express as px

def process_input_json(json_file):
    """
    This function does a minor preprocessing of the input JSON file 
    with the Energy Policy Index and metadata, in order to create a
    dataframe ordered by the index.

    Input:
        json_file(json): the JSON file with the information

    Returns:
        df(Pandas DataFrame): dataframe ready to use in visualization

    """
    with open(json_file, "r") as file:
        df = pd.DataFrame(json.load(file))

    df["Energy Policy Index"] = (df["Norm_EPol_Index"] * 100).round(4)
    df.drop(columns = ["Norm_EPol_Index", "Bill ID", "State"], axis = 1, inplace = True)
    df = df.sort_values(by = "Energy Policy Index", ascending = False)
    df.rename(columns = {"url": "URL"}, inplace = True)

    return df


def display_wordclouds(ngram_type, state):
    """ 
    Select the appropriate image from the assets folder, 
    encode it with base 64 and return the object.

    Inputs:
        ngram_type(str): Words or Bigrams
        state(str): Pennsylvania or Texas

    Returns: 
        image(PNG - base64): the image of the cloud
    """
    if ngram_type == "Words" and state == "Pennsylvania":
        image_path = "cody_bills/assets/words_pennsylvania.png"

    elif ngram_type == "Words" and state == "Texas":
        image_path = "cody_bills/assets/words_texas.png"
    
    elif ngram_type == "Bigrams" and state == "Pennsylvania":
        image_path = "cody_bills/assets/bigrams_pennsylvania.png"

    else:
        image_path = "cody_bills/assets/bigrams_texas.png"

    # The below code was found from this source
    # # https://community.plotly.com/t/how-to-embed-images-into-a-dash-app/61839
    encoded_image = base64.b64encode(open(image_path, 'rb').read())

    return 'data:image/png;base64,{}'.format(encoded_image.decode())


def get_histogram(dropdown_select, datatable):
    """
    Generates a histogram for each state following the distribution of the Normalized Energy
    Policy Index depending on some conditions to use on the dashboard:
    
    Inputs: 
        dropdown_select(str): state selected by user in the dropdown selection, 

            specifying if graph should not include bills where no keyword was found.
    Returns: 
        fig(Plotly Express Figure): the histogram graph figure
            from Plotly Express
    """
    if dropdown_select.startswith("Pennsylvania"):
        color_bar = ["mediumpurple"]
        pattern_bar = ["+"]

    else:
        color_bar = ["red"]
        pattern_bar = ["x"]
       
    if dropdown_select == "Pennsylvania":
        title_section = "<b>Histogram Pennsylvania</b>"
        bins = 40
    elif dropdown_select == "Pennsylvania - No Zeros":
        title_section = "<b>Histogram Pennsylvania - No Zeros</b>"
        bins = 50
    elif dropdown_select == "Texas":
        title_section = "<b>Histogram Texas</b>"
        bins = 40
    elif dropdown_select == "Texas - No Zeros":
        title_section = "<b>Histogram Texas - No Zeros</b>"
        bins = 50

    fig = px.histogram(datatable, 
                    x = "Energy Policy Index",
                    color_discrete_sequence = color_bar,
                    pattern_shape_sequence = pattern_bar,
                    nbins = bins,
                    hover_data = datatable.columns)

    fig.update_layout(showlegend = False,  font = dict(size = 15),
            title = {"text": title_section
            , "y": 0.95, "x": 0.5, "xanchor": "center", "yanchor": "top"}
            )

    return fig
