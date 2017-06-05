from __future__ import division, print_function, absolute_import

import matplotlib
matplotlib.use("Cairo")
import matplotlib.pyplot as plt
import numpy as np

from draw_star import draw_star

def animate_star(star_radius, spot_radius, star_color, spot_theta, filebase):
    """
    Given details on 1 star or n stars, plot and save frames for a movie
    showing the stellar rotation.

    If more than 1 star is to be plotted, all the inputs except filebase should
    be arrays, with all inputs having matching lengths.

    Inputs:
    star_radius (float) radius of the star
    spot_radius (float) radius of the spot on the stellar surface
    star_color (matplotlib color) color of the overall star to plot
    spot_theta (float) the spot's angle from the top of the star
    filebase (string) base filename to use for output files; no extension

    Outputs:
    image files with the name <filebase>_%03d.jpg

    the output files can be combined into a movie using the following command:
    avconv -framerate 5 -i <filebase>_%03d.jpg out.mov
    (libav-tools must be installed)

    """

    one_rotation = np.linspace(0,2*np.pi,20)
    phi_sequence = np.append(one_rotation[:-1], np.append(one_rotation[:-1],
                                                          one_rotation))

    for i, phi in enumerate(phi_sequence):
        draw_star(phi, spot_theta, spot_radius=spot_radius,
                  star_color=star_color, star_radius=star_radius)
        plt.savefig("{0}_{1:0>3}.jpg".format(filebase,i+1))
        plt.close("all")

if __name__=="__main__":
    star_r = 10
    young_spot_r = np.sqrt(0.22 * star_r**2)

    spot_theta = np.pi/3
    animate_star(spot_radius=young_spot_r,star_radius=star_r,star_color="Gold",
                spot_theta=np.pi/5,filebase="spot_images/young_star")
