from __future__ import division, print_function, absolute_import

import matplotlib
matplotlib.use("Cairo")
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

def add_spot(x, y, z, star_radius, spot_phi, spot_theta, spot_radius):

    spot_center_uv = np.array([spot_phi,spot_theta])
    spot_center_xyz = np.array([np.outer(np.cos(spot_center_uv[0]),np.sin(spot_center_uv[1])),
                                np.outer(np.sin(spot_center_uv[0]),
                                         np.sin(spot_center_uv[1])),
                                np.outer(1,np.cos(spot_center_uv[1]))])

    x_sep = x/star_radius - spot_center_xyz[0]
    y_sep = y/star_radius - spot_center_xyz[1]
    z_sep = z/star_radius - spot_center_xyz[2]

    chord_length = np.sqrt(x_sep**2 + y_sep**2 + z_sep**2)
    central_angle = 2 * np.arcsin(chord_length/2)
    great_circle_distance = star_radius * central_angle

    spot = great_circle_distance < spot_radius

    return spot


def draw_star(spot_phi, spot_theta, spot_radius=2,
              star_color="OrangeRed", star_radius=10,
              ax=None):

    if ax is None:
        fig = plt.figure(figsize=(9,9))
        ax = fig.add_subplot(111,projection='3d')

    phi = np.linspace(0,2*np.pi,512)
    theta = np.linspace(0,np.pi,256)

    r = star_radius

    x = r*np.outer(np.cos(phi),np.sin(theta))
    y = r*np.outer(np.sin(phi),np.sin(theta))
    z = r*np.outer(np.ones(np.size(phi)),np.cos(theta))

    spot = add_spot(x, y, z, r, spot_phi, spot_theta, spot_radius)

    c = np.empty(z.shape,"S12")
    c[:] = star_color
    c[spot] = "Grey"
    spot = add_spot(x, y, z, r, spot_phi, spot_theta, spot_radius*0.7)
    c[spot] = "Black"

#     spot = add_spot(x, y, z, r, spot_phi+np.pi/4, spot_theta-np.pi/6, spot_radius)
#     c[spot] = "Black"

    ax.plot_surface(x,y,z,facecolors=c,rstride=2,cstride=2)

    ax._axis3don = False

if __name__=="__main__":

    star_r = 10
    young_spot_r = np.sqrt(0.22 * star_r**2)
    teen_spot_r = np.sqrt(0.1 * star_r**2)
    old_spot_r = np.sqrt(0.005 * star_r**2)

    spot_theta = np.pi/3
    draw_star(np.pi*1.5,np.pi/5,spot_radius=young_spot_r,star_color="Gold",
              star_radius=star_r)
    plt.savefig("young_star.jpg")
    draw_star(np.pi*1.5,np.pi/4,spot_radius=teen_spot_r,star_color="Gold",
              star_radius=star_r)
    plt.savefig("teen_star.jpg")
    draw_star(np.pi*1.5,np.pi/3,spot_radius=old_spot_r,star_color="Gold",
              star_radius=star_r)
    plt.savefig("old_star.jpg")
