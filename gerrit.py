#!/usr/bin/env python
#-*- coding: utf-8 -*-

import paramiko
import os
import pwd

class Gerrit():
    client = None

    def __init__(self, hostname, port=None, username=None):
        if username is None:
            username = pwd.getpwuid(os.getuid()).pw_name
        if port is None:
            port = 29418
        self.hostname = hostname
        self.port = port
        self.username = username
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.connect(hostname=hostname, port=port, username=username)
    
    def get_projects(self):
        stdin, stdout, stderr = self.client.exec_command('gerrit ls-projects')
        projects = stdout.read().decode('utf-8').split('\n')
        projects.pop()
        return projects
    
    @property
    def hook_url(self):
        return "https://%s/r/tools/hooks/commit-msg" % self.hostname