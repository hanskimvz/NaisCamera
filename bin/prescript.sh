#!/bin/sh
#cron
if [ ! -d /var/spool ]; then
    mkdir /var/spool
fi

if [ ! -d /var/spool/cron ]; then
    mkdir /var/spool/cron
fi

if [ ! -d /var/spool/cron/crontabs ]; then
    mkdir /var/spool/cron/crontabs
fi

ES=`ps -ef |grep crond | grep -v grep | awk '{print $1}'`
# echo "$ES"
if [ ! "$ES" ] ;  then
    echo "Service Crond start" 
    /usr/sbin/crond
fi

# proc mode for temperature
echo enabled > /sys/class/thermal/thermal_zone0/mode

# passwd for root
yes pass | passwd root

# NTP
ntpdate  ntp.aliyun.com >/dev/null 2>&1 &
/app/dsp_log/dsp_log &
# i2ctransfer -f -y 0 w3@0x10 0x01 0x00 0x00

