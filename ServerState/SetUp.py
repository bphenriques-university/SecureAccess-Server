#!/usr/bin/python2
import subprocess
import sys, os, errno
import base64
from Crypto.Cipher import AES
from CipherText import *
from ServerApplication import *

BEGIN_MAC = 0
END_MAC = 17
CURRENT_DIR = "./"
USER_DIR_NAME = "sirs_users"
ALLOWED_SITES_FILE = "/allowed_sites"
SYM_KEY_FILE = "/key"
PRIORITY_FILE = "/priority"

def printTitle(text):
	subprocess.call("clear", shell=True)
	max_string = 36
	adjust = 0
	if len(text) == 36:
		half_max_string = 0
		max_string += 4
	else:
		if len(text) % 2 == 1:
			adjust = 1
		half_max_string = ((max_string - len(text))/ 2) - 2
	half_max_adjust = half_max_string + adjust
	print "#" * (max_string + 2)
	print "#", " " * half_max_string, text, " " * half_max_adjust, "#"
	print "#" * (max_string + 2)

def makedirs_p(path):
    try:
        os.makedirs(path, 0700)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def menu_response(question, options, title=None):
	error_string = ""
	while True:
		if title != None:
			printTitle(title)
		print question
		counter = 1
		for option in options:
			option_string = "(" + str(counter) + ") " + option
			print option_string
			counter += 1
		print "(0) Exit"
		print error_string
		
		try:
			response = int(raw_input("Enter a number: "))
		except ValueError:
			error_string = "Oops!  That was no valid number.  Try again..."
			continue

		if response > 0 and response < len(options)+1:
		    return response
		elif response == 0:
		    printTitle("BYE BYE")
		    sys.exit(0)
		else:
			error_string = "Oops!  That was no valid option.  Try again..."
			continue

def choose_devices():
	printTitle("SCANNING, PLEASE WAIT...")
	scan_command = "hcitool scan | grep -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}' | sed 's/\t/ /g'"
	ps = subprocess.Popen(scan_command, shell=True, stdout=subprocess.PIPE)

	lines = []
	for line in iter(ps.stdout.readline, ''):
		# rstrip was adding a space at the begining so [1:] is taking it away
		lines.append(line.rstrip()[1:])

	response = menu_response("Choose your device:", lines, "Set Up")

	# em principio este if nao e' necessario ja que
	# a funcao acima verifica os limites
	if response > 0 and response <= len(lines):
		return lines[response-1][BEGIN_MAC:END_MAC]

def generate_KEK(user_dir):
	key = generate_key()
	qrcode_image = user_dir + "/qrcode.png"
	qr_gen_command = "qrencode -s 20 -o " + qrcode_image +" '"+base64.b64encode(key)+"'"
	ps = subprocess.Popen(qr_gen_command, shell=True)
	qr_gen_display = "eog " + qrcode_image + " > /dev/null 2>&1"
	ps = subprocess.Popen(qr_gen_display, shell=True, stdout=subprocess.PIPE)
	key_file = open(user_dir + SYM_KEY_FILE, "w+")
	key_file.write(key)
	key_file.close()
	return key

def show_key(key):
	question = "Your key (in base64) is: " + base64.b64encode(key) +". Continue?"
	options = [
		"Yes"
	]
	big_title =  "YOUR KEY"
	response = menu_response(question, options, title=big_title)

def prioridade_user(user_dir):
	question = "Choose priority:"
	options = [
		"Low",
		"Medium",
		"High"
	]
	big_title =  "PRIORITY"
	response = menu_response(question, options, title=big_title)
	priority = None
	priority = response
	# 3 = HIGH, 2 = MEDIUM, 1 = LOW

	priority_file = open(user_dir + PRIORITY_FILE, "w+")
	priority_file.write(str(priority))
	priority_file.close()

def create_allowed_sites_file(user_dir):
	open(user_dir + ALLOWED_SITES_FILE, 'a').close()

def show_allowed_sites_instructions(user_dir):
	allowed_sites_file = CURRENT_DIR + user_dir + ALLOWED_SITES_FILE
	printTitle("INSTRUCTIONS")
	print "# To set which sites you allow to be seen by this user:"
	print "# (1) go to the file", allowed_sites_file
	print "# (2) for each line insert the allowed website"
	print "# the website's URL must be written using this structure:"
	print "# \thttps://www.facebook.com"
	print "#"
	print "# If you wish to do this now select (0) Exit"

# Set Up Function
def setup():
	device_MAC = choose_devices()
	user_dir = USER_DIR_NAME + "/" + device_MAC
	makedirs_p(user_dir)
	#default_user = USER_DIR_NAME + "/default_user"
	#makedirs_p(default_user)

	#dar oportunidade de para o setup
	prioridade_user(user_dir)
	key = generate_KEK(user_dir)
	show_key(key)
	create_allowed_sites_file(user_dir)
	show_allowed_sites_instructions(user_dir)

	options = ["Run Server"]
	if menu_response("", options) == 1:
		execute()
	sys.exit(0)

# Execute Function #
def execute():
	printTitle("EXECUTING")
	bm = ServerApplication()
	bm.start()

# Main Function #
def main():
	question = "What do you want to do?"
	options = [
		"Set Up - New User",
		"Run Server"
	]
	big_title =  "SIRS PROJECT 2014 - GROUP 8 - MEIC-A"
	response = menu_response(question, options, title=big_title)
	
	if response == 1:
		setup()
	else:
	    execute()

if __name__ == "__main__":
	main()