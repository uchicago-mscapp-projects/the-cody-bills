#########################################################
#####   This code was written by John Christenson   ##### 
#########################################################

from cody_bills.energy_states.eia_clean import clean_consumed_data
from cody_bills.energy_states.eia_clean import clean_emissions_data
from cody_bills.energy_states.eia_clean import clean_expenditures_data
from cody_bills.energy_states.eia_clean import clean_production_data

#Run tests with <$ poetry run pytest tests/test_eia_clean.py>

def test_clean_consumed_data():
    data = clean_consumed_data()
    assert (data.columns[1] == "State"), "Expected State, got {}".format(
    data.columns[1]
)


def test_clean_emissions_data():
    data = clean_emissions_data()
    assert (len(data) == 2), "Expected 2, got {}".format(len(data))
    assert data.columns[3] == (
    "Percentage of U.S. Total Carbon Dioxide Emissions"
    ), """Expected Percentage of U.S. Total Carbon Dioxide Emissions, 
    got {}""".format(data.columns[3]
)

    
def test_clean_expenditures_data():
    data = clean_expenditures_data()
    assert (data.columns[0] == "Rank"), "Expected Rank, got {}".format(
    data.columns[0]
)


def test_clean_production_data():
    data = clean_production_data()