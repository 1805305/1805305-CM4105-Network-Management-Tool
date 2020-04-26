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


class IntConfMenuButtons(BoxLayout):

    def IntConfAssignIPv4Button(self, instance):
        self.main_menu_root.manager.current = 'IntConfAssignIPv4Screen'

    def IntConfEthernetIntButton(self, instance):
        self.main_menu_root.manager.current = 'IntConfEthernetIntScreen'



class IntConfAssignIPv4(Screen): 
    
    def IntConfAssignIPv4Execute(self):


        
        interface = self.ids._Int_Conf_Assign_IPv4_Layout_.ids.InterfaceTypeSpinner.text + ' ' +  self.ids._Int_Conf_Assign_IPv4_Layout_.ids.InterfaceNumberTextInput.text
        ip_address = self.ids._Int_Conf_Assign_IPv4_Layout_.ids.IPv4AddressTextInput.text + ' ' +  self.ids._Int_Conf_Assign_IPv4_Layout_.ids.SubnetMaskSpinnerLayout.ids.SubnetMaskSpinner.text


        device_ip_address = self.ids._IPv4_Target_Device_Layout_.ids.IPv4AddressTextInput.text


        device = { 
          'device_type': 'cisco_ios', 
          'ip': device_ip_address, 
          'username': 'Test', 
          'password': 'cisco123', 
         } 


        config_commands = ["interface " + interface, 'ip address ' + ip_address]

        net_connect = ConnectHandler(**device) 

        output = net_connect.send_config_set(config_commands)

        print(output)


class IntConfEthernetInt(Screen):        
    pass


    
        
   