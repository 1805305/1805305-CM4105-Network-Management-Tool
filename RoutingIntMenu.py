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

from netmiko import ConnectHandler  

class RoutingIntMenuButtons(BoxLayout):

    def RoutingIntStaticRouteButton(self, instance):
        self.main_menu_root.manager.current = 'RoutingIntStaticRouteScreen'

    def RoutingIntDefaultRouteButton(self, instance):
        self.main_menu_root.manager.current = 'RoutingIntDefaultRouteScreen'

    def RoutingIntDefaultGatewayButton(self, instance):
        self.main_menu_root.manager.current = 'RoutingIntDefaultGatewayScreen'


class RoutingIntStaticRoute(Screen):        
    
    def RoutingIntStaticRouteExecute(self):

        destination_address = self.ids._Routing_Int_Static_Route_Layout_.ids.RoutingIntStaticRouteIPRouteLayout.ids.IPv4AddressTextInput.text + ' ' +  self.ids._Routing_Int_Static_Route_Layout_.ids.RoutingIntStaticRouteIPRouteLayout.ids.SubnetMaskSpinnerLayout.ids.SubnetMaskSpinner.text
        distance_metric = self.ids._Routing_Int_Static_Route_Layout_.ids.RoutingIntStaticRouteMetricDistanceLayout.ids.MetricDistanceTextInput.text

        if self.ids._Routing_Int_Static_Route_Layout_.ids.RoutingIntStaticRouteForwardIPLayout.ids.IPv4AddressTextInput.text == '':
            route_egress = self.ids._Routing_Int_Static_Route_Layout_.ids.RoutingIntStaticRouteForwardInterfaceLayout.ids.InterfaceTypeSpinnerLayout.ids.InterfaceTypeSpinner.text + ' ' +  self.ids._Routing_Int_Static_Route_Layout_.ids.RoutingIntStaticRouteForwardInterfaceLayout.ids.InterfaceNumberTextInput.text
        else:
            route_egress = self.ids._Routing_Int_Static_Route_Layout_.ids.RoutingIntStaticRouteForwardIPLayout.ids.IPv4AddressTextInput.text


        device_ip_address = self.ids._IPv4_Target_Device_Layout_.ids.IPv4AddressTextInput.text


        device = { 
          'device_type': 'cisco_ios', 
          'ip': device_ip_address, 
          'username': 'Test', 
          'password': 'cisco123', 
          } 


        config_commands = ["ip route " + destination_address + ' ' + route_egress + ' ' + distance_metric]

        net_connect = ConnectHandler(**device) 

        output = net_connect.send_config_set(config_commands)

        print(output)

class RoutingIntDefaultRoute(Screen):        
    
    def RoutingIntDefaultRouteExecute(self):

        distance_metric = self.ids._Routing_Int_Default_Route_Layout_.ids.RoutingIntDefaultRouteMetricDistanceLayout.ids.MetricDistanceTextInput.text

        if self.ids._Routing_Int_Default_Route_Layout_.ids.RoutingIntDefaultRouteForwardIPLayout.ids.IPv4AddressTextInput.text == '':
            route_egress = self.ids._Routing_Int_Default_Route_Layout_.ids.RoutingIntDefaultRouteForwardInterfaceLayout.ids.InterfaceTypeSpinnerLayout.ids.InterfaceTypeSpinner.text + ' ' +  self.ids._Routing_Int_Default_Route_Layout_.ids.RoutingIntDefaultRouteForwardInterfaceLayout.ids.InterfaceNumberTextInput.text
        else:
            route_egress = self.ids._Routing_Int_Default_Route_Layout_.ids.RoutingIntDefaultRouteForwardIPLayout.ids.IPv4AddressTextInput.text


        device_ip_address = self.ids._IPv4_Target_Device_Layout_.ids.IPv4AddressTextInput.text

        device = { 
          'device_type': 'cisco_ios', 
          'ip': device_ip_address, 
          'username': 'Test', 
          'password': 'cisco123', 
          } 


        config_commands = ["ip route 0.0.0.0 0.0.0.0 " + route_egress + ' ' + distance_metric]

        net_connect = ConnectHandler(**device) 

        output = net_connect.send_config_set(config_commands)

        print(output)

class RoutingIntDefaultGateway(Screen):        
    
    def RoutingIntDefaultGatewayExecute(self):
        
        default_gateway = self.ids._Routing_Int_Default_Gateway_Layout_.ids.IPv4AddressTextInput.text

        device_ip_address = self.ids._IPv4_Target_Device_Layout_.ids.IPv4AddressTextInput.text

        device = { 
          'device_type': 'cisco_ios', 
          'ip': device_ip_address, 
          'username': 'Test', 
          'password': 'cisco123', 
          } 


        config_commands = ["ip default-gateway " + default_gateway]

        net_connect = ConnectHandler(**device) 

        net_connect.send_config_set(config_commands)

        print(output)

    
        
   