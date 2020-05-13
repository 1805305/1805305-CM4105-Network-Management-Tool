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

from kivy.properties import StringProperty

from netmiko import ConnectHandler  

import ipaddress

from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import AuthenticationException

from GetDeviceUsernameAndPassword import DeviceUsernameAndPasswordPopup


class BasicConfMenuButtons(BoxLayout):

    def BasicConfHostnameButton(self, instance):
        self.main_menu_root.manager.current = 'BasicConfHostnameScreen'

    def BasicConfDomainButton(self, instance):
        self.main_menu_root.manager.current = 'BasicConfDomainScreen'

    def BasicConfReloadButton(self, instance):
        self.main_menu_root.manager.current = 'BasicConfReloadScreen'



class BasicConfHostname(Screen):        
    
    device_username = StringProperty()
    device_password = StringProperty()

    def BasicConfHostnameGetDeviceUsernameAndPassword(self, *args):

        check = False

        p = DeviceUsernameAndPasswordPopup()
        p.ids.UsernameTextInput.bind(text=self.setter('device_username'))
        p.ids.PasswordTextInput.bind(text=self.setter('device_password'))
        p.ids.PasswordTextInput.bind(on_release)
        

        p.open()

    def BasicConfHostnameExecute(self):

        

        #Try statement to ensure that any errors connecting and configuring the device are handled gracefully and the user is informed of what the potential error was using popups
        try:

            hostname = self.ids._Basic_Conf_Hostname_Layout_.ids.HostnameTextInput.text

            #Try statement to ensure the IP address entered is valid. If it is an invalid address the ipaddress module will raise a value error, at which point the user is informed that a valid IP address is required using a popup
            try:

                device_ip_address = self.ids._IPv4_Target_Device_Layout_.ids.IPv4AddressTextInput.text
                ipaddress.ip_address(device_ip_address)

            #ipaddress raises a value error when an invalid IP address is used
            except ValueError:

                Factory.InvalidIPAddressPopup().open() 
                return #Exit from the function

            #self.ShowDeviceUsernameAndPasswordPopup()

            device_username = self.device_username
            device_password = self.device_password

            print(device_username)
            print(device_password)

            device = { 
              'device_type': 'cisco_ios', 
              'ip': device_ip_address, 
              'username': device_username, 
              'password': device_password, 
              } 

            config_commands = ["hostname " + hostname]

            #net_connect = ConnectHandler(**device) 

            #net_connect.send_config_set(config_commands)
    
            #Create and display a popup to inform the user of the successful configuration
            popup = Popup(title='', content=Label(markup = True, text="Successfully set '[b]" +  hostname + "[/b]' as hostname of device with IP address '[b]" + device_ip_address + "[/b]'"), size_hint =(0.65, 0.3))
            popup.open()
        

        #Except error to catch when Credentials are incorrect, informs the user of the error using a popup defined in the MainApplication.kv
        except AuthenticationException:

            Factory.NetmikoAuthenticateFailurePopup().open()

        #Except error to catch when Netmiko timeouts and is unable to connect to device, informs the user of the error using a popup defined in the MainApplication.kv
        except NetMikoTimeoutException:

            Factory.NetmikoTimeoutPopup().open()


class BasicConfDomain(Screen):  
    
    def BasicConfDomainExecute(self):
        
        #Try statement to ensure that any errors connecting and configuring the device are handled gracefully and the user is informed of what the potential error was using popups
        try:

            domain = self.ids._Basic_Conf_Domain_Layout_.ids.DomainTextInput.text
    
            #Try statement to ensure the IP address entered is valid. If it is an invalid address the ipaddress module will raise a value error, at which point the user is informed that a valid IP address is required using a popup
            try:

                device_ip_address = self.ids._IPv4_Target_Device_Layout_.ids.IPv4AddressTextInput.text
                ipaddress.ip_address(device_ip_address)

            #ipaddress raises a value error when an invalid IP address is used
            except ValueError:

                Factory.InvalidIPAddressPopup().open() 
                return #Exit from the function


            device = { 
              'device_type': 'cisco_ios', 
              'ip': device_ip_address, 
              'username': 'Test', 
              'password': 'cisco123', 
              } 


            config_commands = ["ip domain-name " + domain]

            net_connect = ConnectHandler(**device) 

            net_connect.send_config_set(config_commands)

            #Create and display a popup to inform the user of the successful configuration
            popup = Popup(title='', content=Label(markup = True, text="Successfully set '[b]" +  domain + "[/b]' as domain of device with IP address '[b]" + device_ip_address + "[/b]'"), size_hint =(0.65, 0.3))
            popup.open()
  

        #Except error to catch when Credentials are incorrect, informs the user of the error using a popup defined in the MainApplication.kv
        except AuthenticationException:

            Factory.NetmikoAuthenticateFailurePopup().open()

        #Except error to catch when Netmiko timeouts and is unable to connect to device, informs the user of the error using a popup defined in the MainApplication.kv
        except NetMikoTimeoutException:

            Factory.NetmikoTimeoutPopup().open()

class BasicConfReload(Screen): 
    
    def BasicConfReloadExecute(self):

        #Try statement to ensure that any errors connecting and configuring the device are handled gracefully and the user is informed of what the potential error was using popups
        try:

            
            #Try statement to ensure the IP address entered is valid. If it is an invalid address the ipaddress module will raise a value error, at which point the user is informed that a valid IP address is required using a popup
            try:

                device_ip_address = self.ids._Basic_Conf_Reload_Layout_.ids.IPv4AddressTextInput.text
                ipaddress.ip_address(device_ip_address)

            #ipaddress raises a value error when an invalid IP address is used
            except ValueError:

                Factory.InvalidIPAddressPopup().open() 
                return #Exit from the function


            device = { 
              'device_type': 'cisco_ios', 
              'ip': device_ip_address, 
              'username': 'Test', 
              'password': 'cisco123', 
              } 


            net_connect = ConnectHandler(**device) 

            output = net_connect.send_command_timing('reload')
            if 'Proceed with reload' in output:
                output += net_connect.send_command_timing('\n')
                #print(output)

                #Creates and displays a popup to inform user that reload was successful
                popup = Popup(title='', content=Label(markup = True, text="Succesful reload of device with IP address '[b]"+ device_ip_address + "[/b]'"), size_hint =(0.5, 0.3))
                popup.open()
            if 'System configuration has been modified' in output:
                output += net_connect.send_command_timing('yes')
                output += net_connect.send_command_timing('\n')
                #print(output)

                #Creates and displays a popup to inform user that reload was successful
                popup = Popup(title='', content=Label(markup = True, text="Succesful reload of device with IP address '[b]"+ device_ip_address + "[/b]'"), size_hint =(0.5, 0.3))
                popup.open()
            else:
                #Creates and displays a popup to inform user that reload has failed
                popup = Popup(title='', content=Label(markup = True, text="Failed to reload device with IP address '[b]"+ device_ip_address + "[/b]'"), size_hint =(0.5, 0.3))
                popup.open()
  

        #Except error to catch when Credentials are incorrect, informs the user of the error using a popup defined in the MainApplication.kv
        except AuthenticationException:

            Factory.NetmikoAuthenticateFailurePopup().open()

        #Except error to catch when Netmiko timeouts and is unable to connect to device, informs the user of the error using a popup defined in the MainApplication.kv
        except NetMikoTimeoutException:

            Factory.NetmikoTimeoutPopup().open()


    
        
   