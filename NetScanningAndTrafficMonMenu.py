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
from kivy.properties import StringProperty


from kivy.app import App

#Common modules will be imported to perform certain tasks if neccessary

import os
import sys
import time

#Call will be imported from subprocess to allow a cli command to be executed using python
from subprocess import call

class NetScanMenuButtons(BoxLayout):

    def NetScanWiresharkButton(self, instance):
        self.main_menu_root.manager.current = 'NetScanWiresharkScreen'



class NetScanWireshark(Screen):        
   

    #selected_storage_directory = App.get_running_app().selected_storage_directory 

    
    
	#global variables
    

	#Function to set up storage location of network traffic capture files and run a while loop till the users wishes to return to the menu

    def NetworkTrafficCapture(self):

        selected_storage_directory = App.get_running_app().selected_storage_directory


        #Creates variables that will be needed for the call process
        filenamePrefix = 'CapturedData'
        files = [0]
        pcapSuffix = '.pcap'
        

        output_name = self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkFilenameLayout.ids.WiresharkFilenameTextInput.text

        capture_interface = self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkCaptureIntLayout.ids.WiresharkCaptureInterfaceSpinner.text 

        total_duration = self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkCaptureDurationLayout.ids.WiresharkDurationTextInput.text


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




        #If statement to ensure to get the user input for amount of files to use for the buffer ring. If left at unchanged it will default to 1
        if self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferCheckbox.ids.WiresharkRingBufferFileAmountSpinner.text == 'File Amount':

            buffer_ring_file_count = 1

        else:

            buffer_ring_file_count = self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferCheckbox.ids.WiresharkRingBufferFileAmountSpinner.text





        #If else statment to check if the buffer ring check box is selected, if not it creates the tshark command without it. 
        if self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferCheckbox.ids.RingBufferCheckbox.active == True:

            #Set of if elif statements to see which settings to use for the buffer ring - Duration, Packet Amount or FileSize
            if self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferDurationCheckbox.active == True:

                ring_buffer_duration = self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferDurationTextInput.text

                tshark_commands = ["tshark", "-i", capture_interface, "-w", SaveFile, "-a", "duration:" + total_duration, "-b", "duration:" + ring_buffer_duration, "-b", "files:" + buffer_ring_file_count,"-F", "libpcap"]

            elif self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferPacketAmountCheckbox.active == True:

                ring_buffer_packet_amount = self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferPacketAmountTextInput.text

                tshark_commands = ["tshark", "-i", capture_interface, "-w", SaveFile, "-a", "duration:" + total_duration, "-b", "packets:" + ring_buffer_packet_amount, "-b", "files:" + buffer_ring_file_count,"-F", "libpcap"]

            else: #Else will deal with the File Size setting as it is the last of three and so does not need to be specified

                ring_buffer_file_size = self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferFileSizeTextInput.text

                tshark_commands = ["tshark", "-i", capture_interface, "-w", SaveFile, "-a", "duration:" + total_duration, "-b", "filesize:" + ring_buffer_file_size, "-b", "files:" + buffer_ring_file_count,"-F", "libpcap"]

        else: 

            tshark_commands = ["tshark", "-i", capture_interface, "-w", SaveFile, "-a", "duration:" + total_duration, "-F", "libpcap"]

       


        #call(tshark_commands) #Runs the commands within the tshark_commands variable using the call function from the subprocess module, it preforms the operation described above.
        #pcap = directory + '/' + filenamePrefix + pcapSuffix


        




    #Function linked to the Ring Buffer checkbox to modify the various widgets so that they are only visible and useable when the user wishes to enable ring buffer
    def NetScanWiresharkRingBufferSelect(self):

        if self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferCheckbox.ids.RingBufferCheckbox.active == True:


            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.opacity = 1
            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.disabled = False
            
            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferCheckbox.ids.WiresharkRingBufferFileAmountLabel.opacity = 1
            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferCheckbox.ids.WiresharkRingBufferFileAmountLabel.disabled = False

            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferCheckbox.ids.WiresharkRingBufferFileAmountSpinner.opacity = 1
            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferCheckbox.ids.WiresharkRingBufferFileAmountSpinner.disabled = False

            #The following ensures that the Packet Amount and File Size inputs are not displayed with the rest of the widgets, as they only display when required

            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferPacketAmountTextInput.opacity = 0
            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferPacketAmountTextInput.disabled = True
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


    #Function linked to the Packet Amount checkbox to modify the Duration Text Input so that is only visible when checked and disabled and hidden from view when unchecked
    def NetScanWiresharkRingBufferPacketAmountSelect(self):

        if self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferPacketAmountCheckbox.active == True:

            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferPacketAmountTextInput.opacity = 1
            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferPacketAmountTextInput.disabled = False

        else:

            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferPacketAmountTextInput.opacity = 0
            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferPacketAmountTextInput.disabled = True

            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferPacketAmountTextInput.text = ''


    #Function linked to the File Size checkbox to modify the Duration Text Input so that is only visible when checked and disabled and hidden from view when unchecked
    def NetScanWiresharkRingBufferFileSizeSelect(self):
        

        if self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferFileSizeCheckbox.active == True:

            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferFileSizeTextInput.opacity = 1
            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferFileSizeTextInput.disabled = False


        else:

            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferFileSizeTextInput.opacity = 0
            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferFileSizeTextInput.disabled = True
            
            self.ids._Net_Scan_Wireshark_Layout_.ids.NetScanWiresharkRingBufferLayout.ids.WiresharkRingBufferFileSizeTextInput.text = ''


    
        
   