import turtle
import tkinter
import tkinter.colorchooser
import tkinter.filedialog
import xml.dom.minidom

# The foloowing classes define the different commands that
# are supported by the drawing application we are creating.

class GoToCommand:
    def __init__(self, x, y, width=1, color='black'):
        self.x = x
        self.y = y
        self.color = color
        self.width = width

    # The draw method for each command draws the command
    # using the given turtle 

    def draw(self, turtle):
        turtle.width(self.width)
        turtle.pencolor(self.color)
        turtle.goto(self.x, self.y)

    # The __str__ is a special method that is called
    # when a command is converted to a string. The string 
    # version of the command is how it appears in the graphics
    # file format.

    def __str__(self):
        return ’<Command x=" ’ + str(self.x) + ’" y=" ’ + str(self.y) + \
            ’ " width=" ’ + str(self.width) \
            + ’" color =" ’ + self.color + ’ " >GoTo </Command> ’

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

# This is the PyList container obj. Its meant to hold a...
class PyList:
    def __init__(self):
        self.gcList = []

    # The append method is used to add commands to the sequence.
    def append(self, item):
        self.gcList = self.gcList + [item]

    # This method is used by the undo function. It slices the sequence
    # to remove the last item.

    def removeLast(self):
        self.gcList = self.gcList[:-1]

    # This special method is called whenthe over the sequence.
    # Each time yield is called another element of the sequence is returned
    # to the iterator (i.e. the for loop that called this.)

    def __iter__(self):
        for c in self.gcList:
            yield c

    # This is called when the len function is called on the sequence.
    
    def __len__(self):
        return len(self.gcList)

# This class defines the drawing application. The following line says that
# the DrawingApplication class inherits from the Frame class. This means
# that a DrawingApplication is like a Frame Object except for the code
# written here which redefines/extends the behaviour of a Frame.

class DrawingApplication(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.buildWindow()
        self.graphicCommand = PyList()

    # This method is called to create all the widgets, place them in the GUI
    # and define the event handlers for the app.

    def buildWindow(self):
        # The master is the root window. The title is set as below:
        self.master.title('Draw')

        # Here's how to create a menu bar. The tearoff=0 means that 
        # can;t be separated from the windowwhich is a feature of tkinter.
        bar = tkinter.Menu(self.master)
        fileMenu = tkinter.Menu(bar, tearoff=0)

    # This code is called by the "New" menu item below when it is selected.
    # The same applies for loadFile, addToFile, and saveFile below. THe
    # "Exit" menu item below calls quit on the "master" or root window.

    def newWindow():
        # This sets up the turtle to be ready for a new picture to be
        # drawn. It also sets the sequence back to empty. It is necessary
        # for the graphicsCommand sequence to be in the object (i.e. 
        # self.graphicsCommands) because otherwise the statement:
        # graphicsCommand = PyList()
        # would make this variable a local variable in the newWindow
        # method. If it were local, it would not be set anymore once the 
        # newWindow method returned.
        theTurtle.clear()
        theTurtle.penup()
        theTurtle,goto(0,0)
        theTurtle.pendown()
        screen.update()
        screen.listen()
        self.graphicCommand = PyList()

    fileMenu.add_command(label="New", command=newWindow)

    # The parse function adds the contents of an XML file to the sequence.

    def parse(filename):
        xmldoc = xml.dom.minidom.parse(filename)

        graphicsCommandsElement = xmldoc.getElementsByTagName("GraphicsCommands")[0]

        for commandElement in graphicsCommands:
            print(type(commandElement))
            command = commandElement.firstChild.data.strip()
            attr = commandElement.attributes
            if command == "GoTo":
                x = float(attr["x"].value)
                y = float(attr["y"].value)
                width = float(attr["width"].value)
                color = float(attr["color"].value)
                cmd = GoToCommand(x, y, width, color)
            
            elif command == "Circle":
                radius = float(attr["radius"].value)
                width = float(attr["width"].value)
                color = float(attr["color"].value)
                cmd = CircleCommand(radius, width, color)

            elif command == "BeginFill":
                width = float(attr["width"].value)
                cmd = BeginFillCommand(color)

            elif command == "EndFill":
                cmd = EndFillCommand()

            elif command == "PenUp":
                cmd = PenUpCommand()

            elif command == "PenDown":
                cmd = PenDownCommand()

            else:
                raise RuntimeError("Unknown_Command: _" + command)

            self.graphicsCommand.append(cmd)

    def loadFile():
        filename = tkinter.filedialog.askopenfilename(title="Select a Graphics File")

        newWindow()

        # This re-initializes the sequence for the new picture.
        self.graphicsCommands = PyList()

        # Calling Parse will read the graphics commands from the file.
        parse(filename)

        for cmd in self.graphicsCommands:
            cmd.draw(theTurtle)

        # This line is necessary to update the window after the picture is drawn.
        screen.update()

    fileMenu.add_command(label="Load...", command=loadFile)

    def addToFile():
        filename = tkinter.filedialog.askopenfilename(title="Select a Graphics File")

        theTurtle.penup()
        theTurtle.goto(0,0)
        theTurtle.pendown()
        theTurtle.pencolor("#000000")
        theTurtle.fillcolor("#000000")
        cmd = PenUpCommand()
        self.graphicsCommands.append(cmd)
        cmd = GoToCommand(0,0,1,"#000000")
        self.graphicsCommands.append(cmd)
        cmd = PenDownCommand()
        self.graphicsCommands.append(cmd)
        screen.update()
        parse(filename)

        for cmd in self.graphicsCommands:
            cmd.draw(theTurtle)

            screen.update()
    fileMenu.add_command(label="Load Into...", command=addToFile)

    def write(filename):
        file = open(filename,"w")
        file.write(’<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n’)
        file.write(’<GraphicsCommands>\n’)
        for cmd in self.graphicsCommands:
            file.write(’  ’ + str(cmd) + "\n")

        file.write(’</GraphicsCommands>\n’)

        file.close()

    def saveFIle():
        filename = tkinter.filedialog.asksaveasfilename(title="Save Picture As...")
        write(filename)

    fileMenu.add_command(label="Save As...",command=saveFile)
    
    fileMenu.add_command(label="Exit",command=self.master.quit)

    bar.add_cascade(label="File",menu=fileMenu)

    # This tells the root window to display the newly created menu bar.
    self.master.config(menu=bar)

    # Here several widgets are created. The canvas is the drawing area on
    # the left side of the window.
    canvas = tkinter.Canvas(self,width=600,height=600)
    canvas.pack(side=tkinter.LEFT)

    # By creating a RawTurtle, we can have the turtle draw on this canvas.
    # Otherwise, a RawTurtle and a Turtle are exactly the same.
    theTurtle = turtle.RawTurtle(canvas)

    # This makes the shape of the turtle a circle.
    theTurtle.shape("circle")
    screen = theTurtle.getscreen()

    # This causes the application to not update the screen unless
    # screen.update() is called. This is necessary for the ondrag event
    # handler below. Without it, the program bombs after dragging the
    # turtle around for a while.
    screen.tracer(0)

    # This is the area on the right side of the window where all the
    # buttons, labels, and entry boxes are located. The pad creates some empty
    # space around the side. The side puts the sideBar on the right side of the
    # this frame. The fill tells it to fill in all space available on the right
    # side.
    sideBar = tkinter.Frame(self,padx=5,pady=5)
    sideBar.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)

    # This is a label widget. Packing it puts it at the top of the sidebar.
    pointLabel = tkinter.Label(sideBar,text="Width")
    pointLabel.pack()

    # This entry widget allows the user to pick a width for their lines.
    # With the widthSize variable below you can write widthSize.get() to get
    # the contents of the entry widget and widthSize.set(val) to set the value
    # of the entry widget to val. Initially the widthSize is set to 1. str(1) is
    # needed because the entry widget must be given a string.
    widthSize = tkinter.StringVar()
    widthEntry = tkinter.Entry(sideBar,textvariable=widthSize)

    widthEntry.pack()
    widthSize.set(str(1))

    radiusLabel = tkinterLabel(sideBar, text="Radius")
    radiusLabel.pack()

    def circleHandler():
        # When drawing, a command is created and then the command is drawn by calling
        # the draw method. Adding the command to the graphicsCommands sequence means the
        # applcation will remember the picture
        cmd = CircleCommand(float(radiusSize.get()), float(widthSize.get()), penColor.get())
        cmd.draw(theTurtle)
        self.graphicsCommands.append(cmd)

        # These two lines are needed to update the screen and to put the focus back
        # in the drawing canvas. This is necessary because when pressing "u" to undo,
        # the screen must have focus to receive the key press.

        screen.update()
        screen.listen()

    # This created the button widget in the sideBar. THe fill=tkinter.BOTH causes the button
    # to expand to fill the entire width if the sidebar.
    circleButton = tkinter.Button(sideBar, text="Draw Circle", command=circleHandler)
    circleButton.pack(fill=tkinter.BOTH)

    # The color mode 255 below allows colors to be specified in RGB form (i.e. Red/
    # Green/Blue). The mode allows the Red value to be set by a two digit hexadecimal
    # number ranging from 00-FF. The same applies for Blue and Green values. The
    # color choosers below return a string representing the selected color and a slice
    # is taken to extract the #RRGGBB hexadecimal string that the color choosers return.

    screen.colormode(255)
    penLabel = tkinter.label(sideBar, text="Pen Color")
    penLabel.pack()
    # The default color is set to black.
    penColor.set("#000000")

    def getPenColor():
        color = tkinter.colorchooser.askcolor()

        if color != None:
            penColor.set(str(color)[-9: -2])

    penColorButton = tkinter.Button(sideBar, text="Pick Pen Color", command=getPenColor)
    penColorButton.pack(fill=tkinter.BOTH)

    def beginFillHandler():
        cmd = BeginFillCommand(fillColor.get())
        cmd.draw(theTurtle)
        self.graphicCommand.append(cmd)

    beginFillButton = tkinter.Button(sideBar, text="Begin Fill", command=beginFillHandler)
    beginFillButton.pack(tkinter.BOTH)

    def endFIllHandler():
        cmd = EndFillCommand(fillColor.get())
        cmd.draw(theTurtle)
        self.graphicCommand.append(cmd)

    endFillButton = tkinter.Button(sideBar, text="End Fill", command=endFillHandler)
    endFillButton.pack(tkinter.BOTH)

    penLabel = tkinter.Label(sideBar,text="Pen Is Down!")

    penLabel.pack()

    def penUpHandler():
        cmd = PenUpCommand()
        cmd.draw(theTurtle)
        penLabel.configure(text="Pen Is Up!")
        self.graphicsCommands.append(cmd)

    penUpButton = tkinter.Button(sideBar, tect="Pen Up", command=penUpHandler)
    penUpButton.pack(fill=tkinter.BOTH)

    def penDownHandler():
        cmd = PenDownCommand()
        cmd.draw(theTurtle)
        penLabel.configure(text="Pen Is Up!")
        self.graphicsCommands.append(cmd)

    penDownButton = tkinter.Button(sideBar, tect="Pen Up", command=penDownHandler)
    penDownButton.pack(fill=tkinter.BOTH)


    # Here is another event handler. This one handles mouse clicks on the screen
    def clickHandler(x,y):
        # When a mouse click occurs, get the widthSize entry value and set the width of the
        # pen to the widthSize value. The float(widthSize.get()) is needed because
        # the width is a float, but the entry widget stores it as a string.

        cmd = GoToCommand(x, y, float(widthSize.get()), penColor.get())
        cmd.draw(theTurtle)
        self.graphicsCommands.append(cmd)
        
        screen.update()
        screen.listen()

    # Here is how we tie the clickHandler to mouse clicks.
    screen.onclick(clickHandler)

    def dragHandler(x,y):
        
        cmd = GoToCommand(x, y, float(widthSize.get()), penColor.get())
        cmd.draw(theTurtle)
        self.graphicsCommands.append(cmd)
        
        screen.update()
        screen.listen()

    theTurtle.ondrag(dragHandler)

    # The undoHandler undoes the last command by removing it from the
    # sequence and then redrawing the entire picture.

    def undoHandler():
        if len(self.graphicsCommands) > 0:
            self.graphicsCommands.removeLast()
            theTurtle.clear()
            theTurtle.penup()
            theTurtle.goto(0,0)
            theTurtle.pendown()

            for cmd in self.graphicsCommands:
                cmd.draw(theTurtle)
            
            screen.update()

            screen.listen()

    screen.onkeypress(undoHandler, "u")
    screen.listen()
    
    # +-------------------------------------------------------------------------------+
    # | The main function in our GUI program is very simple. It creates the           |
    # | root window. Then it creates the DrawingApplication frame which creates       |
    # | all the widgets and has the logic for the event handlers. Calling mainloop    |
    # | on the frames makes it start listening for events. The mainloop function will | 
    # | return when the application is exited.                                        |
    # +-------------------------------------------------------------------------------+

def main():
    root = tkinter.Tk()
    drawingApp = DrawingApplication(root)

    drawingApp.mainloop()
    print("Program Execution Completed.")

if __name__ == "__main__":
    main()

# +-----+
# | END |
# +-----+
