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

from kivy.properties import ListProperty, StringProperty

from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.uix.label import Label 


#Import multiping to allow for the sending of pings and the gathering of the results

from multiping import MultiPing
from multiping import multi_ping

#Imports ipaddress to provide the ability to maniuplate IP addresses

import ipaddress


#Creates the class that inherits from the BoxLayout class, this class provides the functions to swtich to screens as required

class NetTestingMenuButtons(BoxLayout):

    def NetTestingPingButton(self, instance):
        self.main_menu_root.manager.current = 'NetTestingPingScreen'


#Create the class for the 'Ping A Network Device' Screen using the Screen class for inheritiance

class NetTestingPing(Screen):        
    

    #Defines the properties used throughout the class

    device_ip_address = ListProperty([''])
    result_of_ping = StringProperty('')


    #Creates the function to execute the Ping Device function

    def NetTestingPingExecute(self):
        
        #Defines the variables based on properties set above

        device_ip_address = self.device_ip_address
        result_of_ping = self.result_of_ping

            
        #Try statement to ensure the IP address entered is valid. If it is an invalid address the ipaddress module will raise a value error, at which point the user is informed that a valid IP address is required using a popup
        try:

            device_ip_address[0] = self.ids._IPv4_Target_Device_Layout_.ids.IPv4AddressTextInput.text
            ipaddress.ip_address(device_ip_address[0])

        #ipaddress raises a value error when an invalid IP address is used
        except ValueError:

            Factory.InvalidIPAddressPopup().open() 
            return #Exit from the function

        
        retry_amount = self.ids._Net_Testing_Ping_Layout_.ids.RetryAmountSpinner.text #retry_amount is set a the value of the retry spinner

        #If statement to check if the user set a retry anount, if not the retry amount is set to 0
        if retry_amount == 'No Retries':
            retry_amount = 0
        else:
           pass

        
       #Intiates the ping using the variables set, the responses will be outputted to 'responses' and 'no_response' depending if a response to the ping is recieved
        responses, no_responses = multi_ping(device_ip_address, timeout=0.5, retry= retry_amount, ignore_lookup_errors=True)

        #If statement to check the result of the ping
        if responses: #If a respone is found it is set as successful
            result_of_ping = 'Success'
        if no_responses: #If no response is found it is set as failed
            result_of_ping = 'Failed'

        self.ids._Net_Testing_Ping_Layout_.ids.ResultsLabel.text = "Result of ping to '[i]" + str(device_ip_address[0]) + "[/i]' - [b] " + result_of_ping + " [/b]" #Sets the label on the screen stating the device pinged and the result of the ping
