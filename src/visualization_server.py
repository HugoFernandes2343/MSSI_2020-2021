from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from parking_lot_model import MoneyModel
from mesa.visualization.modules import ChartModule
from histogram_module import HistogramModule

# metodo de representacao das bolinhas vermelhas TODO adaptar para carros

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5}
##todo change this to only have red balls and black squares
    if agent.flag == 1:
        portrayal["Color"] = "black"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    else:
        if agent.wealth >= 0:
            portrayal["Color"] = "red"
            portrayal["Layer"] = 0
        else:
            portrayal["Color"] = "grey"
            portrayal["Layer"] = 1
            portrayal["r"] = 0.2
    return portrayal


grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

#chart = ChartModule([{"Label": "Gini",
#                      "Color": "Black"}],
 #                   data_collector_name='datacollector')

#histogram = HistogramModule(list(range(10)), 200, 500)
server = ModularServer(MoneyModel,
                       [grid],
                       "Money Model",
                       {"N":100, "width":10, "height":10})
server.launch()
