#!/usr/bin/python2
import subprocess
import sys, os, errno
import base64
from Crypto.Cipher import AES
from CipherText import *

users_dir_name = "sirs_users"

def printTitle(text):
	command = "toilet -t -f future "
	subprocess.call("clear", shell=True)
	subprocess.call(command + text, shell=True)

def makedirs_p(path):
    try:
        os.makedirs(path, 0700)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def show_menu(question, options):
	error_string4 = ""
	while True:
		print question
		counter = 1
		for option in options:
			option_string = "(" + str(counter) + ") " + option
			print option_string
			counter += 1
		print "(0) Exit"
		print error_string4
		
		try:
			response4 = int(raw_input("Enter a number: "))
		except ValueError:
			error_string4 = "Oops!  That was no valid number.  Try again..."
			continue

		if response4 > 0 and response4 < len(options)+1:
		    return response4
		elif response4 == 0:
		    printTitle("Bye Bye")
		    sys.exit(0)
		else:
			error_string4 = "Oops!  That was no valid option.  Try again..."
			continue

def choose_devices():
	print "Scanning, please wait"
	scan_command = "hcitool scan | grep -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}' | sed 's/\t/ /g'"
	ps = subprocess.Popen(scan_command, shell=True, stdout=subprocess.PIPE)

	lines = []
	for line in iter(ps.stdout.readline, ''):
			lines.append(line.rstrip())

	error_string3 = ""
	while True:
		print "Choose your device:"
		print error_string3
		device_number = 1
		for line in lines:
			device_id = "(" + str(device_number) + ")"
			print device_id+lines[device_number-1]
			device_number=device_number+1
		print "(0) Exit"

		try:
			response3 = int(raw_input("Enter a number: "))
		except ValueError:
			error_string3 = "Oops!  That was no valid number.  Try again..."
			continue

		if response3 > 0 and response3 <= len(lines):
			return lines[response3-1][1:18]
		elif response3 == 0:
		    printTitle("Bye Bye")
		    sys.exit(0)
		else:
			error_string = "Oops!  That was no valid option.  Try again..."
			continue

def generate_show_key(user_dir):
	key = generate_key()
	print "This is the key (in base64): ", base64.b64encode(key)
	key_file = open(user_dir + "/key", "w+")
	key_file.write(key)
	key_file.close()

def create_allowed_sites_file(user_dir):
	open(user_dir + "/allowed_sites", 'a').close()

# Set Up Function
def setup():
	printTitle("Set Up")
	device_MAC = choose_devices()
	print device_MAC
	user_dir = users_dir_name + "/" + device_MAC
	makedirs_p(user_dir)
	generate_show_key(user_dir)
	create_allowed_sites_file(user_dir)
	if show_menu("Start Executing?", ["Run Program"]) == 1:
		execute()
	sys.exit(0)

# Execute Function #
def execute():
	printTitle("Executing")
	sys.exit(0)

# Main Function #
def main():
	error_string = ""
	while True:
		printTitle("SIRS Project 2014 - Group 8 - MEIC-A")
		print "What do you want to do?"
		print "(1) Set Up - New User"
		print "(2) Run Program"
		print "(0) Exit"
		print error_string

		try:
			response = int(raw_input("Enter a number: "))
		except ValueError:
			error_string = "Oops!  That was no valid number.  Try again..."
			continue

		if response == 1:
			setup()
		elif response == 2:
		    execute()
		elif response == 0:
		    printTitle("Bye Bye")
		    sys.exit(0)
		else:
			error_string = "Oops!  That was no valid option.  Try again..."
			continue

if __name__ == "__main__":
	main()