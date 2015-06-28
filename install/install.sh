#Download lastest minibian, Win32DiskImager, putty
#Write minibian image to SD with Win32DiskImager
#Connect with putty (login : root  password : raspberry)

df -h
fdisk /dev/mmcblk0
#p
#d 2
#n p 2
#+2G
reboot
resize2fs /dev/mmcblk0p2

apt-get update
#Captive portal tools
apt-get install firmware-ralink hostapd dnsmasq -y
#python stuff
apt-get install git python python-pip build-essential python-dev -y
pip install flask tornado #qrcode pillow

#get MUSEAL
git clone https://github.com/nbergont/museal.git

#ETC conf
#cp -r etc/* /etc
#chmod 755 /etc/init.d/museal
#update-rc.d museal defaults 
