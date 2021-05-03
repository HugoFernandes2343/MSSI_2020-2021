from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


class MoneyAgent(Agent):
    """ An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1
        self.flag = 0

    # todo change move to be only moving to the left
    def move(self):
        '''possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)'''
        new_position = self.pos[0] + 1, self.pos[1]
        self.model.grid.move_agent(self, new_position)

    def step(self):
        self.move()


# todo remove wealth only leave wall flag
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
        roads =[]
        
        #Creating the roads
        i = 1
        while i <= 17:
            self.num_agents = self.num_agents + 1
            a = Tile(self.num_agents, self)
            self.grid.place_agent(a, (i, 1))
            roads.append((i,1))
            i = i + 1
        i = 1
        while i <= 17:
            self.num_agents = self.num_agents + 1
            a = Tile(self.num_agents, self)
            self.grid.place_agent(a,(18,i))
            roads.append((18,i))
            i = i + 1
        i = 18
        while i > 1 :
            self.num_agents = self.num_agents + 1
            a = Tile(self.num_agents, self)
            self.grid.place_agent(a,(i,18))
            roads.append((i,18))
            i = i - 1
        i = 18
        while i > 1 :
            self.num_agents = self.num_agents + 1
            a = Tile(self.num_agents, self)
            self.grid.place_agent(a,(1,i))
            roads.append((1,i))
            i = i - 1
        i = 2
        while i <= 17 :
            self.num_agents = self.num_agents + 1
            a = Tile(self.num_agents, self)
            self.grid.place_agent(a,(i,14))
            roads.append((i,14))
            i = i + 1

        #Creating the exit
        self.num_agents = self.num_agents + 1
        a = Tile(self.num_agents, self)
        self.grid.place_agent(a,(7,2))
        roads.append((7,2))

        self.num_agents = self.num_agents + 1
        a = Tile(self.num_agents, self)
        self.grid.place_agent(a,(7,3))
        roads.append((7,3))

        #Creating the entrance todo add a function to the movement that makes cars that enter go to a parking tile
        self.num_agents = self.num_agents + 1
        a = Tile(self.num_agents, self)
        self.grid.place_agent(a,(12,2))
        roads.append((12,2))

        self.num_agents = self.num_agents + 1
        a = Tile(self.num_agents, self)
        self.grid.place_agent(a,(12,3))
        roads.append((12,3))

        ## The three blocks that will hold the cars
        # todo make it so the number of blocks (1-3) depends on the amount of parking tiers
        ##
        self.num_agents = self.num_agents + 1
        a = Tile(self.num_agents, self)
        self.grid.place_agent(a,(7,8))
        roads.append((7,8))

        self.num_agents = self.num_agents + 1
        a = Tile(self.num_agents, self)
        self.grid.place_agent(a,(9,8))
        roads.append((9,8))

        self.num_agents = self.num_agents + 1
        a = Tile(self.num_agents, self)
        self.grid.place_agent(a,(11,8))
        roads.append((11,8))

        #Creating the parking lot outline
        i = 4
        while i <= 12 :
            self.num_agents = self.num_agents + 1
            a = Tile(self.num_agents, self)
            self.grid.place_agent(a,(4,i))
            roads.append((4,i))
            i = i + 1

        i = 4
        while i <= 12 :
            self.num_agents = self.num_agents + 1
            a = Tile(self.num_agents, self)
            self.grid.place_agent(a,(15,i))
            roads.append((15,i))
            i = i + 1

        i=4
        while i <= 14 :
            self.num_agents = self.num_agents + 1
            a = Tile(self.num_agents,self)
            self.grid.place_agent(a,(i,12))
            roads.append((i,12))
            i = i + 1

        self.num_agents = self.num_agents + 1
        a = Tile(self.num_agents, self)
        self.grid.place_agent(a,(5,4))
        roads.append((5,4))

        self.num_agents = self.num_agents + 1
        a = Tile(self.num_agents, self)
        self.grid.place_agent(a,(6,4))
        roads.append((6,4))

        self.num_agents = self.num_agents + 1
        a = Tile(self.num_agents, self)
        self.grid.place_agent(a,(14,4))
        roads.append((14,4))

        self.num_agents = self.num_agents + 1
        a = Tile(self.num_agents, self)
        self.grid.place_agent(a,(13,4))
        roads.append((13,4))

        i = 6
        while i < 9 :
            self.num_agents = self.num_agents + 1
            a = Tile(self.num_agents,self)
            self.grid.place_agent(a,(i,5))
            roads.append((i,5))
            i = i + 1

        i = 13
        while i > 10 :
            self.num_agents = self.num_agents + 1
            a = Tile(self.num_agents,self)
            self.grid.place_agent(a,(i,5))
            roads.append((i,5))
            i = i - 1

        i = 8
        while i < 12 :
            self.num_agents = self.num_agents + 1
            a = Tile(self.num_agents,self)
            self.grid.place_agent(a,(i,4))
            roads.append((i,4))
            i = i + 1

        # TODO turn this into proper car agents that will only be able to walk on black spots
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)
            done = 0
            while not done:
                # Add the agent to a random grid cell
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                if (x,y) in roads:
                    done = 1
                    self.grid.place_agent(a, (x, y))




    # self.datacollector = DataCollector(
        #  model_reporters={"Gini": compute_gini},

    #            agent_reporters={"Wealth": "wealth"})

    def step(self):
        # self.datacollector.collect(self)
        self.schedule.step()
