'''

 
 File: 
   orbit_gnss.py


 Description:
   A Python module to download Two-Line-Element (TLE) format from NORAD to 
   determine and plot the orbit of a given Earth-orbit satellite.


 Record of Revisions:

   Date:         Author:          Description:
   2021-12-06    P. Stegmann      Original Code


'''

# Standard modules
import numpy as np                # Numerics
import pytz                       # World timezone definitions
import unicodedata                # to remove all control characters in TLE.txt
from datetime import datetime, \
                     timedelta

# Local modules
import orbit_graphics              # Plotting Earth and orbits


class orbit:
  '''
   
   Description:
     Class for objects representing a satellite orbit.

  '''
  
  def __init__(self, name):
  	#
    # Description:
    #   'orbit' class Constructor.
    #

  	# Timezone declaration
    self.pdt = pytz.timezone('US/Pacific')

    # Standard Gravitational parameter of Earth
    self.GM = 398600.4418 # unit [ km^3/s^2 ]


  def splitElem(self, tle):
  	#
  	# Description:
    #   Splits a two line element set into title 
    #   and its two lines with stripped lines.
    #
    return map(lambda x: x.strip(), tle.split('\n'))


  def checkValid(self, tle):
  	#
  	# Description:
    #   Checks with checksum to make sure element is valid.
    #
    title, line1, line2 =  self.splitElem(tle)

    return line1[0] == '1' and \
           line2[0] == '2' and \
           line1[2:7] == line2[2:7] and \
           int(line1[-1]) == self.doChecksum(line1) and \
           int(line2[-1]) == self.doChecksum(line2)


  def stringScientificNotation2Float(self, sn):
  	#
  	# Description:
    #   Specific format is 5 digits, a + or -, 
    #   and 1 digit, ex: 01234-5 which is 0.01234e-5
    #
    return 0.00001*float(sn[5]) * 10**int(sn[6:])


  def eccentricAnomalyFromMean(self, \
  	                           mean_anomaly, \
  	                           eccentricity, \
  	                           initValue, \
  	                           maxIter=500, \
  	                           maxAccuracy = 0.0001):
    #
    # Description:
    #   Approximates Eccentric Anomaly from Mean Anomaly.
    #   All input and outputs are in radians.
    #
    mean_anomaly = mean_anomaly
    e0 = initValue
    for x in range(maxIter):
        e1 = e0 - (e0 - eccentricity * np.sin(e0) - mean_anomaly) \
        / (1.0 - eccentricity * np.cos(e0))
        if( abs(e1-e0) < maxAccuracy ):
            break
    return e1


  def inspect(self, \
  	          tle, \
  	          printInfo = True, \
  	          labels = True):
    # 
    # Description:
    #   Returns commented information on a two line element.
    #
    title, line1, line2 =  self.splitElem(tle)
    if not self.checkValid(tle):
      print("Invalid element.")
      return

    satellite_number                                        = int(line1[2:7])
    classification                                          = line1[7:8]
    epoch_year                                              = int(line1[18:20])
    epoch                                                   = float(line1[20:32])
    international_designator_year                           = int(line1[9:11])
    international_designator_launch_number                  = int(line1[11:14])
    international_designator_piece_of_launch                = line1[14:17]
    first_time_derivative_of_the_mean_motion_divided_by_two = float(line1[33:43])
    second_time_derivative_of_mean_motion_divided_by_six    = self.stringScientificNotation2Float(line1[44:52])
    bstar_drag_term                                         = self.stringScientificNotation2Float(line1[53:61])
    the_number_0                                            = float(line1[62:63])
    element_number                                          = float(line1[64:68])
    checksum1                                               = float(line1[68:69])

    satellite        = int(line2[2:7])
    inclination      = float(line2[8:16])
    right_ascension  = float(line2[17:25])
    eccentricity     = float(line2[26:33]) * 0.0000001
    argument_perigee = float(line2[34:42])
    mean_anomaly     = float(line2[43:51])
    mean_motion      = float(line2[52:63])
    revolution       = float(line2[63:68])
    checksum2        = float(line2[68:69])

    # Inferred Epoch date
    year = 2000 + epoch_year if epoch_year < 70 else 1900 + epoch_year
    epoch_date = datetime(year=year, month=1, day=1, tzinfo=pytz.utc) \
                 + timedelta(days=epoch-1) # Have to subtract one day to get correct midnight

    # Time difference of now from epoch, offset in radians
    diff = datetime.now().replace(tzinfo=pytz.utc) \
           + timedelta(hours=8) \
           - epoch_date # Offset for PDT
    diff_seconds = 24*60*60*diff.days \
                   + diff.seconds \
                   + 1e-6*diff.microseconds        # Conversion of difference to seconds.
    print("Time offset: %s" % diff)
    motion_per_sec = mean_motion * 2*np.pi / (24*60*60) # rad/sec
    print("Radians per second: %g" % motion_per_sec)
    offset = diff_seconds * motion_per_sec #rad
    print("Offset to apply: %g" % offset)
    mean_anomaly += offset * 180/np.pi % 360

    # Inferred period
    day_seconds = 24*60*60
    period = day_seconds * 1./mean_motion

    # Inferred semi-major axis (in km)
    semi_major_axis = ((period/(2*np.pi))**2 * self.GM)**(1./3)

    # Inferred true anomaly
    eccentric_anomaly = self.eccentricAnomalyFromMean(mean_anomaly * np.pi/180, eccentricity, mean_anomaly * np.pi/180)
    true_anomaly = 2*np.arctan2(np.sqrt(1+eccentricity) * np.sin(eccentric_anomaly/2.0), np.sqrt(1-eccentricity) * np.cos(eccentric_anomaly/2.0))
    # Convert to degrees
    eccentric_anomaly *= 180/np.pi
    true_anomaly *= 180/np.pi

    if (printInfo):
      print("----------------------------------------------------------------------------------------")
      print(tle)
      print("----------------------------------------------------------------------------------------")
      print("Satellite Name                                            = %s" % title)
      print("Satellite number                                          = ", satellite_number)
      if classification == 'U': 
        print("Unclassified")
      else: 
        print("Classified")
      print("International Designator                                  = YR: %02d, LAUNCH #%d, PIECE: %s" % (international_designator_year, \
        international_designator_launch_number,\
         international_designator_piece_of_launch))
      print("Epoch Date                                                = %s  (YR:%02d DAY:%.11g)" % (epoch_date.strftime("%Y-%m-%d %H:%M:%S.%f %Z"),\
       epoch_year, epoch))
      print("First Time Derivative of the Mean Motion divided by two   = %g" % first_time_derivative_of_the_mean_motion_divided_by_two)
      print("Second Time Derivative of Mean Motion divided by six      = %g" % second_time_derivative_of_mean_motion_divided_by_six)
      print("BSTAR drag term                                           = %g" % bstar_drag_term)
      print("The number 0                                              = %g" % the_number_0)
      print("Element number                                            = %g" % element_number)
      print()
      print("Inclination [Degrees]                                     = %g°" % inclination)
      print("Right Ascension of the Ascending Node [Degrees]           = %g°" % right_ascension)
      print("Eccentricity                                              = %g" % eccentricity)
      print("Argument of Perigee [Degrees]                             = %g°" % argument_perigee)
      print("Mean Anomaly [Degrees] Anomaly                            = %g°" % mean_anomaly)
      print("Eccentric Anomaly                                         = %g°" % eccentric_anomaly)
      print("True Anomaly                                              = %g°" % true_anomaly)
      print("Mean Motion [Revs per day] Motion                         = %g" % mean_motion)
      print("Period                                                    = %s" % timedelta(seconds=period))
      print("Revolution number at epoch [Revs]                         = %g" % revolution)

      print("----------------------------------------------------------------------------------------")
      print("semi_major_axis = %gkm" % semi_major_axis)
      print("eccentricity    = %g" % eccentricity)
      print("inclination     = %g°" % inclination)
      print("arg_perigee     = %g°" % argument_perigee)
      print("right_ascension = %g°" % right_ascension)
      print("true_anomaly    = %g°" % true_anomaly)
      print("----------------------------------------------------------------------------------------")

    if labels:
      orbit_graphics.plotOrbit(semi_major_axis, \
        	             eccentricity, \
        	             inclination, \
                         right_ascension, \
                         argument_perigee, \
                         true_anomaly, \
                         title)
    else:
      orbit_graphics.plotOrbit(semi_major_axis, \
        	             eccentricity, \
        	             inclination, \
                         right_ascension, \
                         argument_perigee, \
                         true_anomaly)

  def doChecksum(self,line):
  	#
  	# Description:
    #   The checksums for each line are calculated by adding 
    #   all numerical digits for that line, including the 
    #   line number. One is added to the checksum for each 
    #   negative sign (-) on that line. All other non-digit 
    #   characters are ignored.
    #  
    # Note: 
    #   This excludes last char for the checksum thats already there.
    #
    return sum( map( int, filter( lambda c: c >= '0' and c <= '9', line[:-1].replace('-','1') ) ) ) % 10

  def remove_control_characters(self,s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")
