import os
from datetime import datetime, timedelta, date, time
import numpy as np
import time

data = [line_catalog.rstrip('\n') for line_catalog in open("STATION0.HYP")]

f= open("dict_sta.dat","w+")

for line in data:
	sta_name = line[0:6].strip()
	sta_lat  = line[6:13].strip()
	sta_lat = -1.0*(float(sta_lat[0:2])+float(sta_lat[2:])/60.0)
	sta_lon  = line[15:22].strip()
	sta_lon = -1.0*(float(sta_lon[0:2])+float(sta_lon[2:])/60.0)
	sta_prof = line[23:27].strip()
	f.write( "%s, %.6f %.6f %s \n" %(sta_name,sta_lat,sta_lon,sta_prof) )


f.close()
