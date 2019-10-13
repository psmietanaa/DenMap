#!/usr/bin/env python3

import argparse
import mail
import requests
import savelog
from scapy.all import *
import socket

# This machine's IP address
myIP = socket.gethostbyname(socket.gethostname())

# These IPs that will not be reported as attackers
whitelist = []

# These IPs will be immediately blocked
blacklist = []


# Console colors
class Colors:
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# This function analyzes network traffic
def analyze(result):
    # Create a map of source IPs and scanned ports
    tracker = {}
    for event in result:
        # Ignore our own scans
        if event[0] == myIP:
            continue
        # Ignore hosts that are on a whitelist
        elif event[0] in whitelist:
            continue
        else:
            # Track the source and destination ports
            try:
                tracker[event[0]].append(event[3])
            except KeyError:
                tracker[event[0]] = [event[3]]
    # Check for suspicious activity
    for key, values in tracker.items():
        # The ip has already been banned
        if key in blacklist:
            continue
        # Check for Nmap scan
        if len(values) >= 50:
            # Get geolocation using API
            response = requests.get('http://api.ipstack.com/' + str(key) + '?access_key=bd022cef1196f511e09a901936bb222d')
            data = response.json()
            # Create email
            content = " Ports scanned by the attacker: " + str(values)
            subject = str(key) + " (" + str(data['city']) + ", " + str(data['region_name']) + ", " + str(data['country_name']) + ") tried to perform Nmap scan and has been banned!"
            # Print output to console
            # print(Colors.BOLD + Colors.FAIL + subject + Colors.END)
            print(subject)
            # Send an email alert
            mail.send_mail(content, subject)
            # Write this information to log
            savelog.write_log(subject + " " + content)
            # Block the ip for future use
            block_ip(key)
        # Check if a host scanned more than 10 ports within 10 seconds
        elif len(values) >= 20:
            # Get geolocation using API
            response = requests.get('http://api.ipstack.com/' + str(key) + '?access_key=bd022cef1196f511e09a901936bb222d')
            data = response.json()
            subject = str(key) + " (" + str(data['city']) + ", " + str(data['region_name']) + ", " + str(data['country_name']) + ") attempted to connect to " + str(len(values) // 2) + " closed ports!"
            # Print output to console
            # print(Colors.BOLD + Colors.WARNING + subject + Colors.END)
            print(subject)
            # Write this information to log
            savelog.write_log(subject + " " + str(values))


# Block an ip address using iptables
def block_ip(ip):
    blacklist.append(ip)
    command = "sudo iptables -I INPUT -s " + str(ip) + " -j DROP"
    os.system(command)


# Unblock an ip address using iptables
def unblock_ip(ip):
    blacklist.remove(ip)
    command = "sudo iptables -D INPUT -s " + str(ip) + " -j DROP"
    os.system(command)


# Main function
def main():
    # Parse any command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--interface", type=str, default='enp0s3', help='This is the interface you want to sniff packets on')
    parser.add_argument("--interval", type=int, default=10, help='This is the interval between analyzing packets')
    args = parser.parse_args()
    # Check if interval has correct range
    if args.interval < 1 or args.interval > 100:
        parser.error("The interval has to be in range [1,100)")

    # Print the logo
    # print(Colors.BOLD + Colors.WARNING + "-" * 30)
    # print("        DenMap Active")
    # print("-" * 30 + Colors.END)

    # Sniff packets continuously in 10 second intervals
    while True:
        packets = sniff(iface=args.interface, filter="tcp", timeout=args.interval)
        result = []
        for packet in packets:
            source_ip = packet['IP'].src
            destination_ip = packet['IP'].dst
            source_port = packet['TCP'].sport
            destination_port = packet['TCP'].dport
            result.append([source_ip, destination_ip, source_port, destination_port])
        analyze(result)
