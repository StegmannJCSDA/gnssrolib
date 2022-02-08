'''

 
 File: 
   graphics.py


 Description:
   A Python module to plot satellite orbits.


 Record of Revisions:

   Date:         Author:          Description:
   2022-02-06    P. Stegmann      Original Code


'''

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


fig = plt.figure(figsize=plt.figaspect(1))  # Square figure
ax = fig.add_subplot(111, projection='3d', aspect="auto")

max_radius = 0

def plotEarth():
    "Draw Earth as a globe at the origin"
    Earth_radius = 6371 # km
    global max_radius
    max_radius = max(max_radius, Earth_radius)
    
    # Coefficients in a0/c x**2 + a1/c y**2 + a2/c z**2 = 1 
    coefs = (1, 1, 1)  

    # Radii corresponding to the coefficients:
    rx, ry, rz = [Earth_radius/np.sqrt(coef) for coef in coefs]

    # Set of all spherical angles:
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)

    # Cartesian coordinates that correspond to the spherical angles:
    # (this is the equation of an ellipsoid):
    x = rx * np.outer(np.cos(u), np.sin(v))
    y = ry * np.outer(np.sin(u), np.sin(v))
    z = rz * np.outer(np.ones_like(u), np.cos(v))

    # Plot:
    ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='b')


def plotOrbit(semi_major_axis, eccentricity=0, inclination=0, 
              right_ascension=0, argument_perigee=0, true_anomaly=0, label=None):
    "Draws orbit around an earth in units of kilometers."
    # Rotation matrix for inclination
    inc = inclination * np.pi / 180.;
    R = np.matrix([[1, 0, 0],
                   [0, np.cos(inc), -np.sin(inc)],
                   [0, np.sin(inc), np.cos(inc)]    ])

    # Rotation matrix for argument of perigee + right ascension
    rot = (right_ascension + argument_perigee) * np.pi/180.
    R2 = np.matrix([[np.cos(rot), -np.sin(rot), 0],
                    [np.sin(rot), np.cos(rot), 0],
                    [0., 0., 1.]    ])    

    ### Draw orbit
    theta = np.linspace(0,2.*np.pi, 360)
    r = (semi_major_axis * (1-eccentricity**2)) / (1 + eccentricity*np.cos(theta))

    xr = r*np.cos(theta)
    yr = r*np.sin(theta)
    zr = 0 * theta

    pts = np.transpose(np.matrix([xr,yr,zr]))
    # Rotate by inclination
    # Rotate by ascension + perigee
    pts =  (R * R2 * pts.T).T


    # Turn back into 1d vectors
    xr,yr,zr = pts[:,0].A.flatten(), pts[:,1].A.flatten(), pts[:,2].A.flatten()

    # Plot the orbit
    ax.plot(xr, yr, zr, '-')
    # plt.xlabel('X (km)')
    # plt.ylabel('Y (km)')
    # plt.zlabel('Z (km)')

    # Plot the satellite
    sat_angle = true_anomaly * np.pi/180.
    satr = (semi_major_axis * (1-eccentricity**2.)) / (1 + eccentricity*np.cos(sat_angle))
    satx = satr * np.cos(sat_angle)
    saty = satr * np.sin(sat_angle)
    satz = 0

    sat = (R * R2 * np.matrix([satx, saty, satz]).T ).flatten()
    satx = sat[0,0]
    saty = sat[0,1]
    satz = sat[0,2]

    c = np.sqrt(satx*satx + saty*saty)
    lat = np.arctan2(satz, c) * 180./np.pi
    lon = np.arctan2(saty, satx) * 180./np.pi
    print("%s : Lat: %g° Long: %g" % (label, lat, lon))
    
    # Draw radius vector from earth
    # ax.plot([0, satx], [0, saty], [0, satz], 'r-')
    # Draw red sphere for satellite
    ax.plot([satx],[saty],[satz], 'ro')

    global max_radius
    max_radius = max(max(r), max_radius)
    ax.set_xlabel(r'$x_{Geocentric}$ [km]')
    ax.set_ylabel(r'$y_{Geocentric}$ [km]')
    ax.set_zlabel(r'$z_{Geocentric}$ [km]')

    # Write satellite name next to it
    if label:
        ax.text(satx, saty, satz, label, fontsize=12)

def doDraw():
    # Adjustment of the axes, so that they all have the same span:
    for axis in 'xyz':
        getattr(ax, 'set_{}lim'.format(axis))((-max_radius, max_radius))
    
    # Draw figure
    plt.savefig('orbit_plot.png')
    plt.show()
