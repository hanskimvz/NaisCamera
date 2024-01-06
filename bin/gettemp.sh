echo enabled > /sys/class/thermal/thermal_zone0/mode
temp=$(cat /sys/class/thermal/thermal_zone0/temp)

res=$(top -bn1)


echo "Temperature:${temp}"

echo "Memory:${res}"