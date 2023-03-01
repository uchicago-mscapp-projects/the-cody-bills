import pytest
from eia_states.eia_clean import clean_emissions_data, clean_consumed_data, clean_expenditures_data,  clean_production_data

def test_clean_emissions_data():
    data = clean_emissions_data()
    # after cleaning
    assert (len(data) == 2
    ), "Expected 2, got {}".format(len(data))
    assert data.columns[3] == ("Percentage of U.S. Total Carbon Dioxide Emissions"
    )
    
