import datetime
import spiceypy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as matpl_dates

# Loading the SPICE kernels via a meta file
spiceypy.furnsh("../Kernels/lsk/naif0012.tls.txt")
spiceypy.furnsh("../Kernels/spk/de432s.bsp")

# Create an initial and ending time date-time object that is converted to a
# string
init_time_utc_str = datetime.datetime(year=2023, month=1, day=1).strftime(
    "%Y-%m-%dT%H:%M:%S"
)
end_time_utc_str = datetime.datetime(year=2024, month=10, day=1).strftime(
    "%Y-%m-%dT%H:%M:%S"
)

# Convert to Ephemeris Time (ET) using the SPICE function utc2et
init_time_et = spiceypy.utc2et(init_time_utc_str)
end_time_et = spiceypy.utc2et(end_time_utc_str)

# Set the number of seconds per hours. This value is used to compute the phase
# angles in 1 hour steps (the ET is given in seconds)
delta_hour_in_seconds = 3600.0
time_interval_et = np.arange(init_time_et, end_time_et, delta_hour_in_seconds)

# All our computed parameters, positions etc. shall be stored in a pandas
# dataframe. First, we create an empty one
inner_solsys_df = pd.DataFrame()

# Set the column ET that stores all ETs
inner_solsys_df.loc[:, "ET"] = time_interval_et

# The column UTC transforms all ETs back to a UTC format. The function
# spicepy.et2datetime is NOT an official part of SPICE (there you can find
# et2utc).
# However this function returns immediately a date-time object
inner_solsys_df.loc[:, "UTC"] = inner_solsys_df["ET"].apply(
    lambda x: spiceypy.et2datetime(et=x)
)

# Compute now the phase angle between Venus and Sun as seen from Earth
#
# For this computation we need the SPICE function phaseq. et is the ET. Based
# on SPICE's logic the target is the Earth (399) and the illumination source
# (illmn) is the Sun (10), the observer (obsrvr) is Venus with the ID 299.
# We apply a correction that considers the movement of the planets and the
# light time (LT+S).
inner_solsys_df.loc[:, "EARTH_VEN2SUN_ANGLE"] = inner_solsys_df["ET"].apply(
    lambda x: np.degrees(
        spiceypy.phaseq(et=x, target="399", illmn="10", obsrvr="299", abcorr="LT+S")
    )
)

# Compute the angle between the Moon and the Sun. We apply the same function
# (phaseq). The Moon NAIF ID is 301
inner_solsys_df.loc[:, "EARTH_MOON2SUN_ANGLE"] = inner_solsys_df["ET"].apply(
    lambda x: np.degrees(
        spiceypy.phaseq(et=x, target="399", illmn="10", obsrvr="301", abcorr="LT+S")
    )
)

# Compute finally the phase angle between the Moon and Venus
inner_solsys_df.loc[:, "EARTH_MOON2VEN_ANGLE"] = inner_solsys_df["ET"].apply(
    lambda x: np.degrees(
        spiceypy.phaseq(et=x, target="399", illmn="299", obsrvr="301", abcorr="LT+S")
    )
)

# Are photos of both objects "photogenic"? Let's apply a pandas filtering
# with some artificially set angular distances and create a binary tag for
# photogenic (1) and non-photogenic (0) constellations
#
# Angular distance Venus - Sun: > 30 degrees
# Angular distance Moon - Sun: > 30 degrees
# Angular distance Moon - Venus: < 10 degrees
inner_solsys_df.loc[:, "PHOTOGENIC"] = inner_solsys_df.apply(
    lambda x: 1
    if (x["EARTH_VEN2SUN_ANGLE"] > 30.0)
    & (x["EARTH_MOON2SUN_ANGLE"] > 30.0)
    & (x["EARTH_MOON2VEN_ANGLE"] < 10.0)
    else 0,
    axis=1,
)

# Print the temporal results (number of computed hours, and number of
# "photogenic" hours)
print(
    f"Number of hours computed: {len(inner_solsys_df)}"
    + f" (around {round(len(inner_solsys_df) / 24)} days)"
)

print(
    f'Number of photogenic hours: {len(inner_solsys_df.loc[inner_solsys_df["PHOTOGENIC"] == 1])}'
    f'(around {round(len(inner_solsys_df.loc[inner_solsys_df["PHOTOGENIC"] == 1]) / 24)} days)'
)
