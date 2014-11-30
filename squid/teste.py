#!/usr/bin/python
from subprocess import call

def changeUsr(newUsr):

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
            file_w.write('acl allowed_sites dstdom_regex -i "/etc/squid3/' + newUsr + '.acl"\n')
        else:
            file_w.write(line)

    call(['squid3', '-k', 'reconfigure'])

#changeUsr('teste')
changeUsr('allow')
