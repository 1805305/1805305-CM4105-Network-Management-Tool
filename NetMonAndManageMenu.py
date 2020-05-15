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

from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.uix.label import Label 

from netmiko import ConnectHandler  

import ipaddress

from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import AuthenticationException 

from MiscModules import DeviceUsernameAndPasswordPopup

class NetMonMenuButtons(BoxLayout):

    def NetMonSpanConfButton(self, instance):
        self.main_menu_root.manager.current = 'NetMonSpanConfScreen'



class NetMonSpanConf(Screen):   
    
    def NetMonSpanConfExecute(self):
        
        #Try statement to ensure that any errors connecting and configuring the device are handled gracefully and the user is informed of what the potential error was using popups
        try:

            session_ID = self.ids._Net_Mon_Span_Conf_Layout_.ids.NetMonSpanConfSessionNoLayout.ids.SPANSessionIDTextInput.text
            source_port = self.ids._Net_Mon_Span_Conf_Layout_.ids.NetMonSpanConfSourcePortLayout.ids.InterfaceTypeSpinner.text + ' ' +  self.ids._Net_Mon_Span_Conf_Layout_.ids.NetMonSpanConfSourcePortLayout.ids.InterfaceNumberTextInput.text
            destination_port = self.ids._Net_Mon_Span_Conf_Layout_.ids.NetMonSpanConfDestinationPortLayout.ids.InterfaceTypeSpinner.text + ' ' +  self.ids._Net_Mon_Span_Conf_Layout_.ids.NetMonSpanConfDestinationPortLayout.ids.InterfaceNumberTextInput.text

            source_command = 'monitor session ' + session_ID + ' source interface ' + source_port
            destionation_command = 'monitor session ' + session_ID + ' destination interface ' + destination_port
        

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
              'username': 'Test', 
              'password': 'cisco123', 
              } 


            config_commands = [source_command, destionation_command]

            net_connect = ConnectHandler(**device) 

            net_connect.send_config_set(config_commands)

            #Set the password and username back to empty after completion of configuration
            App.get_running_app().device_username = ''
            App.get_running_app().device_password = ''

            #Create and display a popup to inform the user of the successful configuration
            popup = Popup(title='', content=Label(markup = True, text="Successfully configured SPAN with session ID '[b]" +  session_ID + "[/b]' on device with IP address '[b]" + device_ip_address + "[/b]'"), size_hint =(0.8, 0.3))
            popup.open()


        #Except error to catch when Credentials are incorrect, informs the user of the error using a popup defined in the MainApplication.kv
        except AuthenticationException:

            Factory.NetmikoAuthenticateFailurePopup().open()

        #Except error to catch when Netmiko timeouts and is unable to connect to device, informs the user of the error using a popup defined in the MainApplication.kv
        except NetMikoTimeoutException:

            Factory.NetmikoTimeoutPopup().open()
    

    def OpenCredentialPopup(self):

        self.the_popup = DeviceUsernameAndPasswordPopup()
        self.the_popup.open()
   