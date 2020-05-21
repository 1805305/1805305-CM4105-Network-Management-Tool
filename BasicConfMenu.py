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

class BasicConfMenuButtons(BoxLayout):

    def BasicConfHostnameButton(self, instance):
        self.main_menu_root.manager.current = 'BasicConfHostnameScreen'

    def BasicConfDomainButton(self, instance):
        self.main_menu_root.manager.current = 'BasicConfDomainScreen'

    def BasicConfReloadButton(self, instance):
        self.main_menu_root.manager.current = 'BasicConfReloadScreen'



#Create the class for the 'Set Hostname' Screen using the Screen class for inheritiance

class BasicConfHostname(Screen):        


    #Creates the function to execute the hostname function

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


            #If statement to ensure user has entered a username or password, if not a warning popup is raised
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

            config_commands = ["hostname " + hostname]

            net_connect = ConnectHandler(**device) 

            net_connect.send_config_set(config_commands)
    
            #Set the password and username back to empty after completion of configuration
            App.get_running_app().device_username = ''
            App.get_running_app().device_password = ''

            #Create and display a popup to inform the user of the successful configuration
            popup = Popup(title='', content=Label(markup = True, text="Successfully set '[b]" +  hostname + "[/b]' as hostname of device with IP address '[b]" + device_ip_address + "[/b]'"), size_hint =(0.7, 0.3))
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




#Create the class for the 'Set Domain' Screen using the Screen class for inheritiance

class BasicConfDomain(Screen):  
    
    #Creates the function to execute the domain function

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


            #If statement to ensure user has entered a username or password, if not a warning popup is raised
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


            config_commands = ["ip domain-name " + domain]

            net_connect = ConnectHandler(**device) 

            net_connect.send_config_set(config_commands)

            #Set the password and username back to empty after completion of configuration
            App.get_running_app().device_username = ''
            App.get_running_app().device_password = ''

            #Create and display a popup to inform the user of the successful configuration
            popup = Popup(title='', content=Label(markup = True, text="Successfully set '[b]" +  domain + "[/b]' as domain of device with IP address '[b]" + device_ip_address + "[/b]'"), size_hint =(0.7, 0.3))
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


#Create the class for the 'Set Domain' Screen using the Screen class for inheritiance

class BasicConfReload(Screen): 
    
    #Creates the function to execute the reload function

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


            net_connect = ConnectHandler(**device) 

            output = net_connect.send_command_timing('reload')


            #If statements that check the output for various strings to ensure that the correct commands are sent
            if 'Proceed with reload' in output: #If this string is detected the tool will send a newline, which will start the reload
                output += net_connect.send_command_timing('\n')

                #Set the password and username back to empty after completion of configuration
                App.get_running_app().device_username = ''
                App.get_running_app().device_password = ''

                #Creates and displays a popup to inform user that reload was successful
                popup = Popup(title='', content=Label(markup = True, text="Succesful reload of device with IP address '[b]"+ device_ip_address + "[/b]'"), size_hint =(0.5, 0.3))
                popup.open()

            if 'System configuration has been modified' in output: #If this string is detected the tool will send the below commands to start the reload
                output += net_connect.send_command_timing('yes')
                output += net_connect.send_command_timing('\n')
                #print(output)

                #Set the password and username back to empty after completion of configuration
                App.get_running_app().device_username = ''
                App.get_running_app().device_password = ''

                #Creates and displays a popup to inform user that reload was successful
                popup = Popup(title='', content=Label(markup = True, text="Succesful reload of device with IP address '[b]"+ device_ip_address + "[/b]'"), size_hint =(0.5, 0.3))
                popup.open()

            else: #If neither set of strings are detected the tool will display a failed configuration popup
                #Creates and displays a popup to inform user that reload has failed
                popup = Popup(title='', content=Label(markup = True, text="Failed to reload device with IP address '[b]"+ device_ip_address + "[/b]'"), size_hint =(0.5, 0.3))
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
        
   