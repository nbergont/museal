#Download lastest minibian, Win32DiskImager, putty
#Write minibian image to SD with Win32DiskImager
#Power rapsberry with new SD
#Connect with putty (login : root  password : raspberry)

apt-get update
#apt-get install git rpi-update

#usefull tools 
apt-get install nano raspi-config  -y

raspi-config
#reboot

#Captive portal tools
apt-get install firmware-ralink hostapd dnsmasq -y

#python stuff
apt-get install python python-pip -y
pip install flask tornado #tornado qrcode pillow

sudo apt-get install build-essential python-dev

#ETC conf
#cp -r etc/* /etc
#update-rc.d audiobox defaults 

#http://www.htpcguides.com/lightweight-raspbian-distro-minibian-initial-setup/
#http://lookingfora.name/2012/12/08/raspberry-pi-creer-un-point-dacces-wifi-avec-portail-captif/