#!/usr/bin/python3
"""Deploy web page to server"""
from fabric.api import put, run, env
from os import path


env.hosts = ["100.25.37.85", "100.26.228.112"]


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