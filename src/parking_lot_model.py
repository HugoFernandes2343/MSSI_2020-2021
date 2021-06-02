from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import random

roads =[]
spawn =[]

class CarAgent(Agent):
    """ An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1
        self.flag = 0
        self.dir = 0
        '''Money that the car has to spend on the parking lot'''
        self.wallet = random.randint(5,50)
        '''Time, in hours that will be seconds for the simmulation, that the car wants to spend on the park'''
        self.time = random.randint(1,24)
        '''State of the car (moving,queuing,parked)'''
        self.state = None
        '''Does the car want to park'''
        self.wantsToPark = False

    def moveUp(self):
        x=self.pos[0]
        y=self.pos[1]
        if((x,y+1) in roads):
            self.model.grid.move_agent(self, (x,y+1))
        else:
            self.changeDir()

    def moveDown(self):
        x=self.pos[0]
        y=self.pos[1]
        if((x,y-1) in roads):
            self.model.grid.move_agent(self, (x,y-1))
        else:
            self.changeDir()
    
    def moveRight(self):
        x=self.pos[0]
        y=self.pos[1]
        if((x+1,y) in roads):
            self.model.grid.move_agent(self, (x+1,y))
        else:
            self.changeDir()

    def moveLeft(self):
        x=self.pos[0]
        y=self.pos[1]
        if((x-1,y) in roads):
            self.model.grid.move_agent(self, (x-1,y))
        else:
            self.changeDir()

    def changeDir(self):
        x=self.pos[0]
        y=self.pos[1]
        direction = self.dir
        if(direction == 3 or direction == 2):
            if((x,y-1) in roads):
                self.dir = 1
            elif((x,y+1) in roads):
                self.dir = 0
        elif(direction == 1 or direction == 0):
            if((x-1,y) in roads):
                self.dir = 2
            elif((x+1,y) in roads):
                self.dir = 3


    # todo change move to be only moving to the left
    def move(self):
        #case change dir on upper bifurcation

        if(self.pos[0]==1 and self.pos[1]==14):
            if(self.dir==1):
                self.dir=3
            if(self.dir==2):
                self.dir=0

        if(self.pos[0]==18 and self.pos[1]==14):
            if(self.wantsToPark):
                self.dir=1
            elif(self.dir==1):
                self.dir=2
            elif(self.dir==3):
                self.dir=0
                

        #check if he wants to park

        if(self.pos[0]==12 and self.pos[1]==1):
            if(self.wantsToPark):
                self.dir=0

        #check if he is at the entrance
        if(self.pos[0]==12 and self.pos[1]==3):
            #como é que verificamos se há lugares XD

        if(self.dir == 0):
            self.moveUp()
        elif(self.dir == 1):
            self.moveDown()
        elif(self.dir == 2):
            self.moveLeft()
        elif(self.dir == 3):
            self.moveRight()       


        #new_position = self.pos[0] + 1, self.pos[1]

    def step(self):

        n = random.randint(0,200)
        if n==1:
            self.wantsToPark = True
        self.move()


# todo remove wealth only leave wall flag
class Tile(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.flag = 1


class ParkingModel(Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height,N_cars, N_spots,Price_hour, Strategy,N_tier1_spots,N_tier1_price,N_tier2_spots,N_tier2_price,N_tier3_spots,N_tier3_price,Max_time,Scalling):
        self.num_agents = N_cars
        self.aux = N_cars
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        '''Total spots of the parking lot'''
        self.spots = N_spots
        '''Price per hour'''
        self.price = Price_hour
        '''Id of the strategy 1 - Default; 2 - Premium Spots; 3 - Max Time; 4 - Scalling; 5 - Reservation'''
        self.strategy = Strategy
        if(self.strategy == 2):
            self.tier_1_spots = N_tier1_spots
            self.tier_2_spots = N_tier2_spots
            self.tier_3_spots = N_tier3_spots
            self.tier_1_price = N_tier1_price
            self.tier_2_price = N_tier2_price
            self.tier_3_price = N_tier3_price
        if(self.strategy == 3):
             self.max_time = Max_time
        if(self.strategy == 4):
            self.scalling = Scalling

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
            if(i>13):
                spawn.append((18,i))

            i = i + 1
        i = 18
        while i > 1 :
            self.num_agents = self.num_agents + 1
            a = Tile(self.num_agents, self)
            self.grid.place_agent(a,(i,18))
            roads.append((i,18))
            spawn.append((i,18))
            i = i - 1
        i = 18
        while i > 1 :
            self.num_agents = self.num_agents + 1
            a = Tile(self.num_agents, self)
            self.grid.place_agent(a,(1,i))
            roads.append((1,i))
            if(i>13):
                spawn.append((1,i))
            i = i - 1
        i = 2
        while i <= 17 :
            self.num_agents = self.num_agents + 1
            a = Tile(self.num_agents, self)
            self.grid.place_agent(a,(i,14))
            roads.append((i,14))
            spawn.append((i,14))
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
            i = i + 1

        i = 4
        while i <= 12 :
            self.num_agents = self.num_agents + 1
            a = Tile(self.num_agents, self)
            self.grid.place_agent(a,(15,i))
            i = i + 1

        i=4
        while i <= 14 :
            self.num_agents = self.num_agents + 1
            a = Tile(self.num_agents,self)
            self.grid.place_agent(a,(i,12))
            i = i + 1

        self.num_agents = self.num_agents + 1
        a = Tile(self.num_agents, self)
        self.grid.place_agent(a,(5,4))

        self.num_agents = self.num_agents + 1
        a = Tile(self.num_agents, self)
        self.grid.place_agent(a,(6,4))

        self.num_agents = self.num_agents + 1
        a = Tile(self.num_agents, self)
        self.grid.place_agent(a,(14,4))

        self.num_agents = self.num_agents + 1
        a = Tile(self.num_agents, self)
        self.grid.place_agent(a,(13,4))

        i = 6
        while i < 9 :
            self.num_agents = self.num_agents + 1
            a = Tile(self.num_agents,self)
            self.grid.place_agent(a,(i,5))
            i = i + 1

        i = 13
        while i > 10 :
            self.num_agents = self.num_agents + 1
            a = Tile(self.num_agents,self)
            self.grid.place_agent(a,(i,5))
            i = i - 1

        i = 8
        while i < 12 :
            self.num_agents = self.num_agents + 1
            a = Tile(self.num_agents,self)
            self.grid.place_agent(a,(i,4))
            i = i + 1

        self.num_agents = self.aux
        for i in range(self.num_agents):
            a = CarAgent(i, self)
            # TODO define the limits of this variables
            a.wallet = round(random.uniform(0.0,100.0),2)
            a.time = random.randint(1,24)
            a.state = "moving"
            self.schedule.add(a)
            done = 0
            while not done:
                # Add the agent to a random grid cell
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                if (x,y) in spawn:
                    done = 1
                    self.grid.place_agent(a, (x, y))




    # self.datacollector = DataCollector(
        #  model_reporters={"Gini": compute_gini},

    #            agent_reporters={"Wealth": "wealth"})

    def step(self):
        # self.datacollector.collect(self)
        self.schedule.step()
