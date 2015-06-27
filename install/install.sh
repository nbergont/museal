#Download lastest minibian, Win32DiskImager, putty
#Write minibian image to SD with Win32DiskImager
#Power rapsberry with new SD
#Connect with putty (login : root  password : raspberry)

apt-get update

#usefull tools 
apt-get install nano raspi-config rpi-update git -y

raspi-config
#Expand filesystem
reboot

#Captive portal tools
apt-get install firmware-ralink hostapd dnsmasq -y

#python stuff
apt-get install python python-pip build-essential python-dev -y
pip install flask tornado #qrcode pillow

#ETC conf
#cp -r etc/* /etc
#update-rc.d museal defaults 
