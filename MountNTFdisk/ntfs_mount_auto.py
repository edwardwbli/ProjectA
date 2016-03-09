#! /usr/bin/env python
# -*- coding: utf-8 -*-
 
import subprocess
import re
import os
 
ntfs_pattern = re.compile(r'.*NTFS.*')
device_dict = {}
 
def get_device_node():
    disk = subprocess.check_output(['diskutil', 'list'])
    disk_list = disk.split("\n")
        
    for info in disk_list: 
        print "%s" % info
        if ntfs_pattern.search(info):
            info_list = info.split()
            print "info_list: %s" % info_list
            disk_path = "/Volumes/%s" % info_list[2]
            device_node = "/dev/%s" % info_list[5]
            device_dict[disk_path] = device_node
        
def mount_ntfs():
    if not device_dict:
        print "No ntfs filesystem found..."
        return 12
    for disk_path in device_dict.keys():
        device_node = device_dict[disk_path]
        if os.path.isdir(disk_path):
            subprocess.check_output(['hdiutil', 'detach', disk_path])
 
        subprocess.check_output(['mkdir', disk_path])
        print "sudo mount_ntfs -o rw,nobrowse %s %s" % (device_node, disk_path)
        subprocess.check_output(['sudo',
                                 'mount_ntfs',
                                 '-o',
                                 'rw,nobrowse',
                                 device_node, disk_path])
        
#        subprocess.check_output(['sudo',
#                                 'ln',
#                                 '-s',
#                                 disk_path, disk_link])
 
if __name__ == '__main__':
    get_device_node()
    mount_ntfs()
  

