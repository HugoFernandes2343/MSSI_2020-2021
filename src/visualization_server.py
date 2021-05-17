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
    "variableSlider": UserSettableParameter("slider", "Variable slider example", 0.5, 0, 1.0, 0.1),
    "variableNumber": UserSettableParameter("number", "Variable number example",1),
    "variableOption": UserSettableParameter("choice", 'Opçoes', value='Opcao A',
                                          choices=['Opcao A', 'Opcao A']),
    "variableCheckbox": UserSettableParameter('checkbox', 'Booleano', value=True)
}

server = ModularServer(ParkingModel,
                       [grid],
                       "Money Model",
                       model_params)
server.launch()
