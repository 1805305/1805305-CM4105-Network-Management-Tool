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

class SecurityConfMenuButtons(BoxLayout):

    def SecurityConfLocalUsernameDatabaseButton(self, instance):
        self.main_menu_root.manager.current = 'SecurityConfLocalUsernameDatabaseScreen'

    def SecurityConfPasswordEncryptionButton(self, instance):
        self.main_menu_root.manager.current = 'SecurityConfPasswordEncryptionScreen'

    def SecurityConfAuxVtyConLinesButton(self, instance):
        self.main_menu_root.manager.current = 'SecurityConfAuxVtyConLinesScreen'


class SecurityConfLocalUsernameDatabase(Screen):        
    
    def SecurityConfLocalUsernameDatabaseExecute(self):



        privilege_level = self.ids._Security_Conf_Local_Username_Database_Layout_.ids.SecurityConfLocalUsernameDatabasePrivilegeLayout.ids.PrivilegeLevelSpinner.text
        new_username = self.ids._Security_Conf_Local_Username_Database_Layout_.ids.SecurityConfLocalUsernameDatabaseUserAndPassLayout.ids.UsernameTextInput.text
        new_password = self.ids._Security_Conf_Local_Username_Database_Layout_.ids.SecurityConfLocalUsernameDatabaseUserAndPassLayout.ids.PasswordTextInput.text

        device_ip_address = self.ids._IPv4_Target_Device_Layout_.ids.IPv4AddressTextInput.text

        device = { 
          'device_type': 'cisco_ios', 
          'ip': device_ip_address, 
          'username': 'Test', 
          'password': 'cisco123', 
          } 

        priv_check = self.ids._Security_Conf_Local_Username_Database_Layout_.ids.SecurityConfLocalUsernameDatabasePrivilegeLayout.ids.PrivilegeLevelSpinner.text
        secret_check = self.ids._Security_Conf_Local_Username_Database_Layout_.ids.SecurityConfLocalUsernameDatabaseSecretLayout.ids.SecretPasswordTrue.active

        if secret_check == True and priv_check != 'No Privilege Required': #Priv and Secret
            config_commands = ["username " + new_username + " privilege " + privilege_level + " secret " + new_password]
        elif  priv_check != 'No Privilege Required': #Priv and password
            config_commands = ["username " + new_username + " privilege " + privilege_level + " password " + new_password]
        elif  secret_check == True:  #Secret       
            config_commands = ["username " + new_username + " secret " + new_password]
        else:   
            config_commands = ["username " + new_username + " password " + new_password] #Standard

        net_connect = ConnectHandler(**device) 

        output = net_connect.send_config_set(config_commands)

        print(output)
    

class SecurityConfPasswordEncryption(Screen):        
    
    def SecurityConfPasswordEncryptionExecute(self):

        device_ip_address = self.ids._IPv4_Target_Device_Layout_.ids.IPv4AddressTextInput.text

        device = { 
          'device_type': 'cisco_ios', 
          'ip': device_ip_address, 
          'username': 'Test', 
          'password': 'cisco123', 
          } 

        if self.ids._Security_Conf_Password_Encryption_Layout_.ids.EnableToggle.state == 'down':
            config_commands = ["service password-encryption"]
        else:
            config_commands = ["no service password-encryption"]

        net_connect = ConnectHandler(**device) 

        output = net_connect.send_config_set(config_commands)

        print(output)

class SecurityConfAuxVtyConLines(Screen):        
    pass

    
        
   