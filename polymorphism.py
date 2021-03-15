class GoToCommand:
    def __init__(self, x, y, width=1, color='black'):
        self.x = x
        self.y = y
        self.color = color
        self.width = width

    def draw(self, turtle):
        turtle.width(self.width)
        turtle.pencolor(self.color)
        turtle.goto(self.x, self.y)

class CircleCommand:
    def __init__(self, radius, width=1, color='black'):
        self.radius = radius
        self.width = width
        self.color = color

    def draw(self, turtle):
        turtle.width(self.width)
        turtle.pencolor(self.color)
        turtle.circle(self.radius)

class BeginFillCommand:
    def __init__(self, color):
        self.color = color

    def draw(self,turtle):
        turtle.fillcolor(self.color)
        turtle.begin_fill()

class EndFillCommand:
    def __init__(self):
        # pass is a statement placeholder and does nothing. We have nothing
        # to initialize in this class because all we want is the polymorphic
        # behavior of the draw method
        pass

    def draw(self, turtle):
        turtle.end_fill()

class PenUpCommand:
    def __init__(self):
        pass

    def draw(self, turtle):
        turtle.penup()

class PenDownCommand:
    def __init__(self):
        pass

    def draw(self, turtle):
        turtle.pendown()