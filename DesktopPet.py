import tkinter as tk
import time
import random

class pet():
    def __init__(self):
        self.window = tk.Tk()
        self.screenWidth = self.window.winfo_screenwidth()
        self.screenHeight = self.window.winfo_screenheight()

        # set images
        self.walking_right = [tk.PhotoImage(file='images\\walking_right_duck.gif', format='gif -index %i' % (i)) for i in range(10)]
        self.walking_left = [tk.PhotoImage(file='images\\walking_left_duck.gif', format='gif -index %i' % (i)) for i in range(10)]
        self.frame_index = 0
        self.img = self.walking_right[self.frame_index]

        # states / actions
        self.state = 0
        self.prevstate = 0
        self.lastAction = time.time()
        self.actionCooldown = 15

        self.groundHeight = self.screenHeight - int((self.screenHeight * 0.055))
        self.jumpHeight = self.screenHeight - int((self.screenHeight * 0.10))
        self.jumpHeightReached = False

        # timestamp to check whether to advance frame
        self.timestamp = time.time()

        # set focushighlight to black when the window does not have focus
        self.window.config(highlightbackground='black')

        # make window frameless
        self.window.overrideredirect(True)

        # make window draw over all others
        self.window.attributes('-topmost', True)

        # turn black into transparency
        self.window.wm_attributes('-transparentcolor', 'black')

        # create a label as a container for our image
        self.label = tk.Label(self.window, bd=0, bg='black')

        # create a window of size 128x128 pixels, at coordinates 0,0
        self.x = 0
        self.y = self.groundHeight
        self.window.geometry('64x64+{x}+{y}'.format(x=str(self.x), y=str(self.y)))
        

        # add the image to our label
        self.label.configure(image=self.img)

        # give window to geometry manager (so it will appear)
        self.label.pack()

        # force window on top
        def placeTop():
            self.window.lift()
            self.window.after(12, placeTop) # call every 10ms

        # run self.update() after 0ms when mainloop starts
        self.window.after(0, self.update)
        placeTop()
        self.window.mainloop()

    
    def changeState(self, newState):
        self.lastAction = time.time()
        self.prevstate = self.state
        self.state = newState
        

    def update(self):
        #random action
        if time.time() > self.lastAction + self.actionCooldown:
            randomAction = random.randint(1,12)

            if randomAction == 1: # Turn Right
                if not self.state == 0:
                    self.changeState(0)

            elif randomAction == 2: # Turn Left
                if not self.state == 1:
                    self.changeState(1)

            elif randomAction == 3: #Jump
                self.changeState(3)

        #Movement
        if self.state == 0: # Move Right
            self.x += 1 
            if self.x >= self.screenWidth: # Change direction at edge
                self.changeState(1)
            
        elif self.state == 1: # Move Left
            self.x -= 1
            if self.x <= 0: # Change direction at edge
                self.changeState(0)

        elif self.state == 3: # Jump
            if self.prevstate == 0:
                self.x += 1
            else:
                self.x -= 1

            if not self.jumpHeightReached:
                self.y -= 1
                if self.y <= self.jumpHeight:
                    self.jumpHeightReached = True
            else:
                self.y += 1
                if self.y >= self.groundHeight:
                    self.changeState(self.prevstate)
                    self.jumpHeightReached = False
                
        # Advance frame every 50ms
        if time.time() > self.timestamp + 0.05:
            self.timestamp = time.time()
            # check if direction changed and advance frame
            self.frame_index = (self.frame_index + 1) % 5

            if self.state == 0:
                self.img = self.walking_right[self.frame_index]
            elif self.state == 1:
                self.img = self.walking_left[self.frame_index]
            else:
                if self.prevstate == 0:
                    self.img = self.walking_right[self.frame_index]
                else:
                    self.img = self.walking_left[self.frame_index]

        # create the window
        self.window.geometry('64x64+{x}+{y}'.format(x=str(self.x), y=str(self.y)))
        # add the image to our label
        self.label.configure(image=self.img)
        # give window to geometry manager (so it will appear)
        self.label.pack()

        # call update after 10ms
        self.window.after(12, self.update)

pet()