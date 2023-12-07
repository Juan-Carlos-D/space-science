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
datetime_utc = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

# Convert to Ephemeris Time (ET) using the SPICE function utc2et
datetime_et = spiceypy.utc2et(datetime_utc)

solsys_df = pd.DataFrame()
solsys_df.loc[:, "ET"] = [datetime_et]
solsys_df.loc[:, "UTC"] = [datetime_utc]

SOLSYS_DICT = {"SUN": 10, "VENUS": 299, "MOON": 301, "MARS": 4}