"""
separation: short range repulsion, opposite of average position of neighbors
alignment: long range attraction, average velocity of neighbors
cohesion: long range attraction, average position of neighbors

with help from https://eater.net/boids and https://github.com/beneater/boids/blob/master/boids.js
"""

# import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import math
import random

bird_num = 80
long_range = .75
short_range = .25
bound_x = 5
bound_y = 5

separation_factor = .09

alignment_factor = .03

cohesion_factor = .003

in_bounds_factor = .005
dist_from_edge = 1.5

limit_factor = .03
limit = .07

class Bird:

    def __init__(self):
        #self.x = random.uniform(2, 4)
        self.x = random.uniform(-bound_x, bound_x)
        self.y = -bound_y
        #self.y = random.uniform(-bound_y, bound_y)
        self.vx = random.uniform(-.2, .2)
        self.vy = random.uniform(0, .2)

    def get_loc(self):
        return self.x, self.y

    def get_vel(self):
        return self.vx, self.vy

    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def close_birds(self, range_len):
        """
        range = 'l' ==> long range
        range = 's' ==> short range
        returns all birds within range of self
        """

        if range_len == 'l':
            dst = long_range
        elif range_len == 's':
            dst = short_range
        else:
            print("wrong range input")
            return
        long_list = []
        for b in bird_list:
            if b != self and self.distance(b) <= dst:
                long_list.append(b)
        return long_list

    def separation(self):
        """
        short range repulsion
        returns vector to position opposite of center of mass of short range close birds
        """
        # short range repulsion
        x = self.x
        y = self.y
        close_list = self.close_birds('s')
        for b in close_list:
            x += b.x
            y += b.y
        x = x/(len(close_list) + 1)
        y = y/(len(close_list) + 1)
        return -(x - self.x) * separation_factor, -(y - self.y) * separation_factor

    def alignment(self):
        """
        returns vector of average velocity of long range close birds
        """

        x = 0
        y = 0
        close_list = self.close_birds('l')
        for b in close_list:
            x += b.vx
            y += b.vy
        x = x/(len(close_list) + 1)
        y = y/(len(close_list) + 1)
        return (x - self.vx) * alignment_factor, (y - self.vy) * alignment_factor

    def cohesion(self):
        """
        velocity vector to average position of long range close birds
        """

        x = 0
        y = 0
        close_list = self.close_birds('l')
        for b in close_list:
            x += b.x
            y += b.y
        x = x / (len(close_list) + 1)
        y = y / (len(close_list) + 1)
        return (x - self.x) * cohesion_factor, (y - self.y) * cohesion_factor

    def in_bounds(self):
        x = 0
        y = 0
        if self.x >= bound_x - dist_from_edge:
            x = -1
        if self.x <= -bound_x + dist_from_edge:
            x = 1
        if self.y >= bound_y - dist_from_edge:
            y = -1
        if self.y <= -bound_y + dist_from_edge:
            y = 1
        return x * in_bounds_factor, y * in_bounds_factor

    def speed_limit(self):
        x = 0
        y = 0
        if self.vx >= limit:
            x = -1
        if self.vx <= -limit:
            x = 1
        if self.vy >= limit:
            y = -1
        if self.vy <= -limit:
            y = 1
        return x * limit_factor, y * limit_factor

    def update(self):
        attr_list = [self.separation(), self.alignment(), self.cohesion(), self.in_bounds(), self.speed_limit()]
        vel_list = [0, 0]
        for i in attr_list:
            vel_list[0] += i[0]
            vel_list[1] += i[1]
        self.vx += vel_list[0]
        self.vy += vel_list[1]

    def move(self):
        self.update()
        self.x += self.vx
        self.y += self.vy


def animate(x):
    if x > 100:
        for b in bird_list:
            b.move()
            bird_plot.set_data([b.x for b in bird_list],
                               [b.y for b in bird_list])
    return bird_plot,


bird_list = [Bird() for i in range(bird_num)]

fig = plt.figure()
ax = plt.axes(xlim=(-bound_x, bound_x), ylim=(-bound_y, bound_y))
ax.patch.set_facecolor('royalblue')
ax.tick_params(axis='both', left=0, bottom=0, labelleft=0, labelbottom=0)
bird_plot, = plt.plot([b.x for b in bird_list],
             [b.y for b in bird_list], 'ko', marker='.', ms=4)

anim = animation.FuncAnimation(fig, animate, interval=10)

plt.show()


