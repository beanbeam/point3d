#!/usr/bin/env python3

import scurses.window as window
import scurses.colors as colors
from point_shapes.simple import *
from math import *
from itertools import repeat

CHAR_DIMENSION_RATIO = 2
FOG_START = 4.5
FOG_STRENGTH = 3.2
TICK_RATE = 60
MIN_BLACK = 233;

def point_c(res, w, h, z):
  ln = []
  for i in range(res+1):
    amt = float(i)/res
    ang = (amt*3*pi/2)+pi/4
    ln.append([cos(ang)*w/2,
               sin(ang)*h/2,
               z])
  return ln

def color_pair_list():
  return list(zip(range(255, MIN_BLACK-1, -1), repeat(colors.BLACK)))

def main(win):
  colors.init(color_pair_list())

  # LETTER A
  #letter  = line(-1.5, 3, 10, 0, -3, 10, 10)
  #letter += line(1.5, 3, 10, 0, -3, 10, 10)
  #letter += line(-.75, 0, 10, .75, 0, 10, 5)

  # LETTER C
  letter  = point_c(10+win.height//20, 3, 6, 10)
  letter += point_c(10+win.height//20, 2.8, 5.6, 10)

  letter  = PointObject(letter)

  ring = PointObject(circle(8, 10, 25))
  #points = torus(5, 4, 6, 25, 10)

  ring_rot_y = 0
  ring_rot_z = 0
  letter_rot = 0

  v = View()
  while True:
    win.clear()
    to_draw = ring.y_rotated(ring_rot_y, 0, 10).z_rotated(ring_rot_z, 0, 0).points
    to_draw += letter.y_rotated(letter_rot, 0, 10).points
    draw(to_draw, v, win)
    ring_rot_y += 1    * pi/TICK_RATE
    ring_rot_z += .413 * pi/TICK_RATE
    letter_rot += .7*pi/TICK_RATE
    win.draw_string(0,0, "Quit - Ctrl+C")
    win.refresh()
    win.sleep(1000 // TICK_RATE)


def draw(points, view, win):
  for point in sorted(points, key = lambda p: p[2], reverse=True):
    posn = view.project(point[0], point[1], point[2])
    w = win.width/CHAR_DIMENSION_RATIO
    h = win.height
    scale = min(w, h)
    xrem = w - scale
    yrem = h - scale
    xpos = int((xrem/2+posn[0]*scale)*CHAR_DIMENSION_RATIO)
    ypos = int(yrem/2+posn[1]*scale)
    char = "o"
    if point[2] < 8.5: char = "O"
    win.draw_string(xpos, ypos, char, get_color_pair(point[2]))


def get_color_pair(d):
  return int(max(1, min(
    FOG_STRENGTH*(d-FOG_START),
    len(color_pair_list()))))

class PointObject(object):
  def __init__(self, points):
    self.points = points

  def translated(self, dx, dy, dz):
    points = []
    for point in self.points:
      points.append([dx+point[0],
                     dy+point[1],
                     dz+point[2]])
    return PointObject(points)

  def y_rotated(self, rad, x_o=0, z_o=0):
    points = []
    for point in self.points:
      r = hypot(point[0]-x_o, point[2]-z_o)
      a = atan2(point[2]-z_o, point[0]-x_o)+rad

      new_x = r*cos(a)+x_o
      new_z = r*sin(a)+z_o
      points.append([new_x, point[1], new_z])
    return PointObject(points)

  def z_rotated(self, rad, x_o=0, y_o=0):
    points = []
    for point in self.points:
      r = hypot(point[0]-x_o, point[1]-y_o)
      a = atan2(point[1]-y_o, point[0]-x_o)+rad

      new_x = r*cos(a)+x_o
      new_y = r*sin(a)+y_o
      points.append([new_x, new_y, point[2]])
    return PointObject(points)


class View(object):
  def __init__(self, x=0, y=0, z=0, fov=.5):
    self.x = x
    self.y = y
    self.z = z
    self.fov = fov

  def project(self, x, y, z):
    x = float(x) - self.x
    y = float(y) - self.y
    z = float(z) - self.z
    fov = float(self.fov)
    return((1+(x/z)/fov)/2,
           (1+(y/z)/fov)/2)

try:
  window.CursesWindow(main)
except KeyboardInterrupt:
  exit()
