# Cura PostProcessingPlugin
# Author:   Christian Köhlke
# Date:     July 03, 2019
#
# A Cura postprocessing script to use the Marlin AutoTemp Feature.
#
# Put this script inside your Cura scripts folder, e. g.: "C:\Users\USERNAME\AppData\Roaming\cura\4.1\scripts" and restart Cura.
# Then you can apply this script as a postprocessing script in Cura. You can change the max. Temperature and the factor, to specify how strong the effect will be.
# You can choose to deactivate this script for the last layer, to prevent the AutoTemp Feature to be active after finishing printing. Then the function will be 
# deactivated, when the temperature is set to zero after the print finished.
#
# Automatic Temperature:
# 
# The hotend target temperature is calculated by all the buffered lines of gcode. The maximum buffered steps/sec of the extruder motor is called "se".
# Start autotemp mode with M109 S B F The target temperature is set to mintemp+factorse[steps/sec] and is limited by mintemp and maxtemp.
# Turn this off by executing M109 without F. Also, if the temperature is set to a value below mintemp, it will not be changed by autotemp.
# On an Ultimaker, some initial testing worked with M109 S215 B260 F1 in the start.gcode
#
#
# How it works
#
# This script searches for M104 and M109 in the G-Code and adds an B... F... (like B245 F1) after the normal S temperature.
#
# M104 is to set the hotend temperature without waiting for it
# M109 sets the hotend temperature and waits, untils the temperature is reached

from ..Script import Script
from UM.Application import Application

class Autotemp(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name": "Autotemp",
            "key": "Autotemp",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "active":
                {
                    "label": "activate Autotemp",
                    "description": "When enabled, marlin uses autotemp.",
                    "type": "bool",
                    "default_value": true
                },
		"activeinlastlayer":
                {
                    "label": "activate Autotemp in last Layer",
                    "description": "When enabled, the AutoTemp function is also used in the last layer. Then it is also active after the print and you will probably have problem switching the temperature manually.",
                    "type": "bool",
                    "default_value": false
                },
                "maxtemperature":
                {
                    "label": "max Temperature",
                    "description": "the maximum Temperature for the Autotemp function",
                    "type": "int",
                    "default_value": 245,
                    "minimum_value": 100,
                    "maximum_value": 300,
                    "minimum_value_warning": 150,
                    "maximum_value_warning": 250
                },
                "factor":
                {
                    "label": "Factor",
                    "description": "the factor, how much the autotemp function takes effect",
                    "type": "float",
                    "default_value": 1,
                    "minimum_value": 0,
                    "maximum_value": 10,
                    "minimum_value_warning": 0,
                    "maximum_value_warning": 10
                }
            }
        }"""

    def execute(self, data):
        active = self.getSettingValueByKey("active")
        activeinlastlayer = self.getSettingValueByKey("activeinlastlayer")
        maxtemperature = self.getSettingValueByKey("maxtemperature")
        factor = self.getSettingValueByKey("factor")

        if active:
            for layer in data:

		lay_idx = data.index(layer)
                lines = layer.split("\n")
                
                if activeinlastlayer or lay_idx+1 < len(data):
                    
                    for line in lines:
                        if line.startswith("M104") or line.startswith("M109"):
                            lin_idx = lines.index(line)
                            
                            # Start autotemp mode with M109 S<mintemp> B<maxtemp> F<factor>
                            linepart = line.split(";",1)
                            replace_line = "%s B %s F %s ;inserted Autotemp function" % (linepart[0], maxtemperature, factor)
                            if len(linepart) > 1:
                                replace_line += linepart[1]
                            lines.insert(lin_idx, replace_line)
                            lines.remove(line)

                result = "\n".join(lines)
                data[lay_idx] = result

        return data
