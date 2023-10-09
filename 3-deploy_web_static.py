#!/usr/bin/python3
"""creates and distributes an archive to the web servers"""

from datetime import datetime
from fabric.api import put, run, env, local
from os import path
import os.path


env.hosts = ["100.25.37.85", "100.26.228.112"]

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

def do_deploy(archive_path):
    """distributes an archive to web servers"""

    if not path.exists(archive_path):
        return False
    file_tar = archive_path.split("/")[-1]
    server_path = "/data/web_static/releases/{}".format(file_tar[:-4])
    run("mkdir -p {}".format(server_path))
    put(archive_path, "/tmp/")
    run("tar -xzf /tmp/{} -C {}".format(file_tar, server_path))
    run("rm /tmp/{}".format(file_tar))
    run("mv -f {}/web_static/* {}/".format(server_path, server_path))
    run('rm -rf {}/web_static'.format(server_path))
    run("rm -rf /data/web_static/current")
    run("ln -s {} /data/web_static/current".format(server_path))
    return True

def deploy():
    """Create and distribute archives to the web server"""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)