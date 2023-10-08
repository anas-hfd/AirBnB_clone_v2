#!/usr/bin/python3
'''Fabric script to generate a .tgz archive from the web_static folder'''

from datetime import datetime
from fabric import local
import os.path


def do_pack():
    '''Creates a .tgz archive from the content of the web_static'''
    '''create the file and datetime'''
    date = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(date.year,
                                                         date.month,
                                                         date.day,
                                                         date.hour,
                                                         date.minute,
                                                         date.second)
    '''Return the .tgz archive'''
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file
