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

class IntConfMenuButtons(BoxLayout):

    def IntConfAssignIPv4Button(self, instance):
        self.main_menu_root.manager.current = 'IntConfAssignIPv4Screen'

    def IntConfEthernetIntButton(self, instance):
        self.main_menu_root.manager.current = 'IntConfEthernetIntScreen'



class IntConfAssignIPv4(Screen):        
    pass

class IntConfEthernetInt(Screen):        
    pass


    
        
   