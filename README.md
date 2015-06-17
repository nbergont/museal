# MUSELA
![Logo](https://raw.githubusercontent.com/nbergont/musela/master/icon.png)

## What is MUSELA ?
MUSELA mean MUSEum Lowcost Audioguide.<br>
Raspberry Pi is used to serve audio files over Wifi (with hotspot captive portal).<br>
Visitor are able to use their smartphone to :
- Connect to wifi hotspot (open network)
- Open web browser and open or reload any web adress (all url are redirected)
- Select audio media and listen

## What do you need ?
- Raspberry Pi 1 or 2 (with alim & case)
- Hostspot compatible wifi USB dongle (http://elinux.org/RPI-Wireless-Hotspot)
- SD card (4Go minimum)
- Total cost : ~80$

## How to use it ?
- Easy way :
 - Download complete system image : TODO
 - Write on SD card (use http://sourceforge.net/projects/win32diskimager/)
 - Boot up Raspberry Pi and connect your smarphone to "MUSELA" Wifi hotspot
 - Open web browser and open or reload any web adress
 - Go to "/admin" page (defaut login : "admin" , defaut password : "admin")
 - Configure your options (don't forget to change login & password)
 - Add new section & audio media
 - Logout & your device is ready !
 
- Hardest way (for advanced users):
 - Download MINIBIAN Raspberry Pi image : https://minibianpi.wordpress.com/
 - Install on SD card
 - Configure system & wifi (TODO)
 - ...

## Third party application/library used ?
- Python Flask (http://flask.pocoo.org/) : for web server
- BootStrap (http://getbootstrap.com/) : for front-end framework
- mediaelement (http://mediaelementjs.com/) : for play audio file
- MINIBIAN (https://minibianpi.wordpress.com/) : for Raspberry operating system

## TODO list :
- [x] Web application to list & play media (for users)
- [x] Web admin for managing media & options
- [x] Wifi hostname change
- [ ] Complete system image for beginner
- [ ] Check if complete system image work on Raspberry 2 (it should work)
- [ ] QRcode functions (Visitor scan QRcode to obtain media)
- [ ] Customisation (theme, colors ...)
- [ ] Add picture or video media
