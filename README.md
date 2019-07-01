# Cura_Marlin_AutoTemp
a postprocessing script for cura to use the Marlin AutoTemp Feature

put this script to your Cura scripts folder, like:
"C:\Users\USERNAME\AppData\Roaming\cura\4.1\scripts"
and restart Cura.

then you can add this script as a postprocessing script in Cura.
you can change the max Temperature and the factor, how strong this works.


* Automatic Temperature:
 * The hotend target temperature is calculated by all the buffered lines of gcode.
 * The maximum buffered steps/sec of the extruder motor is called "se".
 * Start autotemp mode with M109 S<mintemp> B<maxtemp> F<factor>
 * The target temperature is set to mintemp+factor*se[steps/sec] and is limited by
 * mintemp and maxtemp. Turn this off by executing M109 without F*
 * Also, if the temperature is set to a value below mintemp, it will not be changed by autotemp.
 * On an Ultimaker, some initial testing worked with M109 S215 B260 F1 in the start.gcode
