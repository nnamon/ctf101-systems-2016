#!/bin/bash

sysctl -w kernel.dmesg_restrict=1
mount -o remount,hidepid=2 /proc
chmod 700 /tmp /var/tmp /dev/shm

