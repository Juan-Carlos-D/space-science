import datetime
import spiceypy
import numpy as np

spiceypy.furnsh("../Solar System Barycenter/kernel_meta.txt")
spiceypy.furnsh("../Kernels/pck/pck00010.tpc.txt")
spiceypy.furnsh("../Kernels/lsk/naif0012.tls.txt")
spiceypy.furnsh("../Kernels/spk/de432s.bsp")

init_time_utc = datetime.datetime(year=2000, month=1, day=1, hour=0, minute=0, second=0)
delta_days = 10000
end_time_utc = init_time_utc + datetime.timedelta(days=delta_days)

init_time_utc_str = init_time_utc.strftime("%Y-%m-%dT%H:%M:%S")
end_time_utc_str = end_time_utc.strftime("%Y-%m-%dT%H:%M:%S")

init_time_et = spiceypy.utc2et(init_time_utc_str)
end_time_et = spiceypy.utc2et(end_time_utc_str)

ssb_wrt_sun_position = []

time_interval_et = np.linspace(init_time_et, end_time_et, delta_days)

for time_interval_et_f in time_interval_et:
    _position, _ = spiceypy.spkgps(targ=0, et=time_interval_et_f, ref="ECLIPJ2000", obs=10)
    
    ssb_wrt_sun_position.append(_position)

ssb_wrt_sun_position = np.array(ssb_wrt_sun_position)

_, radii_sun = spiceypy.bodvcd(bodyid=10, item="RADII", maxn=3)