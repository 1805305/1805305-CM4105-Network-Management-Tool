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

#Common modules will be imported to perform certain tasks if neccessary

import os
from datetime import datetime

#Re module is imported to allow for strings to be searched for specified phrases

import re




class DeviceInfoMenuButtons(BoxLayout):

    def DeviceInfoPollAndExtractButton(self, instance):
        self.main_menu_root.manager.current = 'DeviceInfoPollAndExtractScreen'

    def DeviceInfoChangeControlButton(self, instance):
        self.main_menu_root.manager.current = 'DeviceInfoChangeControlScreen'


class DeviceInfoPollAndExtract(Screen):        
    

    def DeviceInfoPollAndExtractExecute(self):

        #Try statement to ensure that any errors connecting and reading the device are handled gracefully and the user is informed of what the potential error was using popups
        try:

            selected_storage_directory = App.get_running_app().selected_storage_directory #Create a local variable using the value in the global property selected_storage_directory. This will allow the script to create and store files in the directory set by the user

       
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
 

            net_connect = ConnectHandler(**device) 


            #Create variables to store the state of the data information checkboxes, this will allow them to be easily refrenced in the below if statements. This has been done to improve readablity 
            extract_hostname_selection = self.ids._Device_Info_Poll_And_Extract_Info_Select_.ids.HostnameInfoCheckbox.active
            extract_device_type_selection = self.ids._Device_Info_Poll_And_Extract_Info_Select_.ids.DeviceTypeInfoCheckbox.active
            extract_ios_version_selection = self.ids._Device_Info_Poll_And_Extract_Info_Select_.ids.IOSVersionInfoCheckbox.active
            extract_domain_selection = self.ids._Device_Info_Poll_And_Extract_Info_Select_.ids.DomainInfoCheckbox.active
            extract_uptime_selection = self.ids._Device_Info_Poll_And_Extract_Info_Select_.ids.UptimeInfoCheckbox.active


            #If statement to see if user selected Hostname checkbox, if so it will call the ExtractHostname function

            if extract_hostname_selection == True:

                output = net_connect.send_command("show version | include (uptime is)")

                hostname = self.SearchHostname(output)

            else: #Set hostname to N/A if Hostname is not required

                hostname = 'N/A'




            #If statement to see if user selected Device Type checkbox, if so it will call the ExtractHostname function

            if extract_device_type_selection == True:

                output = net_connect.send_command("show version | include (bytes of memory)")

                device_type = self.SearchDeviceType(output)

            else: #Set device_type to N/A if Device Type is not required
            
                device_type = 'N/A'




            #If statement to see if user selected IOS Version checkbox, if so it will call the ExtractHostname function

            if extract_ios_version_selection == True:

                output = net_connect.send_command("show version | include (, Version)")

                ios_version = self.SearchIOSVersion(output)

            else: #Set ios_version to N/A if IOS Version is not required
           
                ios_version = 'N/A'




            #If statement to see if user selected Domain checkbox, if so it will call the ExtractHostname function

            if extract_domain_selection == True:

                output = net_connect.send_command("show run | include domain name")
                
                domain_name = self.SearchDomain(output)

            else: #Set domain_name to N/A if Domain Name is not required
            
                domain_name = 'N/A'




            #If statement to see if user selected UpTime checkbox, if so it will call the ExtractHostname function

            if extract_uptime_selection == True:

                output = net_connect.send_command("show version | include (uptime is)")

                uptime = self.SearchUptime(output)

            else: #Set uptime to N/A if Uptime is not required
            
                uptime = 'N/A'




            #If statement to check if user requested for the output to be stored locally, if so it will store the output in a txt file. If not it is passed and nothing is done

            if self.ids._Device_Info_Poll_And_Extract_Layout_.ids.DeviceInfoPollAndExtractStoreLocalLayout.ids.StoreLocalCheckbox.active == True:


                poll_info_parent_directory = selected_storage_directory + '\\Outputs\\PollDeviceOutput\\' #Create a variable of the absolute path of where the parent directory for output of data capture will be stored
                poll_info_individual_directory = selected_storage_directory + '\\Outputs\\PollDeviceOutput\\' + device_ip_address #Create a variable of the absolute path of where the all output files for devices with the same hostname will be stored

                file_name = self.ids._Device_Info_Poll_And_Extract_Layout_.ids.DeviceInfoPollAndExtractStoreLocalLayout.ids.FileNameTextInput.text #Create a variable for the desired file name

                poll_info_output_file = poll_info_individual_directory + "/" + file_name + '.txt' #Create a variable for the name and location of the file to be saved. It will be stored as a txt file

                if not os.path.exists(poll_info_parent_directory): #Check for existence of the parent poll directory - one to store all individual directories - and if not there create it, this is done using the os.path function
                     os.makedirs(poll_info_parent_directory)
                else:
                     pass

                if not os.path.exists(poll_info_individual_directory): #Check for existence of the individual poll directory - One to store the current output - and if not there create it, this is done using the os.path function
                    os.makedirs(poll_info_individual_directory)
                else:
                    pass



                #Create a list variable to store the outputs required requested by the user, this will then be written into the file specified by the user
                poll_info_output_store_local = ['Hostname: ' + hostname, 'Device Type: ' + device_type, 'IOS Version: ' + ios_version, 'Domain: ' + domain_name, 'Uptime: ' + uptime]

                with open(poll_info_output_file, 'w') as f: 

                    f.write('\n'.join(poll_info_output_store_local) + '\n') #Write each entry of poll_info_output_store_local list in the specified file on a seperate line

                f.close()

            else:
                pass


            #The following two will update the label to display the IP address of the device that was polled. As well as the text input to display the requested info or input 'N/A' if the user did not request the info
            self.ids._Device_Info_Poll_And_Extract_Layout_.ids.PolledDeviceInfoLabel.text = 'Device Information for IP Address - [b]' + device_ip_address + '[/b]' 
            self.ids._Device_Info_Poll_And_Extract_Layout_.ids.PolledDeviceInfoOutput.text = 'Hostname: ' + hostname + ' \nDevice Type: ' + device_type + '\nIOS Version: ' + ios_version + '\nDomain: ' + domain_name + '\nUptime: ' + uptime
        

        #Except error to catch when Credentials are incorrect, informs the user of the error using a popup defined in the MainApplication.kv
        except AuthenticationException:

            Factory.NetmikoAuthenticateFailurePopup().open()

        #Except error to catch when Netmiko timeouts and is unable to connect to device, informs the user of the error using a popup defined in the MainApplication.kv
        except NetMikoTimeoutException:

            Factory.NetmikoTimeoutPopup().open()



    #Function linked to the Local Store checkbox to modify the various widgets so that they are only visible and useable when the user wishes to store the output from device polling
    def DeviceInfoPollAndExtractStoreLocalSelect(self):

        if self.ids._Device_Info_Poll_And_Extract_Layout_.ids.DeviceInfoPollAndExtractStoreLocalLayout.ids.StoreLocalCheckbox.active == True:

            
            self.ids._Device_Info_Poll_And_Extract_Layout_.ids.DeviceInfoPollAndExtractStoreLocalLayout.ids.FileNameLabel.opacity = 1
            self.ids._Device_Info_Poll_And_Extract_Layout_.ids.DeviceInfoPollAndExtractStoreLocalLayout.ids.FileNameLabel.disabled = False

            self.ids._Device_Info_Poll_And_Extract_Layout_.ids.DeviceInfoPollAndExtractStoreLocalLayout.ids.FileNameTextInput.opacity = 1
            self.ids._Device_Info_Poll_And_Extract_Layout_.ids.DeviceInfoPollAndExtractStoreLocalLayout.ids.FileNameTextInput.disabled = False


        else:

            
            self.ids._Device_Info_Poll_And_Extract_Layout_.ids.DeviceInfoPollAndExtractStoreLocalLayout.ids.FileNameLabel.opacity = 0
            self.ids._Device_Info_Poll_And_Extract_Layout_.ids.DeviceInfoPollAndExtractStoreLocalLayout.ids.FileNameLabel.disabled = True

            self.ids._Device_Info_Poll_And_Extract_Layout_.ids.DeviceInfoPollAndExtractStoreLocalLayout.ids.FileNameTextInput.opacity = 0
            self.ids._Device_Info_Poll_And_Extract_Layout_.ids.DeviceInfoPollAndExtractStoreLocalLayout.ids.FileNameTextInput.disabled = True

            self.ids._Device_Info_Poll_And_Extract_Layout_.ids.DeviceInfoPollAndExtractStoreLocalLayout.ids.FileNameTextInput.text = ''
        



    #Function to search output for the Hostname of a device and return it
    def SearchHostname(self, output):

        if re.search("(.+) uptime is", output) == None: #If regex search finds no matches in string then set hostname as 'unknown'
            hostname = "N/"
        else: #Else if regex search finds any matches then do the following
            dev_hostname = re.search("(.+) uptime is", output) #Set variable dev_hostname as the output of regex search on the output from the device
            hostname = dev_hostname.group(1) #Set variable hostname as the first match from the regex search
            hostname = str(hostname) #Convert variable to string

        return hostname #Return variable hostname to function that called it

    

    
    #Function to search output for the IOS Version of a device and return it
    def SearchIOSVersion(self, output):

        if re.search("\), Version (.+),", output) == None: #If regex search finds no matches in string then set uptime as 'unknown'
            ios_version = "N/A"
        else: #Else if regex search finds any matches then do the following
            dev_version = re.search("\), Version (.+),", output) #Set variable dev_uptime as the output of regex search on the output from the device
            ios_version = dev_version.group(1)#Set variable uptime as the first match from the regex search
            ios_version = str(ios_version) #Convert variable to string

        return ios_version #Return variable ios to function that called it




    #Function to search output for the Device Type of a device and return it
    def SearchDeviceType(self, output):

        if re.search("(.+?) (.+?) (.+?) (.+) bytes of memory", output) == None:  #If regex search finds no matches in string then set model as 'unknown'
            device_type = "N/A"
        else: #Else if regex search finds any matches then do the following
            dev_model = re.search("(.+?) (.+?) (.+) bytes of memory", output) #Set variable dev_model as the output of regex search on the output from the device
            device_type = dev_model.group(1)+ ' ' + dev_model.group(2) #Set variable model as the first match from the regex search
            device_type = str(device_type) #Convert variable to string

        return device_type #Return variable model to function that called it




    #Function to search output for the Domain of a device and return it
    def SearchDomain(self, output):

        if re.search("ip domain name (.+)", output) == None: #If regex search finds no matches in string then set domain_name as 'unknown'
            domain_name = "N/A"
        else: #Else if regex search finds any matches then do the following
            dev_domain = re.search("ip domain name (.+)", output) #Set variable dev_domain as the output of regex search on the output from the device
            domain_name = dev_domain.group(1)#Set variable ios as the first match from the regex search
            domain_name = str(domain_name) #Convert variable to string

        return domain_name #Return variable domain_name to function that called it




    #Function to search output for the Uptime of a device and return it
    def SearchUptime(self, output):

        if re.search("uptime is (.+)", output) == None: #If regex search finds no matches in string then set uptime as 'unknown'
            uptime = "N/A"
        else: #Else if regex search finds any matches then do the following
            dev_uptime = re.search("uptime is (.+)", output) #Set variable dev_uptime as the output of regex search on the output from the device
            uptime = dev_uptime.group(1)#Set variable uptime as the first match from the regex search
            uptime = str(uptime) #Convert variable to string

        return uptime #Return variable uptime to function that called it







class DeviceInfoChangeControlMenuButtons(BoxLayout):

    def DeviceInfoChangeControlSaveConfButton(self, instance):
        self.main_menu_root.manager.current = 'DeviceInfoChangeControlSaveConfScreen'

    def DeviceInfoChangeControlUploadConfButton(self, instance):
        self.main_menu_root.manager.current = 'DeviceInfoChangeControlUploadConfScreen'

    def DeviceInfoChangeControlCompareConfButton(self, instance):
        self.main_menu_root.manager.current = 'DeviceInfoChangeControlCompareConfScreen'


class DeviceInfoChangeControlSaveConf(Screen):        
     

    def DeviceInfoChangeControlSaveConfExecute(self):

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


            device = { 
              'device_type': 'cisco_ios', 
              'ip': device_ip_address, 
              'username': 'Test', 
              'password': 'cisco123', 
              } 

            net_connect = ConnectHandler(**device) #Connect to the device using the credentials and IP address

            if self.ids._Device_Info_Change_Control_Save_Conf_Layout_.ids.RunningTrue.active == True:

                self.SaveDeviceRunConf(net_connect)

            else:

                self.SaveDeviceStartupConf(net_connect)
  

        #Except error to catch when Credentials are incorrect, informs the user of the error using a popup defined in the MainApplication.kv
        except AuthenticationException:

            Factory.NetmikoAuthenticateFailurePopup().open()

        #Except error to catch when Netmiko timeouts and is unable to connect to device, informs the user of the error using a popup defined in the MainApplication.kv
        except NetMikoTimeoutException:

            Factory.NetmikoTimeoutPopup().open()

        


    def SaveDeviceRunConf(self, net_connect):      
        

        #Try statement to ensure that any errors connecting and configuring the device are handled gracefully and the user is informed of what the potential error was using popups
        try: 

            selected_storage_directory = App.get_running_app().selected_storage_directory #Create a local variable using the value in the global property selected_storage_directory. This will allow the script to create and store files in the directory set by the user

            output = net_connect.send_command("show version | include (uptime is)")

            hostname = DeviceInfoPollAndExtract.SearchHostname(self, output) #Sets hostname as output from search_hostname function - This function is designed to find and return the hostname of a device using regex

            date = datetime.now().strftime("%Y-%m-%d_%I-%M-%S_%p")


            run_conf_parent_directory = selected_storage_directory + '\\Outputs\\SaveConfOutput\\' #Create a variable of the absolute path of where the parent directory for output of data capture will be stored
            run_conf_individual_directory = selected_storage_directory + '\\Outputs\\SaveConfOutput\\' + hostname + '\\RunningConf' #Create a variable of the absolute path of where the running configurations files for devices with the same hostname will be stored

            run_conf_output_file = run_conf_individual_directory + "/" + hostname + '_' + date + '_RunningConfiguration.txt' #Create a variable for the name and location of the file to be saved. It will be stored as a txt file

            if not os.path.exists(run_conf_parent_directory): #Check for existence of the parent poll directory - one to store all individual directories - and if not there create it, this is done using the os.path function
                    os.makedirs(run_conf_parent_directory)
            else:
                    pass

            if not os.path.exists(run_conf_individual_directory): #Check for existence of the individual poll directory - One to store the current output - and if not there create it, this is done using the os.path function
                os.makedirs(run_conf_individual_directory)
            else:
                pass


            #show and save running conf of routing device

            net_connect.send_command('skip-page-display')

            output_save_conf = net_connect.send_command('show running-config')
        


            file = open(run_conf_output_file, 'w') #Set variable file_run to create/Open new/exisitng file and allow it to be written to

            file.write(output_save_conf) #Write output from running config from device into the file

            file.close() #Close file

            popup = Popup(title='', content=Label(markup = True, text="Successfully saved the '[b]Running Configuration[/b]' of device with hostname '[b]" + hostname + "[/b]'"), size_hint =(0.8, 0.3))
            popup.open()


        #Except error to catch when Netmiko timeouts and is unable to connect to device, informs the user of the error using a popup defined in the MainApplication.kv
        except NetMikoTimeoutException:

            Factory.NetmikoTimeoutPopup().open()







    #Function to save a device startup configuration to a file

    def SaveDeviceStartupConf(self, net_connect):      
        
        #Try statement to ensure that any errors connecting and configuring the device are handled gracefully and the user is informed of what the potential error was using popups
        try: 

            selected_storage_directory = App.get_running_app().selected_storage_directory #Create a local variable using the value in the global property selected_storage_directory. This will allow the script to create and store files in the directory set by the user

            output = net_connect.send_command("show version | include (uptime is)")

            hostname = DeviceInfoPollAndExtract.SearchHostname(self, output) #Sets hostname as output from search_hostname function - This function is designed to find and return the hostname of a device using regex

            date = datetime.now().strftime("%Y-%m-%d_%I-%M-%S_%p")


            start_conf_parent_directory = selected_storage_directory + '\\Outputs\\SaveConfOutput\\' #Create a variable of the absolute path of where the parent directory for output of data capture will be stored
            start_conf_individual_directory = selected_storage_directory + '\\Outputs\\SaveConfOutput\\' + hostname + '\\StartupConf' #Create a variable of the absolute path of where the running configurations files for devices with the same hostname will be stored

            start_conf_output_file = start_conf_individual_directory + "/" + hostname + '_' + date + '_StartupConfiguration.txt' #Create a variable for the name and location of the file to be saved. It will be stored as a txt file

            if not os.path.exists(start_conf_parent_directory): #Check for existence of the parent poll directory - one to store all individual directories - and if not there create it, this is done using the os.path function
                    os.makedirs(start_conf_parent_directory)
            else:
                    pass

            if not os.path.exists(start_conf_individual_directory): #Check for existence of the individual poll directory - One to store the current output - and if not there create it, this is done using the os.path function
                os.makedirs(start_conf_individual_directory)
            else:
                pass


            #show and save running conf of routing device

            net_connect.send_command('skip-page-display')

            output_save_conf = net_connect.send_command('show startup-config')
        


            file = open(start_conf_output_file, 'w') #Set variable file_run to create/Open new/exisitng file and allow it to be written to

            file.write(output_save_conf) #Write output from running config from device into the file

            file.close() #Close file

            popup = Popup(title='', content=Label(markup = True, text="Successfully saved the '[b]Startup Configuration[/b]' of device with hostname '[b]" + hostname + "[/b]'"), size_hint =(0.8, 0.3))
            popup.open()


        #Except error to catch when Netmiko timeouts and is unable to connect to device, informs the user of the error using a popup defined in the MainApplication.kv
        except NetMikoTimeoutException:

            Factory.NetmikoTimeoutPopup().open()



class DeviceInfoChangeControlUploadConf(Screen):        
    

    def DeviceInfoChangeControlUploadConfExecute(self):

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


            device = { 
              'device_type': 'cisco_ios', 
              'ip': device_ip_address, 
              'username': 'Test', 
              'password': 'cisco123', 
              } 

            

            net_connect = ConnectHandler(**device) 

            selected_conf_file = str(self.ids._Device_Info_Change_Control_Upload_Conf_Layout_.ids.FileChooser.selection[0])

            with open(selected_conf_file, 'r') as f: #user_path is the variable i defined which takes the path of file(configuration file) as raw input from the user.
                config_commands = f.readlines()


            net_connect.send_config_set(config_commands)

    
            #Create and display a popup to inform the user of the successful configuration
            popup = Popup(title='', content=Label(markup = True, text="Successfully uploaded configuration file to device with IP address '[b]" + device_ip_address + "[/b]'"), size_hint =(0.7, 0.3))
            popup.open()
        

        #Except error to catch when Credentials are incorrect, informs the user of the error using a popup defined in the MainApplication.kv
        except AuthenticationException:

            Factory.NetmikoAuthenticateFailurePopup().open()

        #Except error to catch when Netmiko timeouts and is unable to connect to device, informs the user of the error using a popup defined in the MainApplication.kv
        except NetMikoTimeoutException:

            Factory.NetmikoTimeoutPopup().open()



       

        

    

class DeviceInfoChangeControlCompareConf(Screen):        
    
   def DeviceInfoChangeControlCompareConfExecute(self):
       pass

    




    
        

   