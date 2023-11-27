# PlanetariumAppMetrics

## Steps to run the project:
1. Clone and config https://github.com/maria638fdez/PlanetariumAppMetrics.git![image](https://github.com/maria638fdez/PlanetariumAppMetrics/assets/38212450/f10ca992-e368-45b0-a6a7-9705d576b7c9)
   > git clone https://github.com/maria638fdez/PlanetariumAppMetrics
3. Run (Remember to install the needed libraries with pip install):
   > python app/app.py 
4. Open the app at port 5000

## Notes
This flask project is intended to run an app that is managed from the file app.py, in a VM with OSM installed locally.
### Execution 1: fields
index.html > enterNodes.html > enterTasks.html > imain.py (subprocess) > printValues.html
### Execution 2: from file
index.html > readFile.html > imain.py (subprocess) > printValues.html

Where imain executes in order these files:
- isetter.py
- ienergy.py
- isolver.py
- iprinter.py
