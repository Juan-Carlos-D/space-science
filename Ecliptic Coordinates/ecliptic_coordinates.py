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

# Create an initial date-time object that is converted to a string
datetime_utc = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

# Convert to Ephemeris Time (ET) using the SPICE function utc2et
datetime_et = spiceypy.utc2et(datetime_utc)

solsys_df = pd.DataFrame()
solsys_df.loc[:, "ET"] = [datetime_et]
solsys_df.loc[:, "UTC"] = [datetime_utc]

SOLSYS_DICT = {
    "SUN": 10,
    "MERCURY": 1,
    "VENUS": 299,
    "EARTH": 3,
    "MOON": 301,
    "MARS": 4,
    "JUPITER": 5,
    "SATURN": 6,
    "URANUS": 7,
    "NEPTUNE": 8,
    "PLUTO": 9,
}


# Iterate through the dictionary and compute miscellaneous positional
# parameters
for body_name in SOLSYS_DICT:
    # First, compute the directional vector Earth - body in ECLIPJ2000. Use
    # LT+S light time correction. spkezp returns the directional vector and
    # light time. Apply [0] to get only the vector
    solsys_df.loc[:, f"dir_{body_name}_wrt_earth_ecl"] = solsys_df["ET"].apply(
        lambda x: spiceypy.spkezp(
            targ=SOLSYS_DICT[body_name], et=x, ref="ECLIPJ2000", abcorr="LT+S", obs=399
        )[0]
    )
    
    # Compute the longitude and latitude of the body in radians in ECLIPJ2000
    # using the function recrad. recrad returns the distance, longitude and
    # latitude value; thus, apply [1] and [2] to get the longitude and
    # latitude, respectively
    solsys_df.loc[:, f"{body_name}_long_rad_ecl"] = solsys_df[
        f"dir_{body_name}_wrt_earth_ecl"
    ].apply(lambda x: spiceypy.recrad(x)[1])

    solsys_df.loc[:, f"{body_name}_lat_rad_ecl"] = solsys_df[
        f"dir_{body_name}_wrt_earth_ecl"
    ].apply(lambda x: spiceypy.recrad(x)[2])

    solsys_df["SUN_long_rad_ecl"]

# Create an empty matplotlib example plot to show how matplotlib displays
# projected data

# Use a dark background
plt.style.use('dark_background')

# Set a figure
plt.figure(figsize=(12, 8))

# Apply the aitoff projection and activate the grid
plt.subplot(projection="aitoff")
plt.grid(True)

# Set long. / lat. labels
plt.xlabel('Long. in deg')
plt.ylabel('Lat. in deg')

# Save the figure
plt.savefig('empty_aitoff.png', dpi=300)