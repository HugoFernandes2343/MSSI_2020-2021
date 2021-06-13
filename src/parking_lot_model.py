from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import random
import math

roads =[]
spawn =[]


class ParkingModel(Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height,N_cars, N_spots,Price_hour, Strategy,N_tier1_spots,N_tier1_price,N_tier2_spots,N_tier2_price,N_tier3_spots,N_tier3_price,Max_time,Scalling):
        self.num_agents = N_cars
        self.aux = 2 #N_cars
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        
        '''Parking makings'''
        self.makings = 0
        '''Total spots of the parking lot'''
        self.spots = N_spots
        self.available_spots = N_spots
        '''Price per hour'''
        self.price = Price_hour
        '''Id of the strategy 1 - Default; 2 - Premium Spots; 3 - Max Time; 4 - Scalling; 5 - Reservation'''
        self.strategy = Strategy
        #if(self.strategy == 2):
        self.tier_1_spots = N_tier1_spots
        self.tier_2_spots = N_tier2_spots
        self.tier_3_spots = N_tier3_spots
        self.tier_1_price = N_tier1_price
        self.tier_2_price = N_tier2_price
        self.tier_3_price = N_tier3_price
        #if(self.strategy == 3):
        self.max_time = Max_time
        #if(self.strategy == 4):
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

class CarAgent(Agent,ParkingModel):
    """ An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.model = model
        self.id = unique_id
        self.wealth = 1
        self.flag = 0
        self.dir = 0
        '''Flag that means the car does not have money to a lower tier'''
        self.no_money = 0
        '''Money that the car has to spend on the parking lot'''
        self.wallet = random.randint(5,130)
        '''Time, in hours that will be seconds for the simmulation, that the car is parked'''
        self.wait_time = 9999
        '''Time, in hours that will be seconds for the simmulation, that the car wants to spend on the park'''
        self.time = random.randint(2,24)
        self.time_elapsed = 0
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
            #If the park has the 1 strategy implemented
            if self.model.strategy == "1 - Default":
                if self.model.available_spots > 0:
                    price_for_total_time = self.model.price * self.time
                    percentage = (self.wealth/price_for_total_time)*100
    
                    if self.wallet > price_for_total_time:
                        #park and place him in the middle slot
                        self.model.grid.move_agent(self, (9,8))
                        #change dir to 4 and as such he stays put
                        self.dir = 4
                        self.model.makings += price_for_total_time
                    elif random.randrange(0, 100) < percentage:
                        new_time = self.wallet/self.model.price
                        self.wait_time = math.floor(new_time)
                        self.model.makings = self.wait_time * self.model.price
                        #park and place him in the middle slot
                        self.model.grid.move_agent(self, (9,8))
                        #change dir to 4 and as such he stays put
                        self.dir = 4
                    else:
                        self.dir = 1
                        self.wantsToPark = False

#TODO
#if not greater than the desired total time, create a function to decide if he parks or not
#this function sould be more likely to park the closer he can get to the desired time                        
                    
            #If the park has the 2 strategy implemented
            elif self.model.strategy == "2 - Premium Spots":

                #set the needed variables for the park consideration
                price_for_total_time_tier_1 = self.model.tier_1_price * self.time
                price_for_total_time_tier_2 = self.model.tier_2_price * self.time
                price_for_total_time_tier_3 = self.model.tier_3_price * self.time
                percentage_tier_1 = (self.wealth/price_for_total_time_tier_1)*100
                percentage_tier_2 = (self.wealth/price_for_total_time_tier_2)*100
                percentage_tier_3 = (self.wealth/price_for_total_time_tier_3)*100
                
                print("Eu sou o carro " + str(self.id) +" E tenho " + str(self.wallet) +" para gastar, o 1 custa me " + str(price_for_total_time_tier_1))
                print("Eu sou o carro " + str(self.id) +" E tenho " + str(self.wallet) +" para gastar, o 2 custa me " + str(price_for_total_time_tier_2))
                print("Eu sou o carro " + str(self.id) +" E tenho " + str(self.wallet) +" para gastar, o 3 custa me " + str(price_for_total_time_tier_3))
                
                if self.model.tier_1_spots > 0:
                    print("Eu sou o carro " + str(self.id) + " e quero entrar no 1")
                    if self.wallet > price_for_total_time_tier_1:
                        print("Eu sou o carro " + str(self.id) + " e vou entrar no 1")
                        #park and place him in the middle slot
                        self.model.grid.move_agent(self, (7,8))
                        #change dir to 4 and as such he stays put
                        self.dir = 4
                        #pays the park
                        self.model.makings += price_for_total_time_tier_1
                    else:
                        self.no_money += 1                
                if (self.model.tier_2_spots > 0):
                    print("Eu sou o carro " + str(self.id) + " e quero entrar no 2")
                    if self.wallet > price_for_total_time_tier_2:
                        print("Eu sou o carro " + str(self.id) + " e vou entrar no 2")
                        #park and place him in the middle slot
                        self.model.grid.move_agent(self, (9,8))
                        #change dir to 4 and as such he stays put
                        self.dir = 4
                        #pays the park
                        self.model.makings += price_for_total_time_tier_2
                    else:
                        self.no_money += 1
                if (self.model.tier_3_spots > 0):
                    print("Eu sou o carro " + str(self.id) + " e quero entrar no 3")
                    if self.wallet > price_for_total_time_tier_3:
                        print("Eu sou o carro " + str(self.id) + " e vou entrar no 3")
                        #park and place him in the middle slot
                        self.model.grid.move_agent(self, (11,8))
                        #change dir to 4 and as such he stays put
                        self.dir = 4
                        #pays the park
                        self.model.makings += price_for_total_time_tier_3
                    else:
                        self.no_money += 1
                if(self.no_money == 3):
                    if (random.randrange(0,100) < percentage_tier_1 and self.model.tier_1_spots > 0):
                        self.new_time = self.wallet/self.model.tier_1_price
                        self.wait_time = math.floor(self.new_time)
                        self.model.makings = self.wait_time * self.model.tier_1_price
                        self.model.grid.move_agent(self, (7,8))
                        self.dir = 4
                if(self.no_money == 2):            
                    if (random.randrange(0,100) < percentage_tier_2 and self.model.tier_2_spots > 0):
                        self.new_time = self.wallet/self.model.tier_2_price
                        self.wait_time = math.floor(self.new_time)
                        self.model.makings = self.wait_time * self.model.tier_2_price
                        self.model.grid.move_agent(self, (9,8)) 
                        self.dir = 4   
                if(self.no_money == 1):             
                    if (random.randrange(0,100) < percentage_tier_3 and self.model.tier_3_spots > 0):
                        self.new_time = self.wallet/self.model.tier_3_price
                        self.wait_time = math.floor(self.new_time)
                        self.model.makings = self.wait_time * self.model.tier_3_price
                        self.model.grid.move_agent(self, (11,8))
                        self.dir = 4


        if((self.pos[0]==9 and self.pos[1]==8) or (self.pos[0]==7 and self.pos[1]==8) or (self.pos[0]==11 and self.pos[1]==8)):
            if(self.wait_time == 9999):
                self.wait_time = (self.time*10) - 1
            if(self.wait_time == 1):
                self.wait_time = 9999
                self.model.grid.move_agent(self, (7,4))
                self.dir = 1
                self.wantsToPark = False
            elif(self.wait_time > 1):
                self.wait_time -= 1    

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


