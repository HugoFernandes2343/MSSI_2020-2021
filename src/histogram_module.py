from mesa.visualization.ModularVisualization import VisualizationElement
import numpy as np

class HistogramModule(VisualizationElement):
    package_includes = ["Chart.min.js"]
    local_includes = ["histogram_module.js"]

    def __init__(self, bins, canvas_height, canvas_width):
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.bins = bins
        new_element = "new HistogramModule({}, {}, {})"
        new_element = new_element.format(bins,
                                         canvas_width,
                                         canvas_height)
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        wallet_vals = [agent.wallet for agent in model.schedule.agents]
        hist = np.histogram(wallet_vals, bins=self.bins)[0]
        return [int(x) for x in hist]

