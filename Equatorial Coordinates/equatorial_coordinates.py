# Import modules
import datetime
import spiceypy
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Load the SPICE kernels via a meta file
spiceypy.furnsh("../Solar System Barycenter/kernel_meta.txt")
spiceypy.furnsh("../Kernels/pck/pck00010.tpc.txt")
spiceypy.furnsh("../Kernels/lsk/naif0012.tls.txt")
spiceypy.furnsh("../Kernels/spk/de432s.bsp")

# Create an initial date-time object that is converted to a string
datetime_utc = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

# Convert to Ephemeris Time (ET) using the SPICE function utc2et
datetime_et = spiceypy.utc2et(datetime_utc)

# We want to compute the coordinates for different Solar System bodies as seen
# from our planet. First, a pandas dataframe is set that is used to append the
# computed data
solsys_df = pd.DataFrame()

# Add the ET and the corresponding UTC date-time string
solsys_df.loc[:, "ET"] = [datetime_et]
solsys_df.loc[:, "UTC"] = [datetime_utc]

# Set a dictionary that lists some body names and the corresponding NAIF ID
# code. Mars has the ID 499, however the loaded kernels do not contain the
# positional information. We use the Mars barycentre instead
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

# Each body shall have an individual color; set a list with some colors
BODY_COLOR_ARRAY = [
    "y",
    "tab:brown",
    "tab:orange",
    "g",
    "tab:gray",
    "tab:red",
    "m",
    "tab:olive",
    "c",
    "b",
    "tab:purple",
]
