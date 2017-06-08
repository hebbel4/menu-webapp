# menu-webapp

This menu web app displays menus in database, and user can add new restaurants, edit restaurants' name, and delete a restaurant from the database.

**This project makes use of the Linux-based virtual machine (VM), you'll need VirtualBox, Vagrant installed in advance.**

## Start Guide:
* Put all files into a folder "restaurants" inside vagrant subdirectory
* From your terminal, inside the vagrant subdirectory, run the command vagrant up
* When vagrant up is finished running, run vagrant ssh to log in to your Linux VM
* Inside the VM, change directory to \vagrant (cd \vagrant), and then cd restaurants
* Download and run command python lotsofmenus.py to populate database with menus
* Run command python webserver.py
