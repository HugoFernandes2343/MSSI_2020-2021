from parking_lot_model import MoneyModel, compute_gini
import matplotlib.pyplot as plt
import numpy as np
from mesa.batchrunner import BatchRunner

# model = MoneyModel(50, 10, 10)
# for i in range(100):
#     model.step()
#
# agent_counts = np.zeros((model.grid.width, model.grid.height))
# for cell in model.grid.coord_iter():
#    cell_content, x, y = cell
#    agent_count = len(cell_content)
#    agent_counts[x][y] = agent_count
# plt.imshow(agent_counts, interpolation='nearest')
# plt.colorbar()
#
# plt.show()
#
# gini = model.datacollector.get_model_vars_dataframe()
# gini.plot()
# plt.show()
#
# agent_wealth = model.datacollector.get_agent_vars_dataframe()
# print(agent_wealth.head())
#
# end_wealth = agent_wealth.xs(99, level="Step")["Wealth"]
# end_wealth.hist(bins=range(agent_wealth.Wealth.max()+1))
# plt.show()
#
# one_agent_wealth = agent_wealth.xs(14, level="AgentID")
# one_agent_wealth.Wealth.plot()
# plt.show()

fixed_params = {"width": 10,
                "height": 10}
variable_params = {"N": range(10, 500, 10)}

batch_run = BatchRunner(MoneyModel,
                        variable_params,
                        fixed_params,
                        iterations=5,
                        max_steps=100,
                        model_reporters={"Gini": compute_gini})
batch_run.run_all()