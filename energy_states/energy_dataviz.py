from .eia_clean import clean_emissions_data, clean_consumed_data
from .eia_clean import clean_expenditures_data, clean_production_data
import plotly.express as px


def consumed_graph():
    """
    Description
    
    Returns:

    """
    title_section = "<b>Energy Consumed by Pennsylvania & Texas</b>"
    
    bar_graph = (clean_consumed_data(), clean_consumed_data().columns[2], 
            clean_consumed_data().columns[3], title_section
)
    
    return bar_graph


def emissions_graph():
    """
    Description
    
    Returns:
        
    """
    title_section =  "<b>Carbon Dioxide Emissions from Pennsylvania & Texas</b>"
    
    bar_graph = (clean_emissions_data(), clean_emissions_data().columns[3], 
            clean_emissions_data().columns[2], title_section
)
    
    return bar_graph


def expenditures_graph():
    """
    Description
    
    Returns:
        
    """
    title_section = "<b>Energy Expenditures for Pennsylvania & Texas</b>"
    
    bar_graph = (clean_expenditures_data(), clean_expenditures_data().columns[2]
            , clean_expenditures_data().columns[3], title_section
)
    
    return bar_graph


def production_graph():
    """
    Description
    
    Returns:
        
    """
    title_section = "<b>Energy Production by Pennsylvania & Texas</b>"
    
    bar_graph = (clean_production_data(), clean_production_data().columns[3], 
            clean_production_data().columns[2], title_section
)
    
    return bar_graph


def create_graph(data, y_variable, added_hover_variable, title_section):
    """
    Description
    
    Input:
        data:
        y_variable:
        added_hover_variable:
        title_section:
    
    Returns:
        
    """
    fig = px.bar(data, x = "State", y = y_variable, text = "Rank",  
            color = "State", color_discrete_sequence = ["mediumpurple", "red"], 
            pattern_shape = "State", pattern_shape_sequence=["+", "x"],
            hover_data = [added_hover_variable]
)
    
    fig.update_traces(textposition = 'outside')
    
    fig.update_layout(showlegend = False,  font = dict(size = 17),
            title = {"text": title_section
            , "y": 0.96, "x": 0.5, "xanchor": "center", "yanchor": "top"},     
)
    
    fig.show()
    
    return fig