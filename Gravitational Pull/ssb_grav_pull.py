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
init_time_utc = datetime.datetime(year=2000, month=1, day=1, hour=0, minute=0, second=0)
# Add a number of days; you can play around with the datetime variables; but
# leave it as it is for the first try, since other computations and comments
# are based on this value.
delta_days = 10000
end_time_utc = init_time_utc + datetime.timedelta(days=delta_days)

# Convert the datetime objects now to strings
init_time_utc_str = init_time_utc.strftime("%Y-%m-%dT%H:%H:%S")
end_time_utc_str = end_time_utc.strftime("%Y-%m-%dT%H:%H:%S")

# Print the starting and end times
print("Init time in UTC: %s" % init_time_utc_str)
print("End time in UTC: %s\n" % end_time_utc_str)

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
_, radii_sun = spiceypy.bodvcd(bodyid=10, item="RADII", maxn=3)

radius_sun = radii_sun[0]

solar_system_df = pd.DataFrame()
solar_system_df.loc[:, "ET"] = time_interval_et

solar_system_df.loc[:, "UTC"] = solar_system_df["ET"].apply(
    lambda x: spiceypy.et2datetime(et=x).date()
)
solar_system_df.loc[:, "POS_SSB_WRT_SUN"] = solar_system_df["ET"].apply(
    lambda x: spiceypy.spkgps(targ=0, et=x, ref="ECLIPJ2000", obs=10)[0]
)
solar_system_df.loc[:, "POS_SSB_WRT_SUN_SCALED"] = solar_system_df[
    "POS_SSB_WRT_SUN"
].apply(lambda x: x / radius_sun)
solar_system_df.loc[:, "SSB_WRT_SUN_SCALED_DIST"] = solar_system_df[
    "POS_SSB_WRT_SUN_SCALED"
].apply(lambda x: spiceypy.vnorm(x))


# Compute the Phase Angle
NAIF_ID_DICT = {
    "MER": 1,
    "VEN": 2,
    "EAR": 3,
    "MAR": 4,
    "JUP": 5,
    "SAT": 6,
    "URA": 7,
    "NEP": 8,
    "PLU": 9,
}

for planets_name_key in NAIF_ID_DICT:
    planet_pos_col = f"POS_{planets_name_key}_WRT_SUN"
    planet_angle_col = f"PHASE_ANGLE_SUN_{planets_name_key}2SSB"

    planet_id = NAIF_ID_DICT[planets_name_key]

    solar_system_df.loc[:, planet_pos_col] = solar_system_df["ET"].apply(
        lambda x: spiceypy.spkgps(targ=planet_id, et=x, ref="ECLIPJ2000", obs=10)[0]
    )

    solar_system_df.loc[:, planet_angle_col] = solar_system_df.apply(
        lambda x: np.degrees(spiceypy.vsep(x[planet_pos_col], x["POS_SSB_WRT_SUN"])),
        axis=1,
    )

print(solar_system_df["PHASE_ANGLE_SUN_JUP2SSB"])

plt.style.use("dark_background")
fig, (ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9) = plt.subplots(
    9, 1, sharex=True, figsize=(8, 45)
)
for ax_f, planet_abr, planet_name in zip(
    [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9],
    ["MER", "VEN", "EAR", "MAR", "JUP", "SAT", "URA", "NEP", "PLU"],
    [
        "Mercury",
        "Venus",
        "Earth",
        "Mars",
        "Jupiter",
        "Saturn",
        "Uranus",
        "Neptune",
        "Pluto",
    ],
):
    ax_f.set_title(planet_name, color="tab:orange")

    ax_f.plot(
        solar_system_df["UTC"],
        solar_system_df["SSB_WRT_SUN_SCALED_DIST"],
        color="tab:cyan",
    )

    ax_f.set_ylabel("SSB Dist. in Sun Radii", color="tab:cyan")
    ax_f.tick_params(axis="y", labelcolor="tab:cyan")
    ax_f.set_xlim(min(solar_system_df["UTC"]), max(solar_system_df["UTC"]))
    ax_f.set_ylim(0, 2)

    ax_f_add = ax_f.twinx()
    ax_f_add.plot(
        solar_system_df["UTC"],
        solar_system_df[f"PHASE_ANGLE_SUN_{planet_abr}2SSB"],
        color="tab:orange",
    )

    ax_f_add.set_ylabel("Planet phase angle in deg.", color="tab:orange")
    ax_f_add.tick_params(axis="y", labelcolor="tab:orange")

    ax_f_add.invert_yaxis()
    ax_f_add.set_ylim(180, 0)
    ax_f.grid(axis="x", linestyle="dashed", alpha=0.5)

ax2.set_xlabel("Date / Year")
fig.tight_layout()
plt.subplots_adjust(hspace=0.2)
