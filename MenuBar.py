#CM4105 Network Management Tool
#By Cameron Ross Birnie
#Student ID - 1805305

#This tool will allow a user to interact and configure network device using an intutitve and easy to use GUI




#Imports the require module from Kivy to esnure that the user is running the minimum required version of the software to operate the tool

import kivy
kivy.require('1.11.1')

#Import various Kivy modules

from kivy.uix.boxlayout import BoxLayout


#Creates the class that inherits from the BoxLayout class, this class provides the functions to swtich to screens as required

class MenuBar(BoxLayout):
    
    def ReturnToMainMenu(self, instance):
        self.main_menu_root.manager.current = 'MainMenuScreen'
    
    def SetStorageLocationButton(self, instance):
        self.main_menu_root.manager.current = 'SetStorageLocationScreen'

        