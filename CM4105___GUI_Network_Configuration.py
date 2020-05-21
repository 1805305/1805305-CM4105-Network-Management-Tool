#CM4105 Network Management Tool
#By Cameron Ross Birnie
#Student ID - 1805305

#This tool will allow a user to interact and configure network device using an intutitve and easy to use GUI


#This file is the main body of the script that will be used to start the tool



#Imports the required module from Kivy to esnure that the user is running the minimum required version of the software to operate the tool

from kivy import require
require('1.11.1')


#Import various Kivy modules

from kivy.app import App
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

from kivy.uix.popup import Popup
from kivy.uix.label import Label

from kivy.properties import ListProperty, StringProperty



#The following instructions loads the Kivy files that contain instructions for how the GUI is structured

#Loads the Kivy file to control the different screens
Builder.load_file('MenuManager.kv')

#Loads the Kivy file for the menu bar
Builder.load_file('MenuBar.kv')

#Loads the Kivy file for the Main Menu
Builder.load_file('MainMenu.kv')

#Loads the Kivy files for the SubMenus

Builder.load_file('Menus\BasicConfMenu.kv')
Builder.load_file('Menus\IntConfMenu.kv')
Builder.load_file('Menus\RoutingIntMenu.kv')
Builder.load_file('Menus\SecurityConfMenu.kv')
Builder.load_file('Menus\\NetMonAndManageMenu.kv')
Builder.load_file('Menus\DeviceInfoAndChangeControlMenu.kv')
Builder.load_file('Menus\\NetScanningAndTrafficMonMenu.kv')
Builder.load_file('Menus\\NetTestingMenu.kv')
Builder.load_file('Menus\SetStorageLocation.kv')


#Creates the main class for the script that will create the window

class MainApplicationApp(App):


    #Intialise various global properties that can be accessed by any of the python files

    current_screen = StringProperty('Main Menu')
    previous_screen = ListProperty(['MainMenuScreen'])

    selected_storage_directory = StringProperty('')

    device_username = StringProperty()
    device_password = StringProperty()

   
    #This functions builds the application and returns the menu manager that dictates which secreen to load first

    def build(self):
        self.title = 'CM4105 Network Management Tool - 1805305' #Set the title for the application window

        #Opens the StorageLocation.txt to see what the current desired storage location is and sets the global property as the this location so that other functions can find quickly find the directory to store outputs 
        with open('StorageLocation.txt') as f:
            storage_location_file = f.readlines()
            self.selected_storage_directory = storage_location_file[2]
            f.close()

        return MenuManager() 

         
#Creates the MenuManager class that inherits from ScreenManager, this class will control the switching of screens
    
class MenuManager(ScreenManager):
    pass





#If statement to execute the MainApplicationApp if this script is run as the main script, this allows for functions from this script to be imported to other scripts allowing for code reuse

if __name__ == '__main__':
    MainApplicationApp().run()