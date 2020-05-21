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

from kivy.properties import ListProperty, StringProperty

from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.uix.label import Label 

from multiping import MultiPing
from multiping import multi_ping

import ipaddress

class NetTestingMenuButtons(BoxLayout):

    def NetTestingPingButton(self, instance):
        self.main_menu_root.manager.current = 'NetTestingPingScreen'


class NetTestingPing(Screen):        
    
    device_ip_address = ListProperty([''])
    result_of_ping = StringProperty('')

    def NetTestingPingExecute(self):
        
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

        
        retry_check = self.ids._Net_Testing_Ping_Layout_.ids.RetryAmountSpinner.text

        if retry_check == 'No Retries':
            retry_amount = 0
        else:
            retry_amount = self.ids._Net_Testing_Ping_Layout_.ids.RetryAmountSpinner.text

        
        responses, no_responses = multi_ping(device_ip_address, timeout=0.5, retry= retry_amount, ignore_lookup_errors=True)

        if responses:
            result_of_ping = 'Success'
        if no_responses:
            result_of_ping = 'Failed'

        self.ids._Net_Testing_Ping_Layout_.ids.ResultsLabel.text = "Result of ping to '[i]" + str(device_ip_address[0]) + "[/i]' - [b] " + result_of_ping + " [/b]"
