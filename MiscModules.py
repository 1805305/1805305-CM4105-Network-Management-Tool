#CM4105 Network Management Tool
#By Cameron Ross Birnie
#Student ID - 1805305

#This tool will allow a user to interact and configure network device using an intutitve and easy to use GUI




#Imports the require module from Kivy to ensure that the user is running the minimum required version of the software to operate the tool

import kivy
kivy.require('1.11.1')





from kivy.uix.popup import Popup

from kivy.properties import ObjectProperty



class DeviceUsernameAndPasswordPopup(Popup):
    load = ObjectProperty()



