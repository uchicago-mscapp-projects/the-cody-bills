from energy_states.energy_dataviz import consumed_graph, emissions_graph
from energy_states.energy_dataviz import expenditures_graph, production_graph
#Be sure to <$ pip3 install -U kaleido>
# After use <$ pip3 uninstall -y kaleido> to prevent potential issues

#Run tests with <$ poetry run pytest tests/test_energy_dataviz.py>

def test_consumed_graph():
    graph = consumed_graph()

def test_emissions_graph():
    graph = emissions_graph()

def test_expenditures_graph():
    graph = expenditures_graph()
    
def test_production_graph():
    graph = production_graph()