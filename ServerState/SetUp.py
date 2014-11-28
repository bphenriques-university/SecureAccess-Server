#!/usr/bin/python2
import subprocess
import sys, os, errno
import base64
from Crypto.Cipher import AES

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

def post_setup_menu():
	error_string2 = ""
	while True:
		print "Start executing?"
		print "(1) Run Program"
		print "(0) Exit"
		print error_string2
		
		try:
			response2 = int(raw_input("Enter a number: "))
		except ValueError:
			error_string2 = "Oops!  That was no valid number.  Try again..."
			continue

		if response2 == 1:
		    execute()
		elif response2 == 0:
		    printTitle("Bye Bye")
		    sys.exit(0)
		else:
			error_string2 = "Oops!  That was no valid option.  Try again..."
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
	print "#generate key"
	print "#show key"
	key_file = open(user_dir + "/key", "w+")
	key_file.write("this is the key\n")
	key_file.close()

def write_allowed_sites(user_dir):
	print "#show sites"
	site_file = open(user_dir + "/allowed_sites", "a+")
	print "## Current File Content ##"
	for line in site_file:
		print line

	error_string4 = ""
	while True:
		print "What do you want to do?"
		print "(1) Append To File"
		print "(0) Exit"
		print error_string4

		try:
			response4 = int(raw_input("Enter a number: "))
		except ValueError:
			error_string4 = "Oops!  That was no valid number.  Try again..."
			continue

		if response4 == 1:
			response5 = str(raw_input("Enter a site's URL: "))
			site_file.write(response5+ "\n")
		elif response4 == 0:
		    printTitle("Bye Bye")
		    sys.exit(0)
		else:
			error_string4 = "Oops!  That was no valid option.  Try again..."
			continue

# Set Up Function
def setup():
	printTitle("Set Up")
	device_MAC = choose_devices()
	print device_MAC
	user_dir = users_dir_name + "/" + device_MAC
	makedirs_p(user_dir)
	generate_show_key(user_dir)
	write_allowed_sites(user_dir)
	post_setup_menu()
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