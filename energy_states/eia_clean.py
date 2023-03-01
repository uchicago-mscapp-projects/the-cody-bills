import pandas as pd
import pathlib

def clean_emissions_data():
    """
    """
    emissions_filename = pathlib.Path(__file__).parent / """eia_states_data/TotalCarbonDioxideEmissions-StateRankings.csv"""
    
    return clean(emissions_filename)
    
        
def clean_consumed_data():
    """
    """
    consumed_filename = pathlib.Path(__file__).parent / """data/TotalEnergyConsumedperCapita-StateRankings.csv"""
    
    return clean(consumed_filename) 
        
def clean_expenditures_data():
    """
    """
    expenditures_filename = pathlib.Path(__file__).parent / """data/
                        TotalEnergyExpendituresperCapita-StateRankings.csv"""
    
    return clean(expenditures_filename)
    
def clean_production_data():
    """
    """
    production_filename = pathlib.Path(__file__).parent / """data/
                        TotalEnergyProduction-StateRankings.csv"""
    
    return clean(production_filename)


def clean(filename):
    """
    """
    data_to_clean = pd.read_csv(filename)
    
    data = data_to_clean.copy() 
    
    percentage_category_name = "Percentage of U.S. " + data.columns[2].split(
                        ',', 1)[0]
    
    total_of_category = data[data.columns[2]].sum()

    data.drop(data[~data["State"].isin(["IL", "TX"])].index, inplace=True)
    
    data = data.drop(data.columns[3], axis=1) 
    
    data = data.sort_values("State")
    
    data[percentage_category_name] = (data[data.columns[2]] / 
                        total_of_category) * 100
    
    return data 