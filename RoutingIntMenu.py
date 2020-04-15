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

class RoutingIntMenuButtons(BoxLayout):

    def RoutingIntStaticRouteButton(self, instance):
        self.main_menu_root.manager.current = 'RoutingIntStaticRouteScreen'

    def RoutingIntDefaultRouteButton(self, instance):
        self.main_menu_root.manager.current = 'RoutingIntDefaultRouteScreen'

    def RoutingIntDefaultGatewayButton(self, instance):
        self.main_menu_root.manager.current = 'RoutingIntDefaultGatewayScreen'


class RoutingIntStaticRouteLayout(GridLayout):
    pass

class RoutingIntDefaultRouteLayout(GridLayout):
    pass

class RoutingIntDefaultGatewayLayout(GridLayout):
    pass

    
        
   