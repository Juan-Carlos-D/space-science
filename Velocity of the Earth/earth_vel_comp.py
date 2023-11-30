import spiceypy
import datetime
import numpy as np

date_today = datetime.datetime.today()
date_today = date_today.strftime("%Y-%m-%dT00:00:00")

spiceypy.furnsh("../Kernels/lsk/naif0012.tls.txt")
spiceypy.furnsh("../Kernels/spk/de432s.bsp")

et_today_midnight = spiceypy.utc2et(date_today)

earth_state_wrt_sun, earth_sun_light_time = spiceypy.spkgeo(
    targ=399, et=et_today_midnight, ref="ECLIPJ2000", obs=10
)

print(
    f"State vector of the Earth w.r.t. the Sun for {date_today} (midnight):\n"
    + f"{earth_state_wrt_sun}"
)

# Convert list to numpy array
earth_state_wrt_sun = np.array(earth_state_wrt_sun)

# Compute the distance
earth_sun_distance = np.linalg.norm(earth_state_wrt_sun[:3])

# First, we compute the actual orbital speed of the Earth around the Sun
earth_orb_speed_wrt_sun = np.linalg.norm(earth_state_wrt_sun[3:])

# It's around 30 km/s
print(
    f"Current orbital speed of the Earth around the Sun in km/s: {earth_orb_speed_wrt_sun}"
)

# Now let's compute the theoretical expectation. First, we load a pck file that contains
# miscellanoeus information, like the G*M values for different objects

# First, load the kernel
spiceypy.furnsh("../Kernels/pck/gm_de431.tpc.txt")
_, GM_SUN = spiceypy.bodvcd(bodyid=10, item="GM", maxn=1)

# Now compute the orbital speed
v_orb_func = lambda gm, r: np.sqrt(gm / r)
earth_orb_speed_wrt_sun_theory = v_orb_func(GM_SUN[0], earth_sun_distance)

# Print the result
print(
    f"Theoretical orbital speed of the Earth around the Sun in km/s: "
    + f"{earth_orb_speed_wrt_sun_theory}"
)

# A second check:
# The angular difference between the autumn equinox and today's position vector of the Earth
# (in this tutorial October) should be in degrees the number of days passed the 22th September.
# Again please note: we use the "today" function to determine the Earth's state vector.
# Now the "autumn vector" is simpley (1, 0, 0) in ECLIPJ2000 and we use this as a quick and simple
# rough estimation / computation

# Position vector
earth_position_wrt_sun = earth_state_wrt_sun[:3]

# Normalize it
earth_position_wrt_sun_normed = earth_position_wrt_sun / earth_sun_distance

# Define the "autumn vector" of the Earth
earth_position_wrt_sun_normed_autumn = np.array([1.0, 0.0, 0.0])

ang_dist_deg = np.degrees(
    np.arccos(
        np.dot(earth_position_wrt_sun_normed, earth_position_wrt_sun_normed_autumn)
    )
)
print(
    f"Angular distance between autumn and today's position in degrees {date_today}: "
    + f"{ang_dist_deg}"
)
