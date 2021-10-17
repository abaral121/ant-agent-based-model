from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from .model import Diffusion
from .agent import Environment, Home, Food, Ant
import math


def log_norm(value, lower, upper):
    value = min(value, upper)
    value = max(value, lower)
    lower_log = math.log(lower)
    upper_log = math.log(upper)
    value_log = math.log(value)

    return (value_log - lower_log) / (upper_log - lower_log)


def diffusion_portrayal(agent):
    if agent is None:
        return
    # create portrayal dict
    portrayal = {}

    # render this way if agent is Enviornment
    if type(agent) is Environment:
        portrayal["Shape"] = "rect"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        red = int(
            log_norm(agent.amount, agent.model.lowerbound, agent.model.initdrop) * 255
        )
        portrayal["Color"] = "#FF%02x%02x" % (255 - red, 255 - red)

    # render this way if agent is Home
    elif type(agent) is Home:
        portrayal["Shape"] = "circle"
        portrayal["r"] = 2
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 3
        portrayal["Color"] = "#964B00BB"
        portrayal["text"] = agent.amount
        portrayal["text_color"] = "white"

    # render this way if agent is Food
    elif type(agent) is Food:
        portrayal["Shape"] = "circle"
        portrayal["r"] = math.log(1 + agent.amount)
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 2
        portrayal["Color"] = "#00FF00BB"
        portrayal["text"] = agent.amount
        portrayal["text_color"] = "black"

    # render this way if agent is Ant
    elif type(agent) is Ant:
        portrayal["Shape"] = "circle"
        portrayal["r"] = 1
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 1
        portrayal["Color"] = "#000000"

    return portrayal


canvas_element = CanvasGrid(diffusion_portrayal, 50, 50, 500, 500)


model_params = {
    "height": 50,
    "width": 50,
    "evaporate": UserSettableParameter(
        "slider", "Evaporation rate", 0.07, 0.1, 0.30, 0.01
    ),
    "diffusion": UserSettableParameter(
        "slider", "Diffusion rate", 0.03, 0.0, 1.0, 0.10
    ),
    "initdrop": UserSettableParameter("slider", "Initial drop", 500, 100, 1000, 50),
    "prob_random": UserSettableParameter(
        "slider", "Random Probability", 0.1, 0.0, 1.0, 0.01
    ),
    "drop_rate": UserSettableParameter("slider", "Drop rate", 0.9, 0.10, 1.0, 0.10),
}


server = ModularServer(Diffusion, [canvas_element], "Chemical Diffusion", model_params)
