from .eia_clean import clean_emissions_data, clean_consumed_data
from .eia_clean import clean_expenditures_data, clean_production_data
import pandas as pd
import plotly.express as px

# import matplotlib.pyplot as plt
# import seaborn as sns
# import numpy as np

def create_graph():
    """
    """
    
    
    # graph = sns.barplot(x=  clean_emissions_data().columns[1], 
    #                 y=clean_emissions_data().columns[2], data=clean_emissions_data(),
    #                 errwidth=0)

    # for rank in clean_emissions_data().columns[0]:
    #     graph.bar_label(rank,) 
    
    
    # # graph = sns.barplot(x=  clean_emissions_data()[clean_emissions_data().columns[1]], 
    # #                 y=clean_emissions_data()[clean_emissions_data().columns[2]], data=clean_emissions_data(),
    # #                 errwidth=0)

    # # for rank in clean_emissions_data()[clean_emissions_data().columns[0]]:
    # #     graph.bar_label(rank,)
    
    # fig = graph.get_figure()
    # fig.savefig("output.png")
    # print(graph)
    # return graph

    # data[data.columns[2]]