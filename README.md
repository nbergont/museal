# AudioBox
![Logo](https://raw.githubusercontent.com/nbergont/audiobox/master/icon.png)

## What is AudioBox ?
This is a Raspberry Pi projet for lowcost wifi audioguide (for museum).<br>
Visitor use their smartphone to :
- Connect to AudioBox wifi hotspot (open network)
- Open web browser and open or reload any page
- Select media and listen

## What do you need ?
- Raspberry Pi
- Hostspot compatible wifi USB dongle (http://elinux.org/RPI-Wireless-Hotspot)
- SD card (4Go)

## How to use it ?
- Easy way :
 - Download complete system image : TODO
 - Write on SD card (use http://sourceforge.net/projects/win32diskimager/)
 - Boot up Raspberry Pi and connect to AudioBox Wifi hotspot
 - Go to "/admin" page (login : admin , password : admin)
 - Configure options (don't forget to change password & login)
 - Add new section & media
 
- Hardest way :
 - Download MINIBIAN Raspberry Pi image : https://minibianpi.wordpress.com/
 - Install on SD card
 - Configure system & wifi (TODO)
 - ...

## Third party application/library used ?
- Python Flask (http://flask.pocoo.org/)
- BootStrap (http://getbootstrap.com/)
- MINIBIAN (https://minibianpi.wordpress.com/)

## TODO list :
- [x] Web application to list & play media (for users)
- [x] Web admin for managing media & options
- [ ] Complete system image for beginner
- [ ] Automatic system configuration script
- [ ] Wifi hostname change
- [ ] QRcode functions (Visitor scan QRcode to obtain media)
- [ ] Customisation (theme, colors ...)
