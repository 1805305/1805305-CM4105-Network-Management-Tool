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

from netmiko import ConnectHandler  

import ipaddress

from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import AuthenticationException

from MiscModules import DeviceUsernameAndPasswordPopup


class IntConfMenuButtons(BoxLayout):

    def IntConfAssignIPv4Button(self, instance):
        self.main_menu_root.manager.current = 'IntConfAssignIPv4Screen'

    def IntConfEthernetIntButton(self, instance):
        self.main_menu_root.manager.current = 'IntConfEthernetIntScreen'



class IntConfAssignIPv4(Screen): 
    
    def IntConfAssignIPv4Execute(self):

        #Try statement to ensure that any errors connecting and configuring the device are handled gracefully and the user is informed of what the potential error was using popups
        try:
        
            interface = self.ids._Int_Conf_Assign_IPv4_Layout_.ids.InterfaceSelectionLayout.ids.InterfaceTypeSpinnerLayout.ids.InterfaceTypeSpinner.text + ' ' +  self.ids._Int_Conf_Assign_IPv4_Layout_.ids.InterfaceSelectionLayout.ids.InterfaceNumberTextInput.text
            ip_address = self.ids._Int_Conf_Assign_IPv4_Layout_.ids.IPv4AndSubnetMaskLayout.ids.IPv4AddressTextInput.text + ' ' +  self.ids._Int_Conf_Assign_IPv4_Layout_.ids.IPv4AndSubnetMaskLayout.ids.SubnetMaskSpinnerLayout.ids.SubnetMaskSpinner.text


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


            config_commands = ["interface " + interface, 'ip address ' + device_ip_address]

            net_connect = ConnectHandler(**device) 

            net_connect.send_config_set(config_commands)

            #Set the password and username back to empty after completion of configuration
            App.get_running_app().device_username = ''
            App.get_running_app().device_password = ''

            #Create and display a popup to inform the user of the successful configuration
            popup = Popup(title='', content=Label(markup = True, text="Successfully set '[b]" +  interface + "[/b]' with an of IP address '[b]" + ip_address + "[/b]'"), size_hint =(0.65, 0.3))
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


class IntConfEthernetInt(Screen):        
    


    def IntConfEthernetIntExecute(self):
        

        #Try statement to ensure that any errors connecting and configuring the device are handled gracefully and the user is informed of what the potential error was using popups
        try:

            #Define the three potential commands as empty variables

            description_command = ''
            duplex_command = ''
            bandwidth_command = ''

            interface = self.ids._Int_Conf_Ethernet_Int_Layout_.ids.InterfaceSelectionLayout.ids.InterfaceTypeSpinnerLayout.ids.InterfaceTypeSpinner.text + ' ' +  self.ids._Int_Conf_Ethernet_Int_Layout_.ids.InterfaceSelectionLayout.ids.InterfaceNumberTextInput.text
            interface_command = "interface " + interface


            #If statement to check if user has selected Transport Method checkbox, if so the command will be created and inserted into the variable. Else the variable will be left blank

            if self.ids._Int_Conf_Ethernet_Int_Function_Select_.ids.DescriptionCheckbox.active == True:

                description_command = 'description ' + self.ids._Int_Conf_Ethernet_Int_Layout_.ids.IntConfEthernetIntDescriptionLayout.ids.EthernetIntDescriptionTextInput.text
            
            else:
                pass



            #If statement to check if user has selected Duplex checkbox, if so the command will be created and inserted into the variable. Else the variable will be left blank

            if self.ids._Int_Conf_Ethernet_Int_Function_Select_.ids.DuplexCheckbox.active == True:
            

                #If statement for handling if a user does not change duplex type or - It will default to Auto

                if self.ids._Int_Conf_Ethernet_Int_Layout_.ids.IntConfEthernetIntDuplexLayout.ids.DuplexTypeSpinner.text == 'Duplex Type':
                    duplex_type = 'Auto'
                else:
                    duplex_type = self.ids._Int_Conf_Ethernet_Int_Layout_.ids.IntConfEthernetIntDuplexLayout.ids.DuplexTypeSpinner.text

                duplex_command = 'duplex ' + duplex_type #Creates the final duplex command

            else:
                pass

            #If statement to check if user has selected Bandwidth checkbox, if so the command will be created and inserted into the variable. Else the variable will be left blank

            if self.ids._Int_Conf_Ethernet_Int_Function_Select_.ids.BandwidthCheckbox.active == True:
            
                bandwidth_command = 'bandwidth ' + self.ids._Int_Conf_Ethernet_Int_Layout_.ids.IntConfEthernetIntBandwidthLayout.ids.BandwidthTextInput.text
            else:
                pass



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

        
            config_commands = [interface_command, description_command, duplex_command, bandwidth_command]
        

            net_connect = ConnectHandler(**device) 

            net_connect.send_config_set(config_commands)

            #Set the password and username back to empty after completion of configuration
            App.get_running_app().device_username = ''
            App.get_running_app().device_password = ''

            #Create and display a popup to inform the user of the successful configuration
            popup = Popup(title='', content=Label(markup = True, text="Successfully configured interface '[b]" +  interface + "[/b]' of device with IP address '[b]" + device_ip_address + "[/b]'"), size_hint =(0.8, 0.3))
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



    #Function linked to the Description checkbox to modify the Description widgets so that they are visible when checked and disabled and hidden from view when unchecked, the text input will have it's value reset
    def IntConfEthernetIntDescriptionSelect(self):

        if self.ids._Int_Conf_Ethernet_Int_Function_Select_.ids.DescriptionCheckbox.active == True:

            self.ids._Int_Conf_Ethernet_Int_Layout_.ids.IntConfEthernetIntDescriptionLayout.opacity = 1
            self.ids._Int_Conf_Ethernet_Int_Layout_.ids.IntConfEthernetIntDescriptionLayout.disabled = False

        else:

            self.ids._Int_Conf_Ethernet_Int_Layout_.ids.IntConfEthernetIntDescriptionLayout.opacity = 0
            self.ids._Int_Conf_Ethernet_Int_Layout_.ids.IntConfEthernetIntDescriptionLayout.disabled = True

            self.ids._Int_Conf_Ethernet_Int_Layout_.ids.IntConfEthernetIntDescriptionLayout.ids.EthernetIntDescriptionTextInput.text = ''


    #Function linked to the Duplex checkbox to modify the Duplex Type widgets so that they are visible when checked and disabled and hidden from view when unchecked, the Spinner input will have it's value reset
    def IntConfEthernetIntDuplexSelect(self):

        if self.ids._Int_Conf_Ethernet_Int_Function_Select_.ids.DuplexCheckbox.active == True:

            self.ids._Int_Conf_Ethernet_Int_Layout_.ids.IntConfEthernetIntDuplexLayout.opacity = 1
            self.ids._Int_Conf_Ethernet_Int_Layout_.ids.IntConfEthernetIntDuplexLayout.disabled = False

        else:

            self.ids._Int_Conf_Ethernet_Int_Layout_.ids.IntConfEthernetIntDuplexLayout.opacity = 0
            self.ids._Int_Conf_Ethernet_Int_Layout_.ids.IntConfEthernetIntDuplexLayout.disabled = True

            self.ids._Int_Conf_Ethernet_Int_Layout_.ids.IntConfEthernetIntDuplexLayout.ids.DuplexTypeSpinner.text = 'Duplex Type'
            



    #Function linked to the Bandwidth checkbox to modify the Bandwidth widgets so that they are visible when checked and disabled and hidden from view when unchecked, the text inputs will have it's value reset
    def IntConfEthernetIntBandwidthSelect(self):
        

        if self.ids._Int_Conf_Ethernet_Int_Function_Select_.ids.BandwidthCheckbox.active == True:

            self.ids._Int_Conf_Ethernet_Int_Layout_.ids.IntConfEthernetIntBandwidthLayout.opacity = 1
            self.ids._Int_Conf_Ethernet_Int_Layout_.ids.IntConfEthernetIntBandwidthLayout.disabled = False


        else:

            self.ids._Int_Conf_Ethernet_Int_Layout_.ids.IntConfEthernetIntBandwidthLayout.opacity = 0
            self.ids._Int_Conf_Ethernet_Int_Layout_.ids.IntConfEthernetIntBandwidthLayout.disabled = True
            
            self.ids._Int_Conf_Ethernet_Int_Layout_.ids.IntConfEthernetIntBandwidthLayout.ids.BandwidthTextInput.text = ''


    
        
   