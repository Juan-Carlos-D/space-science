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

earth_state_wrt_sun = np.array(earth_state_wrt_sun)
earth_sun_distance = np.linalg.norm(earth_state_wrt_sun[:3])

earth_orb_speed_wrt_sun = np.linalg.norm(earth_state_wrt_sun[3:])

spiceypy.furnsh("../Kernels/pck/gm_de431.tpc.txt")
_, GM_SUN = spiceypy.bodvcd(bodyid=10, item="GM", maxn=1)

v_orb_func = lambda gm, r: np.sqrt(gm / r)
earth_orb_speed_wrt_sun_theory = v_orb_func(GM_SUN[0], earth_sun_distance)
