# Rent apartment finder in Helsinki

## Brief

A program for finding rent apartments in Helsinki. User can filter them by rent (€) per month, district(s), size in m^2, floor number, condition, if it has a balcony and the year of building.
The program can be run from the mainwindow.py file. Used PyQt without (Qt designer) for making the GUI. The web page used is Oikotie.fi

## Libraries used and running the program

PyQt5, requests and Python standard library (time, sys, webbrowser, random, json). PyQt5 can be installed e.g. from terminal with the command pip install pyqt5 and requests can be installed with command pip install requests.
After installing the needed libraries, the program should work and it starts by running the mainwindow.py file.

## Future plans

The program doesn't have any unittests at the moment, and I'm planning to implement them in the near future. Also the program works only with rent apartments in Helsinki. Most likely going to change this so it works in any city in Finland.
