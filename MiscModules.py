#CM4105 Network Management Tool
#By Cameron Ross Birnie
#Student ID - 1805305

#This tool will allow a user to interact and configure network device using an intutitve and easy to use GUI




#Imports the require module from Kivy to ensure that the user is running the minimum required version of the software to operate the tool

import kivy
kivy.require('1.11.1')

#Import various Kivy modules

from kivy.uix.popup import Popup

from kivy.properties import ObjectProperty


#Creates the class that inherits from the Popup class, this class provides the base for the Device Credential Popup

class DeviceUsernameAndPasswordPopup(Popup):
    load = ObjectProperty() #Sets load as an object property



