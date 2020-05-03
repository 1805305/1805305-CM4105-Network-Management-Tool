#CM4105 Network Management Tool
#By Cameron Ross Birnie
#Student ID - 1805305

#This tool will allow a user to interact and configure network device using an intutitve and easy to use GUI




#Imports the require module from Kivy to ensure that the user is running the minimum required version of the software to operate the tool

import kivy
kivy.require('1.11.1')

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen

from kivy.app import App

from kivy.properties import StringProperty

from os.path import dirname


class SetStorageLocation(Screen):        

    def SetStorageLocationChangeExecute(self):
        
        with open('StorageLocation.txt', 'r') as f:
            new_storage_location_file = f.readlines()
           
        new_storage_location_file[2] = self.ids._Set_Storage_Location_File_Chooser_.ids.FileChooser.path
        App.get_running_app().selected_storage_directory =  new_storage_location_file[2]

        f.close()

        with open('StorageLocation.txt', 'w') as f:
            f.writelines( new_storage_location_file )

        f.close()

        #.selection can be used to see the currently selected file, could be used for loading and displaying files within script i.e. self.ids._Set_Storage_Location_File_Chooser_.ids.FileChooser.selection
        
        #self.ids._Set_Storage_Location_Directory_Info_.ids.PotentialStorage.text = self.ids._Set_Storage_Location_File_Chooser_.ids.FileChooser.path
    
        

    def ResetStorageLocationChangeExecute(self):
        
        with open('StorageLocation.txt', 'r') as f:
            reset_storage_location_file = f.readlines()
           
        reset_storage_location_file[2] = dirname(__file__)


        with open('StorageLocation.txt', 'w') as f:
            f.writelines( reset_storage_location_file )
      
        App.get_running_app().selected_storage_directory =  reset_storage_location_file[2]


        f.close()