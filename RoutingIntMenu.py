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

from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.uix.label import Label 
 

#Imports ConnectHandler from netmiko to handle SSH connections with devices

from netmiko import ConnectHandler  

#Imports two execption types to allow for better error handling

from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import AuthenticationException

#Imports ipaddress to provide the ability to maniuplate IP addresses

import ipaddress

#Imports DeviceUsernameAndPasswordPopup from the tool itself to allow for the device credentials to be entered

from MiscModules import DeviceUsernameAndPasswordPopup


#Creates the class that inherits from the BoxLayout class, this class provides the functions to swtich to screens as required

class RoutingIntMenuButtons(BoxLayout):

    def RoutingIntStaticRouteButton(self, instance):
        self.main_menu_root.manager.current = 'RoutingIntStaticRouteScreen'

    def RoutingIntDefaultRouteButton(self, instance):
        self.main_menu_root.manager.current = 'RoutingIntDefaultRouteScreen'

    def RoutingIntDefaultGatewayButton(self, instance):
        self.main_menu_root.manager.current = 'RoutingIntDefaultGatewayScreen'



#Create the class for the 'Set Static Route' Screen using the Screen class for inheritiance

class RoutingIntStaticRoute(Screen):       
    
    #Function to configure a static route on a device
    
    def RoutingIntStaticRouteExecute(self):

        #Try statement to ensure that any errors connecting and configuring the device are handled gracefully and the user is informed of what the potential error was using popups
        try:

            destination_address = self.ids._Routing_Int_Static_Route_Layout_.ids.RoutingIntStaticRouteIPRouteLayout.ids.IPv4AddressTextInput.text + ' ' +  self.ids._Routing_Int_Static_Route_Layout_.ids.RoutingIntStaticRouteIPRouteLayout.ids.SubnetMaskSpinnerLayout.ids.SubnetMaskSpinner.text
            distance_metric = self.ids._Routing_Int_Static_Route_Layout_.ids.RoutingIntStaticRouteMetricDistanceLayout.ids.MetricDistanceTextInput.text

            if self.ids._Routing_Int_Static_Route_Layout_.ids.RoutingIntStaticRouteForwardIPLayout.ids.IPv4AddressTextInput.text == '':
                route_egress = self.ids._Routing_Int_Static_Route_Layout_.ids.RoutingIntStaticRouteForwardInterfaceLayout.ids.InterfaceTypeSpinnerLayout.ids.InterfaceTypeSpinner.text + ' ' +  self.ids._Routing_Int_Static_Route_Layout_.ids.RoutingIntStaticRouteForwardInterfaceLayout.ids.InterfaceNumberTextInput.text
            else:
                route_egress = self.ids._Routing_Int_Static_Route_Layout_.ids.RoutingIntStaticRouteForwardIPLayout.ids.IPv4AddressTextInput.text


            #Try statement to ensure the IP address entered is valid. If it is an invalid address the ipaddress module will raise a value error, at which point the user is informed that a valid IP address is required using a popup
            try:

                device_ip_address = self.ids._IPv4_Target_Device_Layout_.ids.IPv4AddressTextInput.text
                ipaddress.ip_address(device_ip_address)

            #ipaddress raises a value error when an invalid IP address is used
            except ValueError:

                Factory.InvalidIPAddressPopup().open() 
                return #Exit from the function


            #If statement to ensure user has entered a username or password
            if App.get_running_app().device_username == '' or App.get_running_app().device_password == '':

                Factory.NoUserOrPassPopup().open() 
                return #Exit from the function

            else:

                device_username = App.get_running_app().device_username
                device_password = App.get_running_app().device_password


            device = { 
              'device_type': 'cisco_ios', 
              'ip': device_ip_address, 
              'username': device_username, 
              'password': device_password, 
              } 


            config_commands = ["ip route " + destination_address + ' ' + route_egress + ' ' + distance_metric]

            net_connect = ConnectHandler(**device) 

            net_connect.send_config_set(config_commands)

            #Set the password and username back to empty after completion of configuration
            App.get_running_app().device_username = ''
            App.get_running_app().device_password = ''

            #Create and display a popup to inform the user of the successful configuration
            popup = Popup(title='', content=Label(markup = True, text="Successfully configured static route to '[b]" +  destination_address + "[/b]' on device with IP address '[b]" + device_ip_address + "[/b]'"), size_hint =(0.95, 0.3))
            popup.open()

        #Except error to catch when Credentials are incorrect, informs the user of the error using a popup defined in the MainApplication.kv
        except AuthenticationException:

            Factory.NetmikoAuthenticateFailurePopup().open()

        #Except error to catch when Netmiko timeouts and is unable to connect to device, informs the user of the error using a popup defined in the MainApplication.kv
        except NetMikoTimeoutException:

            Factory.NetmikoTimeoutPopup().open()
    

    #Function to open the credential entry popup

    def OpenCredentialPopup(self):

        self.the_popup = DeviceUsernameAndPasswordPopup()
        self.the_popup.open()

    
    #Function linked to the Interface Egress radio button to modify the various widgets so that they are only visible and useable when the user wishes to use the interface egress

    def StaticRouteSelectInterfaceEgress(self):

        self.ids._Routing_Int_Static_Route_Layout_.ids.RoutingIntStaticRouteForwardIPLayout.disabled = True
        self.ids._Routing_Int_Static_Route_Layout_.ids.RoutingIntStaticRouteForwardInterfaceLayout.disabled = False

        self.ids._Routing_Int_Static_Route_Layout_.ids.RoutingIntStaticRouteForwardIPLayout.opacity = 0
        self.ids._Routing_Int_Static_Route_Layout_.ids.RoutingIntStaticRouteForwardInterfaceLayout.opacity = 1

        self.ids._Routing_Int_Static_Route_Layout_.ids.RoutingIntStaticRouteForwardIPLayout.ids.IPv4AddressTextInput.text = ''
  

    #Function linked to the Forward IP Egress radio button to modify the various widgets so that they are only visible and useable when the user wishes to use the forward ip egress

    def StaticRouteSelectIPEgress(self):

        self.ids._Routing_Int_Static_Route_Layout_.ids.RoutingIntStaticRouteForwardIPLayout.disabled = False
        self.ids._Routing_Int_Static_Route_Layout_.ids.RoutingIntStaticRouteForwardInterfaceLayout.disabled = True

        self.ids._Routing_Int_Static_Route_Layout_.ids.RoutingIntStaticRouteForwardIPLayout.opacity = 1
        self.ids._Routing_Int_Static_Route_Layout_.ids.RoutingIntStaticRouteForwardInterfaceLayout.opacity = 0

        self.ids._Routing_Int_Static_Route_Layout_.ids.RoutingIntStaticRouteForwardInterfaceLayout.ids.InterfaceTypeSpinnerLayout.text = 'Interface Type'
        self.ids._Routing_Int_Static_Route_Layout_.ids.RoutingIntStaticRouteForwardInterfaceLayout.ids.InterfaceNumberTextInput.text = ''




#Create the class for the 'Set Default Route' Screen using the Screen class for inheritiance

class RoutingIntDefaultRoute(Screen):        
    

     #Function to configure a default route on a device

    def RoutingIntDefaultRouteExecute(self):

        #Try statement to ensure that any errors connecting and configuring the device are handled gracefully and the user is informed of what the potential error was using popups
        try:

            distance_metric = self.ids._Routing_Int_Default_Route_Layout_.ids.RoutingIntDefaultRouteMetricDistanceLayout.ids.MetricDistanceTextInput.text

            if self.ids._Routing_Int_Default_Route_Layout_.ids.RoutingIntDefaultRouteForwardIPLayout.ids.IPv4AddressTextInput.text == '':
                route_egress = self.ids._Routing_Int_Default_Route_Layout_.ids.RoutingIntDefaultRouteForwardInterfaceLayout.ids.InterfaceTypeSpinnerLayout.ids.InterfaceTypeSpinner.text + ' ' +  self.ids._Routing_Int_Default_Route_Layout_.ids.RoutingIntDefaultRouteForwardInterfaceLayout.ids.InterfaceNumberTextInput.text
            else:
                route_egress = self.ids._Routing_Int_Default_Route_Layout_.ids.RoutingIntDefaultRouteForwardIPLayout.ids.IPv4AddressTextInput.text


            #Try statement to ensure the IP address entered is valid. If it is an invalid address the ipaddress module will raise a value error, at which point the user is informed that a valid IP address is required using a popup
            try:

                device_ip_address = self.ids._IPv4_Target_Device_Layout_.ids.IPv4AddressTextInput.text
                ipaddress.ip_address(device_ip_address)

            #ipaddress raises a value error when an invalid IP address is used
            except ValueError:

                Factory.InvalidIPAddressPopup().open() 
                return #Exit from the function


            #If statement to ensure user has entered a username or password
            if App.get_running_app().device_username == '' or App.get_running_app().device_password == '':

                Factory.NoUserOrPassPopup().open() 
                return #Exit from the function

            else:

                device_username = App.get_running_app().device_username
                device_password = App.get_running_app().device_password


            device = { 
              'device_type': 'cisco_ios', 
              'ip': device_ip_address, 
              'username': device_username, 
              'password': device_password, 
              } 


            config_commands = ["ip route 0.0.0.0 0.0.0.0 " + route_egress + ' ' + distance_metric]

            net_connect = ConnectHandler(**device) 

            net_connect.send_config_set(config_commands)

            #Set the password and username back to empty after completion of configuration
            App.get_running_app().device_username = ''
            App.get_running_app().device_password = ''

            #Create and display a popup to inform the user of the successful configuration
            popup = Popup(title='', content=Label(markup = True, text="Successfully configured default route on device with IP address '[b]" + device_ip_address + "[/b]'"), size_hint =(0.7, 0.3))
            popup.open()

        #Except error to catch when Credentials are incorrect, informs the user of the error using a popup defined in the MainApplication.kv
        except AuthenticationException:

            Factory.NetmikoAuthenticateFailurePopup().open()

        #Except error to catch when Netmiko timeouts and is unable to connect to device, informs the user of the error using a popup defined in the MainApplication.kv
        except NetMikoTimeoutException:

            Factory.NetmikoTimeoutPopup().open()


    #Function to open the credential entry popup

    def OpenCredentialPopup(self):

        self.the_popup = DeviceUsernameAndPasswordPopup()
        self.the_popup.open()


    #Function linked to the Interface Egress radio button to modify the various widgets so that they are only visible and useable when the user wishes to use the interface egress

    def DefaultRouteSelectInterfaceEgress(self):

        self.ids._Routing_Int_Default_Route_Layout_.ids.RoutingIntDefaultRouteForwardIPLayout.disabled = True
        self.ids._Routing_Int_Default_Route_Layout_.ids.RoutingIntDefaultRouteForwardInterfaceLayout.disabled = False

        self.ids._Routing_Int_Default_Route_Layout_.ids.RoutingIntDefaultRouteForwardIPLayout.opacity = 0
        self.ids._Routing_Int_Default_Route_Layout_.ids.RoutingIntDefaultRouteForwardInterfaceLayout.opacity = 1

        self.ids._Routing_Int_Default_Route_Layout_.ids.RoutingIntDefaultRouteForwardIPLayout.ids.IPv4AddressTextInput.text = ''


    #Function linked to the Forward IP Egress radio button to modify the various widgets so that they are only visible and useable when the user wishes to use the forward ip egress

    def DefaultRouteSelectIPEgress(self):

        self.ids._Routing_Int_Default_Route_Layout_.ids.RoutingIntDefaultRouteForwardIPLayout.disabled = False
        self.ids._Routing_Int_Default_Route_Layout_.ids.RoutingIntDefaultRouteForwardInterfaceLayout.disabled = True

        self.ids._Routing_Int_Default_Route_Layout_.ids.RoutingIntDefaultRouteForwardIPLayout.opacity = 1
        self.ids._Routing_Int_Default_Route_Layout_.ids.RoutingIntDefaultRouteForwardInterfaceLayout.opacity = 0

        self.ids._Routing_Int_Default_Route_Layout_.ids.RoutingIntDefaultRouteForwardInterfaceLayout.ids.InterfaceNumberTextInput.text = ''




#Create the class for the 'Set Default Gatewat' Screen using the Screen class for inheritiance

class RoutingIntDefaultGateway(Screen):        
    

    #Function to configure a default gateway on a device

    def RoutingIntDefaultGatewayExecute(self):
        
        #Try statement to ensure that any errors connecting and configuring the device are handled gracefully and the user is informed of what the potential error was using popups
        try:

            default_gateway = self.ids._Routing_Int_Default_Gateway_Layout_.ids.IPv4AddressTextInput.text

            #Try statement to ensure the IP address entered is valid. If it is an invalid address the ipaddress module will raise a value error, at which point the user is informed that a valid IP address is required using a popup
            try:

                device_ip_address = self.ids._IPv4_Target_Device_Layout_.ids.IPv4AddressTextInput.text
                ipaddress.ip_address(device_ip_address)

            #ipaddress raises a value error when an invalid IP address is used
            except ValueError:

                Factory.InvalidIPAddressPopup().open() 
                return #Exit from the function


            #If statement to ensure user has entered a username or password
            if App.get_running_app().device_username == '' or App.get_running_app().device_password == '':

                Factory.NoUserOrPassPopup().open() 
                return #Exit from the function

            else:

                device_username = App.get_running_app().device_username
                device_password = App.get_running_app().device_password


            device = { 
              'device_type': 'cisco_ios', 
              'ip': device_ip_address, 
              'username': device_username, 
              'password': device_password, 
              } 


            config_commands = ["ip default-gateway " + default_gateway]

            net_connect = ConnectHandler(**device) 

            net_connect.send_config_set(config_commands)

            #Set the password and username back to empty after completion of configuration
            App.get_running_app().device_username = ''
            App.get_running_app().device_password = ''

            #Create and display a popup to inform the user of the successful configuration
            popup = Popup(title='', content=Label(markup = True, text="Successfully configured default gateway as '[b]" +  default_gateway + "[/b]' on device with IP address '[b]" + device_ip_address + "[/b]'"), size_hint =(0.85, 0.3))
            popup.open()

        #Except error to catch when Credentials are incorrect, informs the user of the error using a popup defined in the MainApplication.kv
        except AuthenticationException:

            Factory.NetmikoAuthenticateFailurePopup().open()

        #Except error to catch when Netmiko timeouts and is unable to connect to device, informs the user of the error using a popup defined in the MainApplication.kv
        except NetMikoTimeoutException:

            Factory.NetmikoTimeoutPopup().open()


    #Function to open the credential entry popup
    
    def OpenCredentialPopup(self):

        self.the_popup = DeviceUsernameAndPasswordPopup()
        self.the_popup.open()
   