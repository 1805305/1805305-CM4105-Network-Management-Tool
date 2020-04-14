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

class BasicConfMenuButtons(BoxLayout):

    def BasicConfHostnameButton(self, instance):
        self.main_menu_root.manager.current = 'BasicConfHostnameScreen'

    def BasicConfDomainButton(self, instance):
        self.main_menu_root.manager.current = 'BasicConfDomainScreen'

    def BasicConfReloadButton(self, instance):
        self.main_menu_root.manager.current = 'BasicConfReloadScreen'


class BasicConfHostnameLayout(GridLayout):
    pass

class BasicConfDomainLayout(GridLayout):
    pass

class BasicConfReloadLayout(GridLayout):
    pass

    
        
   