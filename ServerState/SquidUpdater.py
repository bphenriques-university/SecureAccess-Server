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
            file_w.write('acl allowed_sites dstdom_regex -i "/home/tiago/Documents/GitRepos/SecureAccess-Server/ServerState/sirs_users/'+str(path_allowed_sites)+'/allowed_sites"\n')
        else:
            file_w.write(line)

    #subprocess.call(['squid3', '-k', 'reconfigure'])
    squid = "squid3 -k reconfigure > /dev/null 2>&1"
    ps = subprocess.Popen(squid, shell=True, stdout=subprocess.PIPE)
    #subprocess.call(['killall', 'firefox'])
    
    check_firefox = "ps -lA | grep firefox"
    ps = subprocess.Popen(check_firefox, shell=True, stdout=subprocess.PIPE)
    response = ps.communicate()
    #print response
    
    # se o firefox estiver aberto faz restart
    if response[0] != "":
        restart_squid = "service squid3 restart"
        ps = subprocess.Popen(restart_squid, shell=True, stdout=subprocess.PIPE)
        ps.communicate()
        print "SQUID RESTART"

    file.close()
    file_w.close()

#comentei isto porque quando se faz import deste ficheiro isto e' chamado pelos vistos e nao queremos isso
#changeUsr("default_user")
