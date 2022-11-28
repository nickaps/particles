'''All fundamental particles should only need X and Y'''
import random

import pygame as pg
import numpy as np

from numba import jit, cuda

pg.init()

playing = True
screen = pg.display.set_mode((1250, 900))
pg.display.set_caption("Test")

particles = []

flux = 0.4

t = 0.001
TIME = 0
G = 60
'''time factor'''


class Particle:
    '''default particle with x and y position with mass and size of 1'''

    def __init__(self, x, y, fast_new=True):
        self.x = x
        self.y = y
        self.w = 1
        self.h = 1
        self.mass = 1
        self.charge = 0
        self.color = (255, 255, 255)
        particles.append(self)

    def draw(self, fast_new=True):

        if self.y < 850:
            self.y += G*t

        if self.w == 0:
            pg.draw.line(screen, self.color, (self.x, self.y), (self.x, self.y))
        else:
            pg.draw.circle(screen, self.color, (self.x, self.y), self.h, self.w)

    def displace(self, displacement, fast_new=True):
        self.x += displacement[0]/self.w
        self.y += displacement[1]/self.w

    def behave(self, fast_new=True):
        '''nothing'''

class Pon(Particle):
    def __init__(self, x, y, fast_new=True):
        super().__init__(x, y)
        self.charge = 1
        self.w = 1
        self.h = 1
        self.color = (255, 0, 0)
        self.e = 5

    def behave(self, fast_new=True):
        dx, dy = 0, 0
        for i in particles:
            if len(particles) > 1 and i != self and np.sqrt((self.x - i.x) ** 2 + (self.y - i.y) ** 2) > 5:
                d = np.sqrt((self.x - i.x) ** 2 + (self.y - i.y) ** 2)
                m = (1 / (d/20)) * -(i.charge * self.charge)
                dx += (i.x - self.x) * m * 4
                dy += (i.y - self.y) * m * 4
        self.displace((dx * t, dy * t))

    def E(self, x, fast_new=True):
        self.e = x

class Din(Particle):
    def __init__(self, x, y, fast_new=True):
        super().__init__(x, y)
        self.charge = -1
        self.w = 1
        self.h = 1
        self.color = (0, 0, 255)
        self.e = 5

    def behave(self, fast_new=True):
        dx, dy = 0, 0
        for i in particles:
            if len(particles) > 1 and i != self and np.sqrt((self.x - i.x) ** 2 + (self.y - i.y) ** 2) > 5:
                d = np.sqrt((self.x - i.x) ** 2 + (self.y - i.y) ** 2)
                m = (1 / (d / 20)) * -(i.charge * self.charge)
                dx += (i.x - self.x) * m * 4
                dy += (i.y - self.y) * m * 4
        self.displace((dx * t, dy * t))

    def E(self, x, fast_new=True):
        self.e = x

class Sinestro(Particle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.charge = 0
        self.w = 2
        self.h = 2
        self.color = (255, 255, 0)
        self.e = 400

    def behave(self):
        self.charge = -np.sin(TIME*flux)*3
        self.color = pg.Color(((np.abs(-np.sin(TIME*flux)))*255, (np.abs(-np.sin(TIME*flux)))*255, 0))

        dx, dy = 0, 0
        for i in particles:
            if len(particles) > 1 and i != self and np.sqrt((self.x - i.x) ** 2 + (self.y - i.y) ** 2) > 5:
                d = np.sqrt((self.x - i.x) ** 2 + (self.y - i.y) ** 2)
                m = (1 / (d / 20)) * -(i.charge * self.charge)
                dx += (i.x - self.x) * m * 4
                dy += (i.y - self.y) * m * 4
        self.displace((dx * t, dy * t))

    def E(self, x):
        self.e = x

class GreenLantern(Particle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.charge = 0
        self.w = 2
        self.h = 2
        self.color = (0,255,0)
        self.e = 400

    def behave(self):
        self.charge = np.sin(TIME*flux)*3
        self.color = pg.Color((0, (np.abs(np.sin(TIME*flux)))*255, 0))

        dx, dy = 0, 0
        for i in particles:
            if len(particles) > 1 and i != self and np.sqrt((self.x - i.x) ** 2 + (self.y - i.y) ** 2) > 5:
                d = np.sqrt((self.x - i.x) ** 2 + (self.y - i.y) ** 2)
                m = (1 / (d / 20)) * -(i.charge * self.charge)
                dx += (i.x - self.x) * m * 4
                dy += (i.y - self.y) * m * 4
        self.displace((dx * t, dy * t))

    def E(self, x):
        self.e = x


class Athon:
    def __init__(self, x, y, degree, positive_core=True):
        self.d = degree
        if degree < 3:
            self.d = 3

        if positive_core == True:
            for i in range(self.d):
                z = random.randrange(0, np.round(2*np.pi*1000), 1)/1000
                Pon(x+np.cos(z)*2,y+np.sin(z)*2)
            for i in range(self.d):
                z = random.randrange(0, np.round(2*np.pi*1000), 1)/1000
                Din(x+np.cos(z)*10,y+np.sin(z)*10)
        else:
            for i in range(self.d):
                z = random.randrange(0, np.round(2*np.pi*1000), 1)/1000
                Din(x+np.cos(z)*2,y+np.sin(z)*2)
            for i in range(self.d):
                z = random.randrange(0, np.round(2*np.pi*1000), 1)/1000
                Pon(x+np.cos(z)*10,y+np.sin(z)*10)

'''
for i in range(80):
    s = Pon(random.randint(100, 150), random.randint(420,480))
    s.E(10)

for i in range(80):
    s = Din(random.randint(1050, 1100), random.randint(420,480))
    s.E(10)
'''


while playing:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            playing = False

        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            t += 0.0002

        if keys[pg.K_DOWN] and t > 0:
            t -= 0.0002


        if keys[pg.K_g]:
            G -= 20
        if keys[pg.K_t]:
            G += 20

        if keys[pg.K_BACKSPACE] and len(particles) > 0:
            particles.remove(particles[len(particles)-1])

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                Athon(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], 3)

            if event.key == pg.K_w:
                Pon(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])

            if event.key == pg.K_s:
                Din(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])

            if event.key == pg.K_SPACE:
                t = 0

    screen.fill((0, 0, 0))
    for i in particles:

        i.draw()
        i.behave()

    TIME += t
    pg.display.update()
