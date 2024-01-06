import os, time, sys
import re


#Temperature
# echo enabled > /sys/class/thermal/thermal_zone0/mode
# temp=$(cat /sys/class/thermal/thermal_zone0/temp)

with open ("/sys/class/thermal/thermal_zone0/mode", "r") as f:
    body = f.read()
if body != "enabled":
    with open ("/sys/class/thermal/thermal_zone0/mode", "w") as f:
        body = f.write("enabled")

with open ("/sys/class/thermal/thermal_zone0/temp", "r") as f:
    body = f.read()
    temp = "%.2f" %(int(body)/1000)


# Resource
regexcpu = re.compile("(\d+.\d+)%\s+idle", re.IGNORECASE)
regexmem = re.compile("(\d+)(\w)\s+used, (\d+)(\w)\s+free", re.IGNORECASE) 

res =  os.popen("top -bn1")
body = res.read()
x = regexcpu.search(body)
idle = x.group(1)
cpu = ("%.2f" %(100-float(idle)))
x = regexmem.search(body)
m_used = int(x.group(1))
m_free = int(x.group(3))
# if x.group(2) == 'K':
#     m_used *=1024
# elif x.group(2) == 'M':
#     m_used *=1024*1024
# if x.group(4) == 'K':
#     m_free *=1024
# elif x.group(4) == 'M':
#     m_free *=1024*1024

m_total = m_used + m_free


# uptime
uptime = 0
res =  os.popen("uptime")
body = res.read()
# print (body)
m = re.search("up\s+(\d+)\s+day", body)
if m:
    uptime += int(m.group(1))*3600*24

m = re.search("(\d+):(\d+),", body)
if m:
    uptime += int(m.group(1)) * 3600
    uptime += int(m.group(2)) * 60

print ("CPU:", cpu)
print ("MEM: %dK/%dK" %(m_used, m_total))
print ("TEMP:", temp)
print ("UPTIME:", uptime)
print ("UPTIME:%d day %d hour %d min" %((uptime//(3600*24)), (uptime%(3600*24))//3600, (uptime%(3600))//60 ))



