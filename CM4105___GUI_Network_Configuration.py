#CM4105 Network Management Tool
#By Cameron Ross Birnie
#Student ID - 1805305

#This tool will allow a user to interact and configure network device using an intutitve and easy to use GUI



#Imports the require module from Kivy to esnure that the user is running the minimum required version of the software to operate the tool

from kivy import require
require('1.11.1')


#Imports basic modules of Kivy to allow for Kivy to be used within Python

from kivy.app import App
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

from kivy.uix.popup import Popup
from kivy.uix.label import Label

from kivy.properties import ListProperty, StringProperty

#from os.path import dirname


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



    current_screen = StringProperty('Main Menu')
    previous_screen = ListProperty(['MainMenuScreen'])


    #current_directory = StringProperty('')
    selected_storage_directory = StringProperty('') # Instead maybe have the open file and search file for location as a module that can be quickly ran from any function, this would stop the need for a global property

    

    def build(self):
        self.title = 'CM4105 Network Management Tool - 1805305' #Set the title for the application window

        #curdir = dirname(__file__)
        #self.current_directory = curdir

        with open('StorageLocation.txt') as f:
            storage_location_file = f.readlines()
            self.selected_storage_directory = storage_location_file[2]
            f.close()

        return MenuManager()

    def GoPreviousScreen(self, **kwargs):
        previous = self.previous_screen
        if len(previous) == 1:
            print('empty')
            return
        if previous:
            screen = previous.pop()
            print(screen)
            #self.root.ids._Menu_Manager_.current = str(screen)
            
class MenuManager(ScreenManager):
    pass





#If statement to run the execute the MainApplicationApp if this script is run as the main script, this allows for functions from this script to increase modularity

if __name__ == '__main__':
    MainApplicationApp().run()