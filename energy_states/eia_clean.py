import pandas as pd
import pathlib
from .states_dict import us_states_anddc


def clean_consumed_data():
    """
    Description
    
    Returns:
        A cleaned and edited dataframe of eia 
    """
    consumed_filename = pathlib.Path(__file__).parent / """eia_states_data/TotalEnergyConsumedperCapita-StateRankings.csv"""
    
    return clean(consumed_filename) 


def clean_emissions_data():
    """
    Description
    
    Returns:
        
    """
    emissions_filename = pathlib.Path(__file__).parent / """eia_states_data/TotalCarbonDioxideEmissions-StateRankings.csv"""
    
    return clean(emissions_filename)

        
def clean_expenditures_data():
    """
    Description
    
    Returns:
        
    """
    expenditures_filename = pathlib.Path(__file__).parent / """eia_states_data/TotalEnergyExpendituresperCapita-StateRankings.csv"""
    
    return clean(expenditures_filename)


def clean_production_data():
    """
    Description
    
    Returns:
        
    """
    production_filename = pathlib.Path(__file__).parent / """eia_states_data/TotalEnergyProduction-StateRankings.csv"""
    
    return clean(production_filename)


def clean(filename):
    """
    Description
    
    Inputs:
        filename
    
    Returns:
        
    """
    data_to_clean = pd.read_csv(filename)
    data = data_to_clean.copy() 
    
    #FYI data.columns[2] is the "Total Energy (Consumed, CO2 Emissions, 
    #   Expenditures, or Production)" for each each State and DC
    total_of_category = data[data.columns[2]].sum()

    #Dropping rows for data that are not PA and TX
    data.drop(data[~data["State"].isin(["PA", "TX"])].index, inplace=True)
    #Dropping the empty "Note:..." column
    data = data.drop(data.columns[3], axis=1) 
    
    percentage_category_name = "Percentage of U.S. " + data.columns[2].split(
                ',', 1)[0]
    #Creating a percentage category dividing the unique data column to the
    #   total of all States and DC then multiplying by 100%
    data[percentage_category_name] = (data[data.columns[2]] / 
                total_of_category) * 100
    
    data[["Rank", "State"]] = data.apply(lambda row: 
                ["State Ranked <b>{}</b> out of 51".format(row["Rank"]),
                us_states_anddc[row["State"]]], axis = 1, 
                result_type = "expand"
)
 
    data = data.sort_values("State")
    
    return data 