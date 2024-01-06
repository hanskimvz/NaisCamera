#!/bin/sh
# /etc/init.d/rc.sysinit
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin

/bin/echo "Sysinit starting"
/bin/mount -t proc none /proc

bootddev=$(cat /proc/cmdline  | sed  -n  "s#root=\(\/dev\/mmcblk[0-9]\).*#\1#p" )
rootpart=$(cat /proc/cmdline  | sed  -n  "s/root=\/dev\/mmcblk[0-9]\p\([0-9]\).*/\1/p" )
datapart=$(($rootpart+1))
if ! ` cat /proc/cmdline  |  grep -E "ubifs|nfs" >/dev/null ` ; then
	mount -o remount,ro rootfs /
	fsck.ext2 -p "${bootddev}p${rootpart}"
	fsck -p "${bootddev}p${datapart}" >/dev/null 2>&1	
fi

mount -o remount,rw rootfs /
mount -t tmpfs  tmpfs /run -o mode=0755,nosuid,nodev
/bin/mount -t sysfs none /sys
/bin/hostname -F /etc/hostname
/sbin/syslogd
/sbin/klogd

/etc/init.d/S21rngd start

# /sbin/ifconfig eth0 down
# if [ -f /etc/mac_addr_file ]; then
#     mac=$(cat /etc/mac_addr_file)
# else
#     mac=$(ifconfig eth0 | sed -n "/HWaddr/s/.*HWaddr \(.*\)/\1/p")
#     echo "${mac}">/etc/mac_addr_file
# fi
# /sbin/ifconfig eth0 hw ether ${mac}
# /sbin/ifconfig eth0 up
# udhcpc -b  -i eth0  &
# /sbin/ifup eth0

mkdir /dev/pts
mount -t devpts devpts /dev/pts

for var in 1 2 3 4 5 6 7 8 9 
do
    ifconfig
    cd /
    find . -name libdbus-1.so.3
    sleep 1
done

if [ -d /home/bin ]; then
    cd /home/bin
    sh prescript.sh
fi


# Start Service
/etc/init.d/S30dbus start
/etc/init.d/S49php-fpm start
/etc/init.d/S50nginx start
/etc/init.d/S50sshd start
/etc/init.d/S50avahi-daemon start

if [ -d /home/bin ]; then
    cd /home/bin
    sh postscript.sh
fi