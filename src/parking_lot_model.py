from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

class MoneyAgent(Agent):
    """ An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1
        self.flag=0
#todo change move to be only moving to the left
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = self.random.choice(cellmates)
            #other.wealth += 1
            self.wealth -= 1

    def step(self):
        self.move()
        if self.wealth > 0:
            self.give_money()

#todo remove wealth only leave wall flag
class Tile(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.flag = 1



class MoneyModel(Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
#todo try to see if this is taking too long
        for num in range(0,self.grid.width * self.grid.height):
            for i in range(0, self.grid.width):
                for j in range(0, self.grid.height):
                    a = Tile(num, self)
                    self.grid.place_agent(a, (i, j))


        # Create agents
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        #self.datacollector = DataCollector(
          #  model_reporters={"Gini": compute_gini},
#            agent_reporters={"Wealth": "wealth"})

    def step(self):
        #self.datacollector.collect(self)
        self.schedule.step()
