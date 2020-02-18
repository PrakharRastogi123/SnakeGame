from random import randint
import tkinter as tk
import PIL
from PIL import Image, ImageTk
MOVE_INCREMENT = 20
MOVE_PER_SECONDS = 15
GAME_SPEED = 1000 // MOVE_PER_SECONDS

class Snake(tk.Canvas): # we are making our Snake class a Canvas!
# so whenever we set any properties or access any methods of the snake class
# we're gonna access them in the Canvas unless we override them in our own class
    def __init__(self):
        super().__init__(width=600, height=620,  # calling the super class (inside init) which is the canvas here, so any properties we are passing to this init method, we could pass to tk.canvas if we define them here
                         background="black",    # setting dimensions of canvas,its background, and we dont want highight border around our canvas ,so setting it 0
                       highlightthickness=0)  # by default highlightthickness value is one and its a white colour border around canvas
        #snake start positions(x,y)
        self.snake_positions = [(100, 100), (80, 100), (60,100)] # since each snake block is 20 pixels, that is why we are seperating x and y by >=20 pixels
        self.food_position = self.set_new_food_position()
        self.score = 0
        self.direction = "Right"
        self.bind_all("<Key>", self.on_key_press) # when a key is pressed we run this method
        self.load_assets()
        self.create_objects()

        self.after(GAME_SPEED, self.perform_actions)

    def load_assets(self):
        try:
            self.snake_body_image = Image.open("./assets/snake.png")
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)
            
            self.food_image = Image.open("./assets/food.png")
            self.food = ImageTk.PhotoImage(self.food_image)
        except IOError as error:
            print(error)
            root.destroy()  #  In case of error encountered in loading image, the root window is terminated
    def create_objects(self):
        self.create_text(100, 12, text=f"Score {self.score} (speed: {MOVE_PER_SECONDS} )",tag="score", fill="#fff", font=("Ink Free", 14)) # score widget positioning and style
        for x_position, y_position in self.snake_positions:
            self.create_image(x_position, y_position, image = self.snake_body, tag="snake") # create three instances of snake.png at given snake positions each tagged as snake
        self.create_image(*self.food_position, image = self.food, tag="food") #self.food_pos[0], self.food_pos[1] == *self.food_pos, (destrucrures the tuple )
        self.create_rectangle(7, 27, 593, 613, outline="#525d69") #rectangle(topleft,bottomright,color of rect boundary(here its light grey))

    def move_snake(self):
        head_x_position, head_y_position = self.snake_positions[0] # the first element of our snake body tuple list is snake's head initial position
        if self.direction == "Left":
            new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)
        if self.direction == "Right":
            new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
        if self.direction == "Down":
            new_head_position = (head_x_position, head_y_position + MOVE_INCREMENT)
        if self.direction == "Up":
            new_head_position = (head_x_position, head_y_position -  MOVE_INCREMENT)

        self.snake_positions = [new_head_position]+self.snake_positions[:-1] # copy the head and cut off the tail block(moving snake)

        # here we find all elements withtag "snake" and all snake_positons, and intervines their each element into a tuple using zip function
        # then we get each element of tagged elements and positon and we can change the position using self.coords
        # self.coord will move the segment(tagged"snake") to the position(self.snake_positions)
        for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
            self.coords(segment, position)

    def perform_actions(self):
        if self.check_collisions():
            self.end_game()
            return
        self.check_food_collision()
        self.move_snake()
        self.after(GAME_SPEED, self.perform_actions) # it calls self.perform_action again after 75 milliseconds(GAME_SPEED)

    def check_collisions(self):
        head_x_position, head_y_position = self.snake_positions[0] # getting current value of snake's head position

        return(
            head_x_position in (0, 600)
            or head_y_position in (20, 620) # in y we check if its 20(not zero b/c we have label widget there) or 620
            or (head_x_position, head_y_position) in self.snake_positions[1:] # if head is equal to positon of any of the boy elements
        )
    
    def on_key_press(self, e):
        new_direction = e.keysym # it gives the symbol of the key associated with the event e(the information tkinter gives as a argument when a key pressed)
        all_directions = ("Up", "Down", "Left", "Right")
        opposite = ({"Up","Down"},{"Left","Right"}) # used to avoid the case when opposite direction key is pressed 
        if  (new_direction in all_directions 
            and {new_direction,self.direction} not in opposite):
            self.direction = new_direction
    
    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1]) # adding at the alst of snake

            if self.score % 5 ==0:
                global MOVE_PER_SECONDS
                MOVE_PER_SECONDS += 1

            self.create_image(
                *self.snake_positions[-1], image=self.snake_body, tag="snake"  # add snake image at the last of snake
            )
            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag("food"), self.food_position)
            # udating text of score
            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score: {self.score} (speed: {MOVE_PER_SECONDS} )", tag="score")

    def set_new_food_position(self):
        while True:                     # infinte loop
            x_position = randint(1, 29) * MOVE_INCREMENT # will be any number from 20 to 580
            y_position = randint(3, 30) * MOVE_INCREMENT # will be any number from 
            # 60(20(label, which we set to border)+20(size of food, as then will cause coolision with wall)+20(food placement size)) to 600
            food_position = (x_position, y_position)
            if food_position not in self.snake_positions:
                return food_position

    def end_game(self):
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width()/2, # to center i.e /2
            self.winfo_height()/2,
            text=f"Game Over: You Scored {self.score}",
            fill="#fff",
            font=("Ink Free", 24)
        )

root = tk.Tk()  # create main application window
root.title("Snake")
root.resizable(False, False)  # X and Y axis of root window is now non resizable
board = Snake()               # getting instance of Snake Class in board variable
board.pack()
root.mainloop()  # starts our main application window
