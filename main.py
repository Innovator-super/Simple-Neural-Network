import tkinter as tk
import os
from random import uniform, randint
import math


file = os.path.dirname(os.path.abspath(__file__))


window = tk.Tk()
window.geometry("300x500")
window.title("flappy bird")


canvas = tk.Canvas(window, width=300, height=500, bg='#70c5ce')
canvas.pack()


class Bird:
    def __init__(self, genome = []):
        self.x = 50
        self.y = 300
        self.speed = 0


        self.image = tk.PhotoImage(file = file + '\\Картинки\\Птица.png')
        self.image_id = canvas.create_image(self.x, self.y, image = self.image)

        if genome: self.genome = genome
        else: self.genome = [uniform(-1, 1), uniform(-1, 1), uniform(-1, 1)]


        self.jump_reload = True
        self.live = True


        self.score = 0
    

    def move(self, pipe):
        self.score += 1
        canvas.coords(self.image_id, self.x, self.y)
        self.speed += 0.2
        self.y += self.speed


        if self.x + self.image.width() / 2 > pipe.x - pipe.image_pipetop.width() / 2:
            if self.x - self.image.width() / 2 < pipe.x + pipe.image_pipetop.width() / 2:
                if self.y - self.image.height() / 2 < pipe.window_start_y or self.y + self.image.height() / 2 > pipe.window_start_y + pipe.window_gap:
                    self.live = False

    
    def jump(self):
        if self.jump_reload == False: return
        self.jump_reload = False
        window.after(200, self.jump_update)


        self.speed = -5
    

    def jump_update(self):
        self.jump_reload = True
    

    def think(self, pipe):
        n1 = self.y
        n2 = pipe.window_start_y
        n3 = pipe.window_start_y + pipe.window_gap


        out = n1 * self.genome[0] + n2 * self.genome[1] + n3 * self.genome[2]


        if out > 0:
            self.jump()


class Pipe:
    def __init__(self):
        self.x = 250
        self.window_start_y = 200
        self.window_gap = 120
        self.speed = 2


        self.image_pipetop = tk.PhotoImage(file = file + '\\Картинки\\Верхний столб.png')
        self.image_pipebottom = tk.PhotoImage(file = file + '\\Картинки\\Нижний столб.png')


        self.image_top_start = self.window_start_y - self.image_pipetop.height() / 2
        self.image_bottom_start = self.window_start_y + self.image_pipetop.height() / 2 + self.window_gap


        self.image_pipetop_id = canvas.create_image(self.x, self.image_top_start, image = self.image_pipetop) 
        self.image_pipebottom_id = canvas.create_image(self.x, self.image_bottom_start, image = self.image_pipebottom)

        
    def move(self):
        self.x -= self.speed
        canvas.coords(self.image_pipetop_id, self.x, self.image_top_start)
        canvas.coords(self.image_pipebottom_id, self.x, self.image_bottom_start)


        if self.x < -self.image_pipetop.width() / 2:
            self.reload()


    def reload(self):
        self.x = 300 + self.image_pipetop.width() / 2

        
        self.window_start_y = randint(20, 350)
        

        self.image_top_start = self.window_start_y - self.image_pipetop.height() / 2
        self.image_bottom_start = self.window_start_y + self.image_pipetop.height() / 2 + self.window_gap


def main():
    global birds
    for i in range(len(birds)):
        birds[i].move(pipe)
        birds[i].think(pipe)
    

    birds = [bird for bird in birds if bird.live == True]


    for i in range(len(birds)):
        if birds[i].score > best_bird['score']:
            best_bird['genome'] = birds[i].genome
            best_bird['score'] = birds[i].score


    if len(birds) == 0:
        best_genome = best_bird['genome'].copy()
        birds.append(Bird(best_genome))
        for i in range(30):
            mutation_genome = best_genome.copy()
            mutation_genome[randint(0, 2)] += uniform(-0.5, 0.5)
            birds.append(Bird(mutation_genome))
        pipe.reload()


    pipe.move()


    window.after(10, main)


birds = []
for i in range(30):
    birds.append(Bird())
pipe = Pipe()


best_bird = {
    'genome' : [],
    'score' : 0,
}


main()


window.mainloop()