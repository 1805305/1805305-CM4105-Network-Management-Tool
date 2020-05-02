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


        
        interface = self.ids._Int_Conf_Assign_IPv4_Layout_.ids.InterfaceSelectionLayout.ids.InterfaceTypeSpinnerLayout.ids.InterfaceTypeSpinner.text + ' ' +  self.ids._Int_Conf_Assign_IPv4_Layout_.ids.InterfaceSelectionLayout.ids.InterfaceNumberTextInput.text
        ip_address = self.ids._Int_Conf_Assign_IPv4_Layout_.ids.IPv4AndSubnetMaskLayout.ids.IPv4AddressTextInput.text + ' ' +  self.ids._Int_Conf_Assign_IPv4_Layout_.ids.IPv4AndSubnetMaskLayout.ids.SubnetMaskSpinnerLayout.ids.SubnetMaskSpinner.text


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
    


    def IntConfEthernetIntExecute(self):
        
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




        device_ip_address = self.ids._IPv4_Target_Device_Layout_.ids.IPv4AddressTextInput.text

        device = { 
          'device_type': 'cisco_ios', 
          'ip': device_ip_address, 
          'username': 'Test', 
          'password': 'cisco123', 
          } 

        
        config_commands = [interface_command, description_command, duplex_command, bandwidth_command]
        

        net_connect = ConnectHandler(**device) 

        output = net_connect.send_config_set(config_commands)

        print(output)


        



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


    
        
   