import datetime
import spiceypy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Loading the SPICE kernels via a meta file
spiceypy.furnsh("../Solar System Barycenter/kernel_meta.txt")
spiceypy.furnsh("../Kernels/pck/pck00010.tpc.txt")
spiceypy.furnsh("../Kernels/lsk/naif0012.tls.txt")
spiceypy.furnsh("../Kernels/spk/de432s.bsp")

# We want to compute miscellaneous positions w.r.t. the centre of
# the Sun for a certain time interval.
# First, we set an initial time in UTC.
init_time_utc = datetime.datetime(year=2000, month=1, day=1, \
                                  hour=0, minute=0, second=0)
# Add a number of days; you can play around with the datetime variables; but
# leave it as it is for the first try, since other computations and comments
# are based on this value.
delta_days = 10000
end_time_utc = init_time_utc + datetime.timedelta(days=delta_days)

# Convert the datetime objects now to strings
init_time_utc_str = init_time_utc.strftime('%Y-%m-%dT%H:%H:%S')
end_time_utc_str = end_time_utc.strftime('%Y-%m-%dT%H:%H:%S')

# Print the starting and end times
print('Init time in UTC: %s' % init_time_utc_str)
print('End time in UTC: %s\n' % end_time_utc_str)

# Convert to Ephemeris Time (ET) using the SPICE function utc2et
init_time_et = spiceypy.utc2et(init_time_utc_str)
end_time_et = spiceypy.utc2et(end_time_utc_str)

# Create a numpy array that covers a time interval in delta = 1 day step
time_interval_et = np.linspace(init_time_et, end_time_et, delta_days)

# Using km is not intuitive. AU would scale it too severely. Since we compute
# the Solar System Barycentre (SSB) w.r.t. the Sun; and since we expect it to
# be close to the Sun, we scale the x, y, z component w.r.t the radius of the
# Sun. We extract the Sun radii (x, y, z components of the Sun ellipsoid) and
# use the x component
_, radii_sun = spiceypy.bodvcd(bodyid=10, item='RADII', maxn=3)

radius_sun = radii_sun[0]

