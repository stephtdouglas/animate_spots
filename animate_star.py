from __future__ import division, print_function, absolute_import

import matplotlib
matplotlib.use("Cairo")
import matplotlib.pyplot as plt
import numpy as np

from draw_star import draw_star, draw_three_stars

def animate_star(star_radius, spot_radius, star_color, spot_theta, filebase,
                 nstars=1,frames_per_rotation=20,nframes=20):
    """
    Given details on 1 star or n stars, plot and save frames for a movie
    showing the stellar rotation.

    If more than 1 star is to be plotted, set nstars to the number of stars
    and all the inputs except filebase should be arrays, with all inputs having
    matching lengths.

    Inputs:
    star_radius (float or arraylike) radius of the star

    spot_radius (float or arraylike) radius of the spot on the stellar surface

    star_color (matplotlib-accepted color or arraylike)
         color of the star to plot

    spot_theta (float or arraylike) the spot's angle from the top of the star

    filebase (string) base filename to use for output files; no extension

    frames_per_rotation (int or arraylike, default=20)
         number of frames per rotation of the star

    nframes (int, default=20)

    Outputs:
    image files with the name <filebase>_%03d.jpg

    the output files can be combined into a movie using the following command:
    avconv -framerate 5 -i <filebase>_%03d.jpg out.mov
    (libav-tools must be installed)

    """

    # make sure there's an input for each star, even if they're repeated
    star_r, spot_r, star_c, spot_t, f_per_r = np.broadcast_arrays(
         star_radius, spot_radius, star_color, spot_theta,
         frames_per_rotation)

    nstars = len(star_r)

    phi_init = np.pi * 1.5

    # What's the change in azimuthal angle between frames for each star
    delta_phi = np.zeros(nstars)
    max_phi = np.zeros(nstars)
    for i in range(nstars):
        delta_phi[i] = 2 * np.pi / f_per_r[i]
        max_phi[i] = delta_phi[i] * nframes + phi_init

    phi = np.zeros(nframes*nstars).reshape((3,-1))
    for i in range(nstars):
        phi[i] = np.arange(phi_init, max_phi[i], delta_phi[i])

    for i in range(nframes):
        draw_three_stars(spot_phi=phi[:,i], spot_theta=spot_t,
                         spot_radius=spot_r,
                         star_color=star_c, star_radius=star_r)
        plt.savefig("{0}_{1:0>3}.jpg".format(filebase,i+1))
        plt.close("all")

if __name__=="__main__":
    star_r = 10
    young_spot_r = np.sqrt(0.22 * star_r**2)
    teen_spot_r = np.sqrt(0.1 * star_r**2)
    old_spot_r = np.sqrt(0.005 * star_r**2)

    spot_theta = np.pi/3
    animate_star(spot_radius=[young_spot_r,teen_spot_r,old_spot_r],
                 star_radius=star_r,star_color="Gold",
                 spot_theta=[np.pi/5,np.pi/4,np.pi/3],
                 frames_per_rotation = [10,20,40], nframes=40,
                 filebase="spot_images/three_stars")
