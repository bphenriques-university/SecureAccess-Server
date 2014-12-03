#!/usr/bin/python
import subprocess

def changeUsr(path_allowed_sites):

    '''
        Change the file used to view the allowed websites.
        It should be the one containing the allowed websites for the
        newUsr.
        teste should be used if no user is logged in.
    '''

    file = open('/etc/squid3/squid.conf.backup', 'r')
    file_w = open('/etc/squid3/squid.conf', 'w')
    lines = file.readlines()

    for line in lines:
        if(line.startswith('acl allowed_sites')):
            file_w.write('acl allowed_sites dstdom_regex -i "/home/tiago/Documents/GitRepos/SecureAccess-Server/ServerStateTIAGO/sirs_users/'+str(path_allowed_sites)+'/allowed_sites"\n')
        else:
            file_w.write(line)

    subprocess.call(['squid3', '-k', 'reconfigure'])
    subprocess.call(['killall', 'firefox'])
    #call(['firefox', '>', '/dev/null', '2>&1'])
    firefox = "firefox > /dev/null 2>&1"
    ps = subprocess.Popen(firefox, shell=True, stdout=subprocess.PIPE)
    file.close()
    file_w.close()

changeUsr("default_user")
