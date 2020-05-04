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


class NetMonMenuButtons(BoxLayout):

    def NetMonSpanConfButton(self, instance):
        self.main_menu_root.manager.current = 'NetMonSpanConfScreen'



class NetMonSpanConf(Screen):   
    
    def NetMonSpanConfExecute(self):
        
        session_ID = self.ids._Net_Mon_Span_Conf_Layout_.ids.NetMonSpanConfSessionNoLayout.ids.SPANSessionIDTextInput.text
        source_port = self.ids._Net_Mon_Span_Conf_Layout_.ids.NetMonSpanConfSourcePortLayout.ids.InterfaceTypeSpinner.text + ' ' +  self.ids._Net_Mon_Span_Conf_Layout_.ids.NetMonSpanConfSourcePortLayout.ids.InterfaceNumberTextInput.text
        destination_port = self.ids._Net_Mon_Span_Conf_Layout_.ids.NetMonSpanConfDestinationPortLayout.ids.InterfaceTypeSpinner.text + ' ' +  self.ids._Net_Mon_Span_Conf_Layout_.ids.NetMonSpanConfDestinationPortLayout.ids.InterfaceNumberTextInput.text

        source_command = 'monitor session ' + session_ID + ' source interface ' + source_port
        destionation_command = 'monitor session ' + session_ID + ' destination interface ' + destination_port
        

        device_ip_address = self.ids._IPv4_Target_Device_Layout_.ids.IPv4AddressTextInput.text


        device = { 
          'device_type': 'cisco_ios', 
          'ip': device_ip_address, 
          'username': 'Test', 
          'password': 'cisco123', 
          } 


        config_commands = [source_command, destionation_command]

        net_connect = ConnectHandler(**device) 

        output = net_connect.send_config_set(config_commands)

        print(output)

        self.ids._Net_Mon_Span_Conf_Layout_.ids.SPANCompleteLabel.text = "Successfully configured SPAN with session ID '[b]" +  session_ID + "[/b]' on device with IP address '[b]" + device_ip_address + "[/b]'"
    
        
   