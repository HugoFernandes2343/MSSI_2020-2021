from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from parking_lot_model import ParkingModel
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
server = ModularServer(ParkingModel,
                       [grid],
                       "Money Model",
                       {"N":10, "width":20, "height":20})
server.launch()
