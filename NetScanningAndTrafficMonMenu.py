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
from kivy.properties import StringProperty

from kivy.app import App


#Common modules will be imported to perform certain tasks if neccessary

import os
from datetime import datetime

#Call will be imported from subprocess to allow CLI commands to be executed using python

from subprocess import call

#Import netifaces and winref to discover the interfaces on the computer to allow dynamic population of the network interface spinner

import netifaces
import winreg


#Creates the class that inherits from the BoxLayout class, this class provides the functions to swtich to screens as required

class NetScanMenuButtons(BoxLayout):

    def NetScanWiresharkButton(self, instance):
        self.main_menu_root.manager.current = 'NetScanWiresharkScreen'





#Create the class for the 'Capture Network Traffic Using Wireshark' Screen using the Screen class for inheritiance

class NetScanWireshark(Screen):        
   

    #Function to get the network interfaces present on the device using netifaces.interfaces()
    
    def NetScanWiresharkPopulateNetworkInterfaces(self):

        x = netifaces.interfaces() #Sets 'x' as the output from netifaces.interfaces()

        network_interfaces = self.get_connection_name_from_guid(x) #Sets network_interfaces as the output from get_connection_name_from_guid, this function is needed on windows OS to convert the GUID that is returned with with netifaces.interfaces() 

        #If statement to check if an interface has been categorised as unknown and if so remove it
        if '(unknown)' in network_interfaces:

            network_interfaces.remove('(unknown)')

        else: 
            pass

        self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkCaptureIntLayout.ids.WiresharkCaptureInterfaceSpinner.values = network_interfaces #Set the values for WiresharkCaptureInterfaceSpinner to the list returned by get_connection_name_from_guid(). This will allow for the spinner to dynamically change dependent on what network interfaces the user has 

        

    #Function provided by Gord Thompson and posted on StackOverflow to convert the GUID provided by netifaces.interfaces() to the actual interface names. The link to the orignal post can be found at https://stackoverflow.com/questions/29913516/how-to-get-meaningful-network-interface-names-instead-of-guids-with-netifaces-un
    def get_connection_name_from_guid(self, iface_guids):
        iface_names = ['(unknown)' for i in range(len(iface_guids))]
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        reg_key = winreg.OpenKey(reg, r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}')
        for i in range(len(iface_guids)):
            try:
                reg_subkey = winreg.OpenKey(reg_key, iface_guids[i] + r'\Connection')
                iface_names[i] = winreg.QueryValueEx(reg_subkey, 'Name')[0]
            except FileNotFoundError:
                pass
        return iface_names
        

	#Function to capture network using TShark, it is written as wireshark in text to the user as this is the main GUI version of the process and would be more recognised than Tshark, the output from the function can be viewed on wireshark when required

    def NetworkTrafficCapture(self):

        selected_storage_directory = App.get_running_app().selected_storage_directory


        #Creates variables that will be needed for the call process
        filenamePrefix = 'CapturedData'
        files = [0]
        pcapSuffix = '.pcap'
        

        #If statement to check if user has entered an output name, if not the current time and date will be used
        if self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkFilenameLayout.ids.WiresharkFilenameTextInput.text == '':

            output_name = datetime.now().strftime("%Y-%m-%d_%I-%M-%S_%p")

        else:

            output_name = self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkFilenameLayout.ids.WiresharkFilenameTextInput.text



        shark_parent_directory = selected_storage_directory + '\\Outputs\\NetTrafficTSharkOutput\\' #Create a variable of the absolute path of where the parent directory for output of data capture will be stored
        shark_individual_directory = selected_storage_directory + '\\Outputs\\NetTrafficTSharkOutput\\' + output_name #Create a variable of the absolute path of where the data capture files will be stored


        if not os.path.exists(shark_parent_directory): #Check for existence of the parent shark directory - one to store all individual directories - and if not there create it, this is done using the os.path function
             os.makedirs(shark_parent_directory)
        else:
             pass

        if not os.path.exists(shark_individual_directory): #Check for existence of the individual directory - One to store the current output -and if not there create it, this is done using the os.path function
            os.makedirs(shark_individual_directory)
        else:
            pass




        SaveFile = shark_individual_directory + "/" + filenamePrefix + pcapSuffix #Create variable for location for data capture 





        #If statement to get user input on interface to capture traffic on, if unselected it will default to the first value
        if self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkCaptureIntLayout.ids.WiresharkCaptureInterfaceSpinner.text == 'Network Interface':

            capture_interface = self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkCaptureIntLayout.ids.WiresharkCaptureInterfaceSpinner.values[0]

        else: 

            capture_interface = self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkCaptureIntLayout.ids.WiresharkCaptureInterfaceSpinner.text



        #If statement to get user input on duration to capture traffic on, if unselected it will default to the 10 secs
        if self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkCaptureDurationLayout.ids.WiresharkDurationTextInput.text == '':

           total_duration = '10'

        else:  
            
            total_duration = self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkCaptureDurationLayout.ids.WiresharkDurationTextInput.text



        #If statement to ensure to get the user input for amount of files to use for the buffer ring. If left at unchanged it will default to 1
        if self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferCheckbox.ids.WiresharkRingBufferFileAmountSpinner.text == 'File Amount':

            buffer_ring_file_count = '1'

        else:

            buffer_ring_file_count = self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferCheckbox.ids.WiresharkRingBufferFileAmountSpinner.text





        #If else statment to check if the buffer ring check box is selected, if not it creates the tshark command without it. 
        if self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferCheckbox.ids.RingBufferCheckbox.active == True:

            #If Else statements to see which settings to use for the buffer ring - Duration or FileSize
            if self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferDurationCheckbox.active == True:

                ring_buffer_duration = self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferDurationTextInput.text

                tshark_commands = ["C:\\Program Files\\Wireshark\\tshark.exe", "-i", capture_interface, "-w", SaveFile, "-a", "duration:" + total_duration, "-b", "duration:" + ring_buffer_duration, "-b", "files:" + buffer_ring_file_count,"-F", "libpcap"]


            else: #Else will deal with the File Size setting as it is the last of two and so does not need to be specified

                ring_buffer_file_size = self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferFileSizeTextInput.text

                tshark_commands = ["C:\\Program Files\\Wireshark\\tshark.exe", "-i", capture_interface, "-w", SaveFile, "-a", "duration:" + total_duration, "-b", "filesize:" + ring_buffer_file_size, "-b", "files:" + buffer_ring_file_count,"-F", "libpcap"]

        else: 

            tshark_commands = ["C:\\Program Files\\Wireshark\\tshark.exe", "-i", capture_interface, "-w", SaveFile, "-a", "duration:" + total_duration]
           

        self.ids.NetScanWiresharkStatusOfMonitorLayout.ids.StatusOfMonitorInterfaceLabel.text = "Network Capture Intiated on interface -[b] " + capture_interface + " [/b]" #Set the info label at the top of the screen to inform user of most recent capture
       
        self.ids.NetScanWiresharkStatusOfMonitorLayout.ids.StatusOfMonitorStorageLabel.text = "Captured file/s can be found at -[b] " + shark_individual_directory + " [/b]" #Set the info label at the top of the screen to inform user of most recent capture


        call(tshark_commands) #Runs the commands within the tshark_commands variable using the call function from the subprocess module, it preforms the operation described above.


               
        

    #Function linked to the Ring Buffer checkbox to modify the various widgets so that they are only visible and useable when the user wishes to enable ring buffer
    def NetScanWiresharkRingBufferSelect(self):

        if self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferCheckbox.ids.RingBufferCheckbox.active == True:


            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.opacity = 1
            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.disabled = False
            
            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferCheckbox.ids.WiresharkRingBufferFileAmountLabel.opacity = 1
            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferCheckbox.ids.WiresharkRingBufferFileAmountLabel.disabled = False

            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferCheckbox.ids.WiresharkRingBufferFileAmountSpinner.opacity = 1
            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferCheckbox.ids.WiresharkRingBufferFileAmountSpinner.disabled = False

            #The following ensures that the File Size inputs are not displayed with the rest of the widgets, as they only display when required

            
            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferFileSizeTextInput.opacity = 0
            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferFileSizeTextInput.disabled = True

        else:
            
            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.opacity = 0
            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.disabled = True

            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferCheckbox.ids.WiresharkRingBufferFileAmountLabel.opacity = 0
            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferCheckbox.ids.WiresharkRingBufferFileAmountLabel.disabled = True

            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferCheckbox.ids.WiresharkRingBufferFileAmountSpinner.opacity = 0
            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferCheckbox.ids.WiresharkRingBufferFileAmountSpinner.disabled = True

            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferDurationCheckbox.active = True #Ensure that the Duration checkbox is active by default

            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferCheckbox.ids.WiresharkRingBufferFileAmountSpinner.text = 'File Amount' #Reset the text value of the spinner to default




    #Function linked to the Duration checkbox to modify the Duration Text Input so that is only visible when checked and disabled and hidden from view when unchecked
    def NetScanWiresharkRingBufferDurationSelect(self):

        if self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferDurationCheckbox.active == True:

            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferDurationTextInput.opacity = 1
            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferDurationTextInput.disabled = False

        else:

            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferDurationTextInput.opacity = 0
            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferDurationTextInput.disabled = True

            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferDurationTextInput.text = ''


    


    #Function linked to the File Size checkbox to modify the File Size Text Input so that is only visible when checked and disabled and hidden from view when unchecked
    def NetScanWiresharkRingBufferFileSizeSelect(self):
        

        if self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferFileSizeCheckbox.active == True:

            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferFileSizeTextInput.opacity = 1
            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferFileSizeTextInput.disabled = False


        else:

            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferFileSizeTextInput.opacity = 0
            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferFileSizeTextInput.disabled = True
            
            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferFileSizeTextInput.text = ''


    
        
   