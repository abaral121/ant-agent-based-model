from mesa import Agent
import math


def get_distance(pos1, pos2):
    """
    gets distance euclidian between two points

    args:
        pos1: the position of first agent
        pos2: the position of second agent

    return: a single value of distance
    """
    x1, y1 = pos1
    x2, y2 = pos2
    dx = x1 - x2
    dy = y1 - y2

    return math.sqrt((dx ** 2 + dy ** 2))


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
        # self.random_move()
        # self.home_move()
        self.gradient_move()
        pass

    def home_move(self):
        neighbors = [
            n.get_pos()
            for n in self.model.grid.get_neighbors(self.pos, True)
            if type(n) is Environment
        ]
        min_dist = min([get_distance(self.home.pos, pos) for pos in neighbors])
        final_candidates = [
            pos for pos in neighbors if get_distance(self.home.pos, pos) == min_dist
        ]
        self.random.shuffle(final_candidates)
        self.model.grid.move_agent(self, final_candidates[0])

    def gradient_move(self):
        max = self.model.lowerbound
        neighbors = [
            n
            for n in self.model.grid.get_neighbors(self.pos, True)
            if type(n) is Environment
        ]
        where = (0, 0)
        for n in neighbors:
            if n.amount > max:
                max = n.amount
                where = n.get_pos()

        if max > self.model.lowerbound:
            self.model.grid.move_agent(self, where)
        else:
            self.random_move()
