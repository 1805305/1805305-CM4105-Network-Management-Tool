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

from multiping import MultiPing
from multiping import multi_ping

class NetTestingMenuButtons(BoxLayout):

    def NetTestingPingButton(self, instance):
        self.main_menu_root.manager.current = 'NetTestingPingScreen'


class NetTestingPing(Screen):        
    
    device_ip_address = ListProperty([''])
    result_of_ping = StringProperty('Sucess')

    def NetTestingPingExecute(self):

        #Need to add a method of ensuring only ip address or  maybe even valid domain name is entered. Probably best done with an IF statement that checks for a valid IP and if not produces a pop up saying 'Please enter a valid IP' and breaks out the function
        try:

        
            device_ip_address = self.device_ip_address
            result_of_ping = self.result_of_ping

            device_ip_address[0] = self.ids._IPv4_Target_Device_Layout_.ids.IPv4AddressTextInput.text
        
        
            retry_check = self.ids._Net_Testing_Ping_Layout_.ids.RetryAmountSpinner.text

            if retry_check == 'No Retries':
                retry_amount = 0
            else:
                retry_amount = self.ids._Net_Testing_Ping_Layout_.ids.RetryAmountSpinner.text

        
            responses, no_responses = multi_ping(device_ip_address, timeout=0.5, retry= retry_amount, ignore_lookup_errors=True)

            if responses:
                print("    reponses: %s" % list(responses.keys()))
                result_of_ping = 'Success'
            if no_responses:
                print("    no response received in time, even after retries: %s" %
                        no_responses)
                result_of_ping = 'Failed'


            if device_ip_address[0] == '':
                self.ids._Net_Testing_Ping_Layout_.ids.ResultsLabel.text = "Result of ping to '[i]Local Host[/i]' - [b] " + result_of_ping + " [/b]"
            else:       
                self.ids._Net_Testing_Ping_Layout_.ids.ResultsLabel.text = "Result of ping to '[i]" + str(device_ip_address[0]) + "[/i]' - [b] " + result_of_ping + " [/b]"



        except Exception: 
            
            self.ids._Net_Testing_Ping_Layout_.ids.ResultsLabel.text = '[b]Please enter a valid IP address and try again[/b]'