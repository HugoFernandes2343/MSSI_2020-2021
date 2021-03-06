from parking_lot_model import ParkingModel, compute_gini
import matplotlib.pyplot as plt
import numpy as np
from mesa.batchrunner import BatchRunner

# model = ParkingModel(50, 10, 10)
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

batch_run = BatchRunner(ParkingModel,
                        variable_params,
                        fixed_params,
                        iterations=5,
                        max_steps=100,
                        model_reporters={"Gini": compute_gini})
batch_run.run_all()

run_data = batch_run.get_model_vars_dataframe()
run_data.head()
plt.scatter(run_data.N, run_data.Gini)
plt.show()

#Get the Agent DataCollection
data_collector_agents = batch_run.get_collector_agents()

print(data_collector_agents[(10,2)])

#Get the Model DataCollection.

data_collector_model = batch_run.get_collector_model()

print(data_collector_model[(10,1)])

