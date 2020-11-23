#!/usr/bin/sh

# Optimize your sound system.

echo -n performance|tee /sys/devices/system/cpu/cpufreq/policy*/scaling_governor

echo 3072 > /sys/class/rtc/rtc0/max_user_freq
echo 3072 > /proc/sys/dev/hpet/max_user_freq
