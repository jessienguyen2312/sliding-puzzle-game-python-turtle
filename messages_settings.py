'''
    Subclass Messages of the puzzle sliding game
    This subclass is for the purpose of displaying temporary messages
        on screen
    Citation: The framework of creating this subclass comes from:
        Website: Stackoverflow
        URL: https://stackoverflow.com/a/50912869
        Title: "Using python classes (OOP) to create FUNCTIONAL turtle objects?"
        Date of retrieval: 12/4/2022
'''
# import modules
import turtle
# import Turtle
from turtle import Turtle


class Messages(Turtle):
    def __init__(self, shape, speed, position, time):
        super().__init__(shape=shape, visible=False)
        # set assets of the Messages subclass
        self.shape(shape)  # assign shape
        self.speed(speed)  # assign speed
        self.penup()  # default - penup
        self.goto(position)  # assign position of message
        self.showturtle()  # restore visibility of message
        turtle.ontimer(self.hideturtle, t=time)  # assign timer
