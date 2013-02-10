import time, datetime
ti = time.localtime()
t = datetime.time(ti.tm_hour, ti.tm_min , ti.tm_sec)
print t