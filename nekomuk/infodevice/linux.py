# -*- coding: utf-8 -*-
import os
import re

class InfoDevice(object):
    by_path = {}
    by_uuid = {}
    by_label = {}
    def __init__(self):
        devices = {}
        pattern = r"^([^ ]+) on ([^ ]+).+"
        lines = os.popen('mount').readlines()
        for line in lines:
            data = re.findall(pattern, line)[0]
            devices[data[0]] = data[1]
        pattern = r"^([^:]+): (?:SEC_TYPE=\".+\" |)(LABEL=\"(.+)\" |)UUID=\"([^ ]+)\".+"
        lines = os.popen('blkid').readlines()
        for line in lines:
            data = re.findall(pattern, line)[0]
            if not data[0] in devices: continue
            mount_path = devices[data[0]]
            vars = {
                'dev': data[0],
                'path': mount_path,
                'label': data[2],
                'uuid': data[3],
            }
            self.by_path[mount_path] = vars
            self.by_label[data[2]] = vars
            self.by_uuid[data[3]] = vars
    def get_device_by_path(self, path):
        for device in sorted(self.by_path.keys(), key=len, reverse=True):
            if path.startswith(device):
                return self.by_path[device]
        return False
        
    def get_device_by_label(self, label):
        return self.by_label.get(label, False)
    
    def get_device_by_uuid(self, uuid):
        return self.by_uuid.get(uuid, False)
