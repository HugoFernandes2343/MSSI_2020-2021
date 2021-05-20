from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from parking_lot_model import ParkingModel
from mesa.visualization.modules import ChartModule
from histogram_module import HistogramModule
from mesa.visualization.UserParam import UserSettableParameter


# metodo de representacao das bolinhas vermelhas TODO adaptar para carros

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5}
##todo change this to only have red balls and black squares
    if agent.flag == 1:
        portrayal["Color"] = "black"
        portrayal["Layer"] = 0
        portrayal["Shape"] = "rect"
        portrayal["w"] = 1
        portrayal["h"] = 1
    else:
        if agent.flag == 0:
            portrayal["Color"] = "red"
            portrayal["Layer"] = 1

    return portrayal


grid = CanvasGrid(agent_portrayal, 20, 20, 800,800 )

#chart = ChartModule([{"Label": "Gini",
#                      "Color": "Black"}],
 #                   data_collector_name='datacollector')

#histogram = HistogramModule(list(range(10)), 200, 500)

""" 
Parameter types include:

'number' - a simple numerical input
'checkbox' - boolean checkbox
'choice' - String-based dropdown input, for selecting choices within a model
'slider' - A number-based slider input with settable increment
'static_text' - A non-input textbox for displaying model info.

 """

model_params = {
    "N":10, 
    "width":20, 
    "height":20,
    "Strategy": UserSettableParameter("choice", 'Strategy to Use', value='1 - Default',
                                        choices=['1 - Default', '2 - Premium Spots', '3 - Max Time', '4 - Scalling', '5 - Reservation']),
    "N_cars": UserSettableParameter("slider", "Number of cars", value=20, min_value=5, max_value=100, step=1),
    "N_spots": UserSettableParameter("slider", "Number of Parking Spots", value=20, min_value=20, max_value=100, step=1),
    "Price_hour": UserSettableParameter("slider", "Price per hour", value=0.1, min_value=0.1, max_value=10.0, step=0.1),
    "N_tier1_spots": UserSettableParameter("slider", "strat 2: Number of Parking Spots for tier 1", value=20, min_value=5, max_value=100, step=1),
    "N_tier1_price": UserSettableParameter("slider", "strat 2: Price per hour for tier 1", value=0.1, min_value=0.1, max_value=10.0, step=0.1),
    "N_tier2_spots": UserSettableParameter("slider", "strat 2: Number of Parking Spots for tier 2", value=10, min_value=5, max_value=50, step=1),
    "N_tier2_price": UserSettableParameter("slider", "strat 2: Price per hour for tier 2", value=0.1, min_value=0.1, max_value=10.0, step=0.1),
    "N_tier3_spots": UserSettableParameter("slider", "strat 2: Number of Parking Spots for tier 3", value=5, min_value=5, max_value=25, step=1),
    "N_tier3_price": UserSettableParameter("slider", "strat 2: Price per hour for tier 3", value=0.1, min_value=0.1, max_value=10.0, step=0.1),
    "Max_time": UserSettableParameter("slider", "strat 3: Maximum parking time", value=1, min_value=1, max_value=24, step=1),
    "Scalling": UserSettableParameter("slider", "strat 4: Scalling of the price", value=0.0, min_value=0.0, max_value=5.0, step=0.1)
}

server = ModularServer(ParkingModel,
                       [grid],
                       "Money Model",
                       model_params)
server.launch()
