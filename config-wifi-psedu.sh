# https://www.raspberrypi.org/forums/viewtopic.php?p=462982
wget https://dl.dropboxusercontent.com/u/80256631/8188eu-v7-20150406.tar.gz
tar xzf 8188eu-v7-20150406.tar.gz
./install.sh
sudo reboot
# test
lsmod
lsusb
ifconfig -a
# modify wlan0
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
>>>BEGIN>>>
# ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
# update_config=1
ctrl_interface=/var/run/wpa_supplicant
ctrl_interface_group=0
network={
ssid=""
proto=WPA2
key_mgmt=WPA-PSK
pairwise=TKIP
group=TKIP
psk=""
}
>>>END>>>

#dynamic wlan0
sudo nano /etc/network/interfaces
>>>BEGIN>>>
auto lo
iface lo inet loopback

auto eth0
allow-hotplug eth0
iface eth0 inet static
address 192.168.137.254
netmask 255.255.255.0
gateway 192.168.137.1
dns-nameservers 8.8.8.8

auto wlan0
allow-hotplug wlan0
iface wlan0 inet dhcp
wpa-ssid "nubia"
wpa-psk "501501501"

auto wlan1
allow-hotplug wlan1
iface wlan1 inet manual
wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
>>>END>>>
# restart network
sudo /etc/init.d/networking restart
