#!/usr/bin/env python
#-*- coding: utf-8 -*-

from gerrit import Gerrit
import simplejson
import os

__dir__ = os.path.dirname(__file__)

class Config():
    config_file = None
    config = {}
    overrides = {}
    exceptions = []
    _gerrit = None

    def __init__(self, config_file="config.json", exceptions=[], defaults={}):
        self.config_file = os.path.join(__dir__, config_file)
        self.exceptions = exceptions
        for key in defaults:
            self.config[key] = defaults[key]
        self.load()
        self.save()
    
    def load(self):
        if not os.path.exists(self.config_file):
            self.save()
        self.config.update(simplejson.load(open(self.config_file)))
    
    def save(self):
        config_tosave = {}
        for key in self.config:
            if key not in self.exceptions:
                config_tosave[key] = self.config[key]
        open(self.config_file, 'w').write(simplejson.dumps(config_tosave))
    
    @property
    def can_gerrit(self):
        return self.get('host') is not None
    
    @property
    def gerrit(self):
        if not self._gerrit:
            self._gerrit = Gerrit(hostname=self['host'], port=self.get('port'), username=self.get('user'))
        return self._gerrit


    def override(self, key, value):
        self.overrides[key] = value

    def __setitem__(self, key, value):
        self.config[key] = value
    set = __setitem__

    def __getitem__(self, key):
        if key in self.overrides:
            return self.overrides[key]
        return self.config[key]
    
    def get(self, key, default=None):
        if key in self.overrides:
            return self.overrides[key]
        return self.config.get(key, default)