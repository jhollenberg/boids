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

starling_num = 80
long_range = .75
short_range = .25
bound_x = 5
bound_y = 5

toward_const = .005

lower_limit_const = .003

separation_factor = .09

alignment_factor = .03

cohesion_factor = .003

avoid_factor = .13

in_bounds_factor = .005
dist_from_edge = 1.5


class Bird:

    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.attr_list = ''
        self.type = ''
        self.limit = 0
        self.limit_factor = 0

    def get_type(self):
        return self.type

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
        for s in starling_list:
            if s != self and self.distance(s) <= dst:
                long_list.append(s)
        return long_list

    def speed_limit(self):
        x = 0
        y = 0
        if self.vx >= self.limit:
            x = -1
        if self.vx <= -self.limit:
            x = 1
        if self.vy >= self.limit:
            y = -1
        if self.vy <= -self.limit:
            y = 1
        #if x + y != 0 and self.get_type() == 'h':
           # print('ul')
        return x * self.limit_factor, y * self.limit_factor

    def update(self):
        vel_list = [0, 0]
        for i in eval(self.attr_list):
            vel_list[0] += i[0]
            vel_list[1] += i[1]

        self.vx += vel_list[0]
        self.vy += vel_list[1]

    def move(self):
        self.update()
        self.x += self.vx
        self.y += self.vy


class Hawk(Bird):

    def __init__(self, x, y, vx, vy):
        super().__init__(x, y, vx, vy)
        self.attr_list = '[self.towards_birds(), self.speed_limit(), self.lower_limit()]'
        self.limit = .14
        self.limit_factor = .04
        self.type = 'h'

    def towards_birds(self):
        x = 0
        y = 0
        for s in starling_list:
            x += s.x
            y += s.y

        x = x/len(starling_list)
        y = y/len(starling_list)
        x_dist = x - self.x
        y_dist = y - self.y
        test = Bird(x, y, 0, 0)

        if (x_dist * self.vx > 0 or y_dist * self.vy > 0) or (self.distance(test) > 20):
            return toward_const * (x - self.x), toward_const * (y - self.y)
        return 0, 0

    def lower_limit(self):
        if math.sqrt(self.get_vel()[0]**2 + self.get_vel()[1]**2) < .15:
            # print('ll')
            return self.vx * lower_limit_const, self.vy * lower_limit_const
        return 0, 0


class Starling(Bird):

    def __init__(self, x, y, vx, vy):
        super().__init__(x, y, vx, vy)
        self.attr_list = '[self.separation(), self.alignment(), self.cohesion(), self.avoid_hawk(), self.in_bounds(), self.speed_limit()]'
        self.limit = .07
        self.limit_factor = .03
        self.type = 's'

        #elf.attr_list = '[self.in_bounds()]'
        # self.x = random.uniform(-bound_x, bound_x)
        # self.y = -bound_y
        # self.vx = random.uniform(-.2, .2)
        # self.vy = random.uniform(0, .2)

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

    def avoid_hawk(self):
        """
        avoid the hawk dawg
        """
        x = 0
        y = 0
        for h in hawk_list:
            if self.distance(h) < 1:
                x -= h.x - self.x
                y -= h.y - self.y
        return avoid_factor * x, avoid_factor * y

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


def animate_helper(item_list, start_frame, plot, frame):
    if frame > start_frame:
        for i in item_list:
            i.move()
        plot.set_data([i.x for i in item_list],
                      [i.y for i in item_list])
    # return plot


def animate(x):
    animate_helper(starling_list, 100, bird_plot, x)
    animate_helper(hawk_list, 100, hawk_plot, x)
    # if x > 100:
    #     for s in starling_list:
    #         s.move()
    #     bird_plot.set_data([s.x for s in starling_list],
    #                         [s.y for s in starling_list])
    # if x > 250:
    #     for h in hawk_list:
    #         h.move()
    #     hawk_plot.set_data([h.x for h in hawk_list],
    #                             [h.y for h in hawk_list])
    #return bird_plot,


starling_list = [Starling(random.uniform(-bound_x, bound_x), -bound_y, random.uniform(
    -.2, .2), random.uniform(0, .2)) for i in range(starling_num)]
hawk_list = [Hawk(-5, 0, .25, random.uniform(-.01, .01))]


fig = plt.figure()
ax = plt.axes(xlim=(-bound_x, bound_x), ylim=(-bound_y, bound_y))
ax.patch.set_facecolor('royalblue')
ax.tick_params(axis='both', left=0, bottom=0, labelleft=0, labelbottom=0)
bird_plot, = plt.plot([s.x for s in starling_list],
                      [s.y for s in starling_list], 'ko', marker='.', ms=4)
hawk_plot, = plt.plot([h.x for h in hawk_list], [h.y for h in hawk_list], 'ro', marker='.', ms=10)

anim = animation.FuncAnimation(fig, animate, interval=10)

plt.show()


