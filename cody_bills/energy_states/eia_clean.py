import pandas as pd

def clean_consumed_data():
    """
    Read in and clean the U.S. Total Energy Consumed per Capita by State data 
    from the U.S. Energy Information Administration (EIA).
    
    Returns:
        A cleaned and edited dataframe of energy consumed data
    """
    consumed_filename = "energy_states/eia_states_data/raw_data/TotalEnergyConsumedperCapita-StateRankings.csv"    
    
    return clean(consumed_filename) 


def clean_emissions_data():
    """
    Read in and clean the U.S. Carbon Dioxide Emissions by State data from the 
    U.S. Energy Information Administration (EIA).
    
    Returns:
        A cleaned and edited dataframe of CO2 emissions data 
    """
    emissions_filename = "energy_states/eia_states_data/raw_data/TotalCarbonDioxideEmissions-StateRankings.csv"
    
    return clean(emissions_filename)

        
def clean_expenditures_data():
    """
    Read in and clean the U.S. Total Energy Expenditures per Capita by State 
    data from the U.S. Energy Information Administration (EIA).
    
    Returns:
        A cleaned and edited dataframe of energy expenditures data 
    """
    expenditures_filename = "energy_states/eia_states_data/raw_data/TotalEnergyExpendituresperCapita-StateRankings.csv"
    
    return clean(expenditures_filename)


def clean_production_data():
    """
    Read in and clean the U.S. Total Energy Production by State data from the 
    U.S. Energy Information Administration (EIA).
    
    Returns:
        A cleaned and edited dataframe of energy production data 
    """
    production_filename  = "energy_states/eia_states_data/raw_data/TotalEnergyProduction-StateRankings.csv"
    
    return clean(production_filename)


def clean(filename):
    """
    Clean a csv file of data based off the filename read in.  The cleaning 
    steps include:
    - Summing the total of the Consumed, CO2 Emissions, Expenditures, 
        or Production column then using that variable to create a new 
        percentage of the total U.S. column
    - Dropping rows (State(s)) & columns that won't be utilized
    - Adding contextual info to the "Rank" variable
    - Changing the state abbreviation(s) to the full state name(s)
    
    Inputs:
        filename (string): The filename with the pathway to load in one of the 
            raw_data files with eia_states_data
    
    Returns:
        A cleaned dataframe
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


def save_cleaned_dataframe(data, file_path):
    """
    Take a cleaned dataframe and save it as a csv file to the cleaned_data 
    folder within the eia_states_data folder.
    
    Inputs:
        data (dataframe): A cleaned dataframe
        file_path (string): The pathway for how the csv file should be saved
    """
    data.to_csv(file_path, index=False)



def save_all_cleaned():
    """
    Initialize the cleaning and then saving of the consumed, emissions, 
    expenditures, and production data.
    """
    save_cleaned_dataframe(clean_consumed_data(), 
            "energy_states/eia_states_data/cleaned_data/cleaned_consumed.txt"
)
    save_cleaned_dataframe(clean_emissions_data(), 
            "energy_states/eia_states_data/cleaned_data/cleaned_emissions.txt"
)
    save_cleaned_dataframe(clean_expenditures_data(),
            "energy_states/eia_states_data/cleaned_data/cleaned_expenditures.txt"
)
    save_cleaned_dataframe(clean_production_data(), 
            "energy_states/eia_states_data/cleaned_data/cleaned_production.txt"
)

#States and DC included here, towards bottom and not at top out of 
#   personal preference
us_states_anddc = {"AK": "Alaska",
            "AL": "Alabama",
            "AR": "Arkansas",
            "AZ": "Arizona",
            "CA": "California",
            "CO": "Colorado",
            "CT": "Connecticut",
            "DC": "District of Columbia",
            "DE": "Delaware",
            "FL": "Florida",
            "GA": "Georgia",
            "HI": "Hawaii",
            "IA": "Iowa",
            "ID": "Idaho",
            "IL": "Illinois",
            "IN": "Indiana",
            "KS": "Kansas",
            "KY": "Kentucky",
            "LA": "Louisiana",
            "MA": "Massachusetts",
            "MD": "Maryland",
            "ME": "Maine",
            "MI": "Michigan",
            "MN": "Minnesota",
            "MO": "Missouri",
            "MS": "Mississippi",
            "MT": "Montana",
            "NC": "North Carolina",
            "ND": "North Dakota",
            "NE": "Nebraska",
            "NH": "New Hampshire",
            "NJ": "New Jersey",
            "NM": "New Mexico",
            "NV": "Nevada",
            "NY": "New York",
            "OH": "Ohio",
            "OK": "Oklahoma",
            "OR": "Oregon",
            "PA": "Pennsylvania",
            "RI": "Rhode Island",
            "SC": "South Carolina",
            "SD": "South Dakota",
            "TN": "Tennessee",
            "TX": "Texas",
            "UT": "Utah",
            "VA": "Virginia",
            "VT": "Vermont",
            "WA": "Washington",
            "WI": "Wisconsin",
            "WV": "West Virginia",
            "WY": "Wyoming"
}

#run function from cd 30122-project-the-cody-bills within a poetry shell
#   poetry run python energy_states/eia_clean.py
save_all_cleaned()