import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import numpy as np
import pytest


from energy_states.eia_clean import clean_emissions_data, clean_consumed_data 
from energy_states.eia_clean import clean_expenditures_data,  clean_production_data
from energy_states.energy_dataviz import create_graph

def test_graph():
    graph = create_graph()
    
    assert graph
    