import spiceypy
import datetime
import math

# get today's date
date_today = datetime.datetime.today()

# converts the datetime to a string, replacing the time w/ midnight
date_today = date_today.strftime("%Y-%m-%dT00:00:00")

# loads the SPICE kernels for leapseconds and for the planets
spiceypy.furnsh("../Kernels/lsk/naif0012.tls.txt")
spiceypy.furnsh("../Kernels/spk/de432s.bsp")

# computes the Ephemeris Time
et_today_midnight = spiceypy.utc2et(date_today)

# computes the state vector of the Earth w.r.t. the sun
earth_state_wrt_sun, earth_sun_light_time = spiceypy.spkgeo(
    targ=399, et=et_today_midnight, ref="ECLIPJ2000", obs=10
)

# The state vector is 6 dimensional: x, y, z in km and the corresponding velocities in km/s
print(
    'State vector of the Earth w.r.t. the Sun for "today" (midnight):\n',
    earth_state_wrt_sun,
)

# The (Euclidean) distance should be around 1 AU. Why "around"? Well the Earth revolves the Sun in
# a slightly non-perfect circle (elliptic orbit). First, we compute the distance in km
earth_sun_distance = math.sqrt(
    earth_state_wrt_sun[0] ** 2.0
    + earth_state_wrt_sun[1] ** 2.0
    + earth_state_wrt_sun[2] ** 2.0
)

# Convert the distance in astronomical units (1 AU)
# Instead of searching for the "most recent" value, we use the default value in SPICE
# This way, we can easily compare our results with the results of others.
earth_sun_distance_au = spiceypy.convrt(earth_sun_distance, "km", "au")
