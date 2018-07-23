#!/bin/sh
sn=`sudo cat /sys/block/mmcblk0/device/cid |cut -c19-26`
sudo cat > "/etc/hostapd/hostapd.conf" <<EOF
interface=wlan0
driver=nl80211
ssid=HF_AP_${sn}
hw_mode=g
channel=6
wmm_enabled=1
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=123456788
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
EOF

sleep 2s

#sudo service hostapd start
hostapd -d /etc/hostapd/hostapd.conf
