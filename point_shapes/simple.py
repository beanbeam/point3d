from math import *

def line(x1, y1, z1, x2, y2, z2, res):
  pts = []
  xdiff = x2-x1
  ydiff = y2-y1
  zdiff = z2-z1
  for i in range(res+1):
    amt = float(i)/res
    pts.append([x1+xdiff*amt,
               y1+ydiff*amt,
               z1+zdiff*amt])
  return pts

def oval(w, h, z, res):
  pts = []
  for i in range(res):
    amt = float(i)/res
    ang = (amt*2*pi)
    pts.append([cos(ang)*w/2,
               sin(ang)*h/2,
               z])
  return pts

def circle(r, z, res):
  return oval(r, r, z, res)

def torus(inner_r, outer_r, z, res1, res2):
  pts = []
  cross_section_r = (outer_r-inner_r)/2
  center_r = outer_r - cross_section_r
  for i in range(res2):
    amt = float(i)/res2
    ang = (amt*2*pi)
    pts += (circle(center_r+cross_section_r*cos(ang),
                   z+cross_section_r*sin(ang),
                   res1))
  return pts
