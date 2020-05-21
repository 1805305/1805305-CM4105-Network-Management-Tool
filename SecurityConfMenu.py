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

class SecurityConfMenuButtons(BoxLayout):

    def SecurityConfLocalUsernameDatabaseButton(self, instance):
        self.main_menu_root.manager.current = 'SecurityConfLocalUsernameDatabaseScreen'

    def SecurityConfPasswordEncryptionButton(self, instance):
        self.main_menu_root.manager.current = 'SecurityConfPasswordEncryptionScreen'

    def SecurityConfAuxVtyConLinesButton(self, instance):
        self.main_menu_root.manager.current = 'SecurityConfAuxVtyConLinesScreen'




#Create the class for the 'Configure Local Username Databse' Screen using the Screen class for inheritiance

class SecurityConfLocalUsernameDatabase(Screen):        
    
    #Function to add a new user account to a device

    def SecurityConfLocalUsernameDatabaseExecute(self):

        #Try statement to ensure that any errors connecting and configuring the device are handled gracefully and the user is informed of what the potential error was using popups
        try:

            privilege_level = self.ids._Security_Conf_Local_Username_Database_Layout_.ids.SecurityConfLocalUsernameDatabasePrivilegeLayout.ids.PrivilegeLevelSpinner.text
            new_username = self.ids._Security_Conf_Local_Username_Database_Layout_.ids.SecurityConfLocalUsernameDatabaseUserAndPassLayout.ids.UsernameTextInput.text
            new_password = self.ids._Security_Conf_Local_Username_Database_Layout_.ids.SecurityConfLocalUsernameDatabaseUserAndPassLayout.ids.PasswordTextInput.text


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

            net_connect.send_config_set(config_commands)

            #Set the password and username back to empty after completion of configuration
            App.get_running_app().device_username = ''
            App.get_running_app().device_password = ''

            #Create and display a popup to inform the user of the successful configuration
            popup = Popup(title='', content=Label(markup = True, text="Successfully added new user '[b]" +  new_username + "[/b]' to device with IP address '[b]" + device_ip_address + "[/b]'"), size_hint =(0.8, 0.3))
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




#Create the class for the 'Set Password Encryption' Screen using the Screen class for inheritiance

class SecurityConfPasswordEncryption(Screen):        
    

    #Function to enable or disable password encryption on a device

    def SecurityConfPasswordEncryptionExecute(self):

        #Try statement to ensure that any errors connecting and configuring the device are handled gracefully and the user is informed of what the potential error was using popups
        try:


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

            if self.ids._Security_Conf_Password_Encryption_Layout_.ids.EnableToggle.state == 'down':
                config_commands = ["service password-encryption"]
                encryption_type = "Enabled"
            else:
                config_commands = ["no service password-encryption"]
                encryption_type = "Disabled"

            net_connect = ConnectHandler(**device) 

            net_connect.send_config_set(config_commands)

            #Set the password and username back to empty after completion of configuration
            App.get_running_app().device_username = ''
            App.get_running_app().device_password = ''

            #Create and display a popup to inform the user of the successful configuration
            popup = Popup(title='', content=Label(markup = True, text="Successfully '[b]" +  encryption_type + "[/b]' password encryption on device with IP address '[b]" + device_ip_address + "[/b]'"), size_hint =(0.8, 0.3))
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




#Create the class for the 'Configure Aux, Con and Vty Lines' Screen using the Screen class for inheritiance

class SecurityConfAuxVtyConLines(Screen):        
    

    #Function to configure a the Aux, Con or Vty lines on a device

    def SecurityConfAuxVtyConLinesExecute(self):
        
        #Try statement to ensure that any errors connecting and configuring the device are handled gracefully and the user is informed of what the potential error was using popups
        try:

            #Define the three potential commands as empty variables

            transport_command = ''
            login_command = ''
            exec_timeout_command = ''

            #Else if to find out which line the user wishes to configure

            if self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesSelectLineLayout.ids.ConTrue.active == True:
                line_to_configure = 'Console'
            elif self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesSelectLineLayout.ids.AuxTrue.active == True:
                line_to_configure = 'Aux'
            else:
                line_to_configure = 'Vty'


            #Else if to find out the line_range the user wishes to configure, if console or auxiliary is the line to configure set line to 0

            if self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesSelectLineLayout.ids.ConTrue.active == True or self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesSelectLineLayout.ids.AuxTrue.active == True:
                line_range = '0'
            else:
                start_line_range = self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesLineRangeLayout.ids.LineRangeStartTextInput.text
                end_line_range = self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesLineRangeLayout.ids.LineRangeEndTextInput.text

                line_range = start_line_range + ' ' + end_line_range #Define the line_range variable from reading user input from the two text inputs

            line_command = "line " + line_to_configure + ' ' + line_range #Create a variable to store the command to enter the line to improve ease of reading further down


            #If statement to check if user has selected Transport Method checkbox, if so the command will be created and inserted into the variable. Else the variable will be left blank

            if self.ids._Security_Conf_Aux_Vty_Con_Lines_Function_Select_.ids.TransportMethodCheckbox.active == True:


                #Creates the variable for input/output dependent on user choice
                transport_type = self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesTransportOptionsLayout.ids.TransportInputOutputSpinner.text # Defines wheter the user wants to configure input or output transport method


                #If statement for handling if a user does not change method 1 - It will default to ssh

                if self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesTransportOptionsLayout.ids.TransportMethodNo1Spinner.text == 'Method 1':
                    transport_method1 = 'SSH'
                else:
                    transport_method1 = self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesTransportOptionsLayout.ids.TransportMethodNo1Spinner.text



                #If statement for handling if a user does not change method 2 or if N/A was selected. Or if a user has entered 'none' as the value in method 1 - It will default to blank

                if self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesTransportOptionsLayout.ids.TransportMethodNo2Spinner.text == 'Method 2' or self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesTransportOptionsLayout.ids.TransportMethodNo2Spinner.text == 'N/A' or transport_method1 == 'none':
                    transport_method2 = ''
                else:
                    transport_method2 = self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesTransportOptionsLayout.ids.TransportMethodNo2Spinner.text
                

                #Combines the three variables to create the final command 

                transport_command = 'transport ' + transport_type + ' ' + transport_method1 + ' ' + transport_method2 # Creates the final Transport Command
            
            else:
                pass



            #If statement to check if user has selected Login Type checkbox, if so the command will be created and inserted into the variable. Else the variable will be left blank

            if self.ids._Security_Conf_Aux_Vty_Con_Lines_Function_Select_.ids.LoginTypeCheckbox.active == True:
            
                #If statement to check if user has selected to login using the local user database or a custom password and set the login_type_command variable accordingly
                if self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesLoginOptionsLayout.ids.LoginLocalTrue.active == True:
                    login_command = 'login local'
                else:
                    login_command = 'password ' + self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesLoginOptionsLayout.ids.LineLoginPasswordTextInput.text

            else:
                pass

            #If statement to check if user has selected Exec Timeout checkbox, if so the command will be created and inserted into the variable. Else the variable will be left blank

            if self.ids._Security_Conf_Aux_Vty_Con_Lines_Function_Select_.ids.ExecTimeoutCheckbox.active == True:
            
                exec_timeout_command = 'exec-timeout ' + self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesExecTimeoutOptionsLayout.ids.LineExecTimeoutMinutesTextInput.text + ' ' + self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesExecTimeoutOptionsLayout.ids.LineExecTimeoutSecondsTextInput.text

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

        
            config_commands = [line_command, transport_command, login_command, exec_timeout_command]
        

            net_connect = ConnectHandler(**device) 

            net_connect.send_config_set(config_commands)


            #Set the password and username back to empty after completion of configuration
            App.get_running_app().device_username = ''
            App.get_running_app().device_password = ''


            #If statement to check if VTY was the selected function, and then display the text with a line range, else it will display it as line 0
            if self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesSelectLineLayout.ids.VtyTrue.active == True:

                #Create and display a popup to inform the user of the successful configuration
                popup = Popup(title='', content=Label(markup = True, text="Successfully configured '[b]" + line_to_configure + "[/b]' Lines '[b]" +  start_line_range +" - " + end_line_range + "[/b]' on device with IP address '[b]" + device_ip_address + "[/b]'"), size_hint =(0.8, 0.3))
                popup.open()

            else:

                #Create and display a popup to inform the user of the successful configuration
                popup = Popup(title='', content=Label(markup = True, text="Successfully configured '[b]" + line_to_configure + "[/b]' Line '[b]" +  line_range + "[/b]' on device with IP address '[b]" + device_ip_address + "[/b]'"), size_hint =(0.8, 0.3))
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




    #Function linked to the Console checkbox to modify the various widgets so that only commands that can be performed on the Console line can be set - Remove and reset the Line Range text inputs as Console only allows for line 0 and modifiying which transport methods are available
    def SecurityConfAuxVtyConLinesConSelect(self):

        if self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesSelectLineLayout.ids.ConTrue.active == True:

            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesTransportOptionsLayout.ids.TransportInputOutputSpinner.text = 'Output'
            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesTransportOptionsLayout.ids.TransportInputOutputSpinner.values = ''
            

            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesTransportOptionsLayout.ids.TransportMethodNo1Spinner.values = 'SSH', 'Telnet', 'all', 'none'

        else:
            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesTransportOptionsLayout.ids.TransportInputOutputSpinner.text = 'Input'
            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesTransportOptionsLayout.ids.TransportInputOutputSpinner.values = 'Output', 'Input'

            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesTransportOptionsLayout.ids.TransportMethodNo1Spinner.values = 'SSH', 'Telnet', 'rlogin', 'all', 'none'



    #Function linked to the Aux checkbox to modify the various widgets so that only commands that can be performed on the Console line can be set - Remove and reset the Line Range text inputs as Aux only allows for line 0
    def SecurityConfAuxVtyConLinesVtySelect(self):

        if self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesSelectLineLayout.ids.VtyTrue.active == True:

            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesLineRangeLayout.opacity = 1
            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesLineRangeLayout.disabled = False
            

        else:
            
            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesLineRangeLayout.opacity = 0
            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesLineRangeLayout.disabled = True
   
            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesLineRangeLayout.ids.LineRangeStartTextInput.text = '' 
            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesLineRangeLayout.ids.LineRangeEndTextInput.text = ''



    #Function linked to the Transport checkbox to modify the Transport Method widgets so that they are visible when checked and disabled and hidden from view when unchecked, the spinners will have their values reset
    def SecurityConfAuxVtyConLinesTransportSelect(self):

        if self.ids._Security_Conf_Aux_Vty_Con_Lines_Function_Select_.ids.TransportMethodCheckbox.active == True:

            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesTransportOptionsLayout.opacity = 1
            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesTransportOptionsLayout.disabled = False

        else:

            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesTransportOptionsLayout.opacity = 0
            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesTransportOptionsLayout.disabled = True

            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesTransportOptionsLayout.ids.TransportInputOutputSpinner.text = 'Output'
            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesTransportOptionsLayout.ids.TransportMethodNo1Spinner.text = 'Method 1'
            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesTransportOptionsLayout.ids.TransportMethodNo2Spinner.text = 'Method 2'



    #Function linked to the Login checkbox to modify the Login Type widgets so that they are visible when checked and disabled and hidden from view when unchecked, the text input will have it's value reset
    def SecurityConfAuxVtyConLinesLoginTypeSelect(self):

        if self.ids._Security_Conf_Aux_Vty_Con_Lines_Function_Select_.ids.LoginTypeCheckbox.active == True:

            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesLoginOptionsLayout.opacity = 1
            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesLoginOptionsLayout.disabled = False

            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesLoginOptionsLayout.ids.LineLoginPasswordTextInput.disabled = True #Specifically disable password text input until user selects that they want to use password entry

        else:

            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesLoginOptionsLayout.opacity = 0
            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesLoginOptionsLayout.disabled = True

            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesLoginOptionsLayout.ids.LoginLocalTrue.active = True
            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesLoginOptionsLayout.ids.LineLoginPasswordTextInput.text = ''
            



    #Function linked to the ExecTimeout checkbox to modify the Exec-Timeout widgets so that they are visible when checked and disabled and hidden from view when unchecked, the text inputs will have their value reset
    def SecurityConfAuxVtyConLinesExecTimeoutSelect(self):
        

        if self.ids._Security_Conf_Aux_Vty_Con_Lines_Function_Select_.ids.ExecTimeoutCheckbox.active == True:

            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesExecTimeoutOptionsLayout.opacity = 1
            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesExecTimeoutOptionsLayout.disabled = False


        else:

            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesExecTimeoutOptionsLayout.opacity = 0
            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesExecTimeoutOptionsLayout.disabled = True
            
            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesExecTimeoutOptionsLayout.ids.LineExecTimeoutMinutesTextInput.text = ''
            self.ids._Security_Conf_Aux_Vty_Con_Lines_Layout_.ids.SecurityConfAuxVtyConLinesExecTimeoutOptionsLayout.ids.LineExecTimeoutSecondsTextInput.text = ''