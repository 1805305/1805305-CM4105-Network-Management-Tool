#CM4105 Network Management Tool
#By Cameron Ross Birnie
#Student ID - 1805305

#This tool will allow a user to interact and configure network device using an intutitve and easy to use GUI




#Imports the require module from Kivy to ensure that the user is running the minimum required version of the software to operate the tool

import kivy
kivy.require('1.11.1')

#Import various Kivy modules

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen

from kivy.app import App

from kivy.properties import StringProperty

#Common modules will be imported to perform certain tasks if neccessary

import os
import sys

#Import OS path to allow for access to system functions

from os.path import dirname


#Create the class for the 'Set Storage Location' Screen using the Screen class for inheritiance

class SetStorageLocation(Screen):        


    #Functions handles changing the desired storage location to the location set by the user

    def SetStorageLocationChangeExecute(self):
        
        with open(os.path.join(sys.path[0], 'StorageLocation.txt'), 'r') as f: #Open the storage location text file in read mode
            new_storage_location_file = f.readlines() #Read each line and store as a list
           
        new_storage_location_file[2] = self.ids._Set_Storage_Location_File_Chooser_.ids.FileChooser.path #Sets index 2 of the list as the file path selected by the user
       
        f.close() #Close the file


        with open(os.path.join(sys.path[0], 'StorageLocation.txt'), 'w') as f: #Open the storage location text file in write mode
            f.writelines( new_storage_location_file ) #Write the new list to the file

        f.close() #Close the file

        App.get_running_app().selected_storage_directory =  new_storage_location_file[2] #Set the global property 'selected_storage_directory' as the new file path
    


    #Function to reset the selected storage location to the location that the tool itself is stored in

    def ResetStorageLocationChangeExecute(self):
        
        with open(os.path.join(sys.path[0], 'StorageLocation.txt'), 'r') as f: #Open the storage location text file in read mode
            reset_storage_location_file = f.readlines() #Read each line and store as a list
           
        reset_storage_location_file[2] = dirname(__file__)  #Sets index 2 of the list as the directory of the tool

        f.close() #Close the file


        with open(os.path.join(sys.path[0], 'StorageLocation.txt'), 'w') as f: #Open the storage location text file in write mode
            f.writelines( reset_storage_location_file ) #Write the new list to the file
        
        f.close() #Close the file

        App.get_running_app().selected_storage_directory =  reset_storage_location_file[2]  #Set the global property 'selected_storage_directory' as the new file path


        f.close()