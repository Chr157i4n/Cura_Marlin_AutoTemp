# Cura PostProcessingPlugin
# Author:   Christian Köhlke
# Date:     July 01, 2019

# Description:  this postprocessing-script can be used in cura to enable the AutoTemp function of Marlin


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
                    "description": "the factor, how much the autotemp function ",
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
        maxtemperature = self.getSettingValueByKey("maxtemperature")
        factor = self.getSettingValueByKey("factor")

  

        if active:
            for layer in data:


                
                lay_idx = data.index(layer)
                lines = layer.split("\n")
            
                for line in lines:
                    if line.startswith("M104"):
                        lin_idx = lines.index(line)
                        
                        # Start autotemp mode with M109 S<mintemp> B<maxtemp> F<factor>
                        replace_line = line + " B" + str(maxtemperature) + " F" + str(factor) + " ;inserted Autotemp function"
                        lines.insert(lin_idx,replace_line)
                        lines.remove(line)

                result = "\n".join(lines)
                data[lay_idx] = result

            
        return data
