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

class BasicConfMenuButtons(BoxLayout):

    def BasicConfHostnameButton(self, instance):
        self.main_menu_root.manager.current = 'BasicConfHostnameScreen'

    def BasicConfDomainButton(self, instance):
        self.main_menu_root.manager.current = 'BasicConfDomainScreen'

    def BasicConfReloadButton(self, instance):
        self.main_menu_root.manager.current = 'BasicConfReloadScreen'



class BasicConfHostname(Screen):        
    

    def BasicConfHostnameExecute(self):
        #text = self.ids._Basic_Conf_Hostname_Layout_.ids.HostnameTextInput.text
        #self.ids._Basic_Conf_Hostname_Layout_.ids.IPv4AddressTextInput.text = text
        #print(text)

        ip_address = self.ids._Basic_Conf_Hostname_Layout_.ids.IPv4AddressTextInput.text
        hostname = self.ids._Basic_Conf_Hostname_Layout_.ids.HostnameTextInput.text

        device = { 
          'device_type': 'cisco_ios', 
          'ip': ip_address, 
          'username': 'Test', 
          'password': 'cisco123', 
          } 


        hostname_command = ["hostname " + hostname]

        net_connect = ConnectHandler(**device) 

        net_connect.send_config_set(hostname_command)

        output = net_connect.find_prompt()

        print(output)


class BasicConfDomain(Screen):  
    
    def BasicConfDomainExecute(self):

        ip_address = self.ids._Basic_Conf_Domain_Layout_.ids.IPv4AddressTextInput.text
        domain = self.ids._Basic_Conf_Domain_Layout_.ids.DomainTextInput.text

        device = { 
          'device_type': 'cisco_ios', 
          'ip': ip_address, 
          'username': 'Test', 
          'password': 'cisco123', 
          } 


        config_commands = ["ip domain-name " + domain]

        net_connect = ConnectHandler(**device) 

        output = net_connect.send_config_set(config_commands)

        print(output)

class BasicConfReload(Screen): 
    
    def BasicConfReloadExecute(self):

        ip_address = self.ids._Basic_Conf_Reload_Layout_.ids.IPv4AddressTextInput.text

        device = { 
          'device_type': 'cisco_ios', 
          'ip': ip_address, 
          'username': 'Test', 
          'password': 'cisco123', 
          } 


        net_connect = ConnectHandler(**device) 

        output = net_connect.send_command_timing('reload')
        if 'Proceed with reload' in output:
            output += net_connect.send_command_timing('\n')
            print(output)
        if 'System configuration has been modified' in output:
            output += net_connect.send_command_timing('yes')
            output += net_connect.send_command_timing('\n')
            print(output)
        else:
            # probably should raise an error here (as this is not expected)
            print('Failed')




        #output = net_connect.find_prompt()
        #print(output)
        #net_connect.send_command('do reload', expect_string='confirm')
        #net_connect.send_command('\n')
        #print('Reloading Device')


    
        
   