#########################################################
#####   This code was written by John Christenson   ##### 
#########################################################

from cody_bills.energy_states.energy_dataviz import consumed_graph
from cody_bills.energy_states.energy_dataviz import emissions_graph
from cody_bills.energy_states.energy_dataviz import expenditures_graph 
from cody_bills.energy_states.energy_dataviz import production_graph

#Run tests with <$ poetry run pytest tests/test_energy_dataviz.py>

def test_consumed_graph():
    graph = consumed_graph()

def test_emissions_graph():
    graph = emissions_graph()

def test_expenditures_graph():
    graph = expenditures_graph()
    
def test_production_graph():
    graph = production_graph()