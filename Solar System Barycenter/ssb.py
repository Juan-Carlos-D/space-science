import datetime
import spiceypy
import numpy as np

spiceypy.furnsh("../Solar System Barycenter/kernel_meta.txt")

init_time_utc = datetime.datetime(year=2000, month=1, day=1, hour=0, minute=0, second=0)
delta_days = 10000
end_time_utc = init_time_utc + datetime.timedelta(days=delta_days)

init_time_utc_str = init_time_utc.strftime("%Y-%m-%dT%H:%M:%S")
end_time_utc_str = end_time_utc.strftime("%Y-%m-%dT%H:%M:%S")
