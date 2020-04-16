#CM4105 Network Management Tool
#By Cameron Ross Birnie
#Student ID - 1805305

#This tool will allow a user to interact and configure network device using an intutitve and easy to use GUI




#Imports the require module from Kivy to ensure that the user is running the minimum required version of the software to operate the tool

import kivy
kivy.require('1.11.1')

from kivy.uix.boxlayout import BoxLayout

class MainMenuButtons(BoxLayout):
    

    def BasicConfMenuButton(self, instance):
        self.main_menu_root.manager.current = 'BasicConfMenuScreen'

    def IntConfMenuButton(self, instance):
        self.main_menu_root.manager.current = 'IntConfMenuScreen'

    def RoutingIntMenuButton(self, instance):
        self.main_menu_root.manager.current = 'RoutingIntMenuScreen'

    def SecurityConfMenuButton(self, instance):
        self.main_menu_root.manager.current = 'SecurityConfMenuScreen'

    def NetMonMenuButton(self, instance):
        self.main_menu_root.manager.current = 'NetMonMenuScreen'

    def DeviceInfoMenuButton(self, instance):
        self.main_menu_root.manager.current = 'DeviceInfoMenuScreen'

    def NetScanMenuButton(self, instance):
        self.main_menu_root.manager.current = 'NetScanMenuScreen'

    def NetTestingMenuButton(self, instance):
        self.main_menu_root.manager.current = 'NetTestingMenuScreen'
    
    def SetStorageLocationButton(self, instance):
        self.main_menu_root.manager.current = 'SetStorageLocationScreen'
        
        
    