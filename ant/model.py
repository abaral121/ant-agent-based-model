from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from .agent import Environment, Home, Food, Ant


class Diffusion(Model):
    def __init__(
        self,
        height=50,
        width=50,
        evaporate=0.07,
        diffusion=0.3,
        initdrop=500,
        lowerbound=0.01,
    ):

        super().__init__()

        self.evaporate = evaporate
        self.diffusion = diffusion
        self.initdrop = initdrop
        self.lowerbound = lowerbound

        # create empty schedule
        self.schedule = SimultaneousActivation(self)

        # define grid
        self.grid = MultiGrid(height, width, torus=True)

        # iter through grid, create and place envionrment agent in each spot
        for (_, x, y) in self.grid.coord_iter():
            # create agent
            cell = Environment((x, y), self)

            self.grid.place_agent(cell, (x, y))
            self.schedule.add(cell)

        # location of home
        homeloc = (25, 25)

        # create home agent, place in grid, add to schedule
        # the reason why we do self.home is so that the home coords are accessable to other classes?
        self.home = Home(self.next_id, homeloc, self)
        self.grid.place_agent(self.home, homeloc)
        self.schedule.add(self.home)

        # location of food
        food_locs = ((22, 11), (35, 8), (18, 33))

        # create food agent, place in grid, add to schedule, add food
        for loc in food_locs:
            food = Food(self.next_id(), self)
            self.grid.place_agent(food, loc)
            self.schedule.add(food)
            food.add(100)

        # create ant agent, place in grid, add to schedule
        for i in range(4):
            ant = Ant(self.next_id(), self.home, self)
            self.grid.place_agent(ant, self.home.pos)
            self.schedule.add(ant)

        self.running = True

    def step(self):
        self.schedule.step()
