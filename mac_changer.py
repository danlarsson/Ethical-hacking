#!/usr/bin/env python

import random
import subprocess
import optparse
import re

def change_mac(interface, new_mac):
    print('[+] Changing MAC addess for ' + interface + ' to ' + new_mac)

    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])

    
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(['ifconfig', interface])
    mac_address_search_result = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w\:\w\w', ifconfig_result)
    if not mac_address_search_result:
        print('[-] No MAC address on interface: ' + interface)
        exit()
        
    return(mac_address_search_result.group(0))
    
    
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface', help='Interface to change its MAC address')
    parser.add_option('-m', '--mac', dest='new_mac', help='Ner MAC adress, leave blank to randomize')
    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error('[-] You have to specify a intereface with -i')
    elif not options.new_mac:
        # Randomize the mac address if the user not specify one.
        options.new_mac = ':'.join(("%012x" % random.randint(0, 0xFFFFFFFFFFFF))[i:i+2] for i in range(0, 12, 2))

    return(options)


options = get_arguments()

print('[+] Original MAC address: ' + get_current_mac(options.interface))
change_mac(options.interface, options.new_mac)
if get_current_mac(options.interface) == options.new_mac:
    print('[+] MAC address was changed to: ' + options.new_mac)
else:
    print('[-] MAC address was not changed')

