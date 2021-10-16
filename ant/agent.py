from mesa import Agent


class Environment(Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)  # in this case pos was the unique id
        self.pos = pos
        self.amount = 0.0

    def step(self):
        # getting pheremons from agent
        all_p = self.amount
        neighbors = [
            n
            for n in self.model.grid.get_neighbors(self.pos, True)
            if type(n) is Environment
        ]

        # sum all neighbor p amounts and get avg
        for n in neighbors:
            all_p += n.amount
        ave_p = all_p / (len(neighbors) + 1)

        # calculates diff between agent and the avg neighbor p vals
        self._nextAmount = (1 - self.model.evaporate) * (
            self.amount + (self.model.diffusion * (ave_p - self.amount))
        )

        if self._nextAmount < self.model.lowerbound:
            self._nextAmount = 0

    def advance(self):
        self.amount = self._nextAmount

    def add(self, amount):
        self.amount += amount

    def get_pos(self):
        return self.pos


class Home(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
        self.amount = 0

    def add(self, amount):
        # incrememnts food at home by amount
        self.amount += amount


class Food(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.amount = 0

    def add(self, amount):
        self.amount += amount

    def any_food(self):
        return self.amount > 0

    def eat(self):
        if self.any_food():
            self.amount -= 1


class Ant(Agent):
    def __init__(self, unique_id, home, model):
        super().__init__(unique_id, model)
        self.pos = home.pos
        self.home = home

    def random_move(self):
        # search ant agent surrounding area
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        # select a choice
        next_move = self.random.choice(possible_steps)
        # move agent
        self.model.grid.move_agent(self, next_move)

    def step(self):
        self.random_move()
        pass
