'''

 
 File: 
   main.py


 Description:
   A driver for the TLE orbit plotter.


 Record of Revisions:

   Date:         Author:          Description:
   2022-02-06    P. Stegmann      Original Code


'''

import numpy as np
import urllib.request              # Downloading NORAD data
import orbit_gnss as gnss
import orbit_graphics

if __name__ == "__main__":
    # elem1 = """ISS (ZARYA)
    # 1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
    # 2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537"""

    # dragon = """DRAGON CRS-2            
    # 1 39115U 13010A   13062.62492353  .00008823  00000-0  14845-3 0   188
    # 2 39115  51.6441 272.5899 0012056 334.2535  68.5574 15.52501943   306"""

    orbit_graphics.plotEarth()

    gps_orbit = gnss.orbit("gps-ops")

    # Data from NORAD http://www.celestrak.com/NORAD/elements/
    # filename = "noaa.txt" # NOAA satellites
    # filename = "geo.txt" # Geostationary satellites
    # filename = "gps-ops.txt" # GPS sats
    # filename = "military.txt" # Some military satellites
    # filename = "stations.txt" # Space stations
    # filename = "visual.txt" # 100 brightest or so objects

    # files = ["noaa.txt", "stations.txt", "military.txt", "gps-ops.txt"]
    # files = ["stations.txt"]

    names = ["gps-ops"]

    for urlname in names:
        f = urllib.request.urlopen("http://www.celestrak.com/NORAD/elements/%s.txt" % urlname)
        elem = ""
        for line in f:
            line = str(line.decode('UTF-8'))
            elem += line
            if (line[0] == '2'):
                elem = elem.strip()
                if elem.startswith("GPS BIIR-2"):
                    gps_orbit.inspect(elem, printInfo=True, labels=True)
                    print(elem)
                elem = ""

    # gps_orbit.inspect(elem1)
    # gps_orbit.inspect(dragon)

    orbit_graphics.doDraw()
