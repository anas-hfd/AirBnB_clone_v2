#!/usr/bin/python3
#distributes an archive to the web servers, using the function do_deploy:
import os
from fabric.api import *

env.hosts = ["100.25.37.85", "100.26.228.112"]


def do_deploy(archive_path):
    #deploys the archive to the web servers
    if not os.path.exists(archive_path):
        return False

    # Upload the archive to /tmp/ on the remote servers
    put(archive_path, '/tmp/')

    # Extract the archive to /data/web_static/releases/
    archive_filename = os.path.basename(archive_path)
    archive_name_no_ext = os.path.splitext(archive_filename)[0]
    remote_path = f'/data/web_static/releases/{archive_name_no_ext}'
    run(f'mkdir -p {remote_path}')
    run(f'tar -xzf /tmp/{archive_filename} -C {remote_path}')
    run(f'rm /tmp/{archive_filename}')

    # Delete the old symbolic link
    run('rm -f /data/web_static/current')

    # Create a new symbolic link
    run(f'ln -s {remote_path} /data/web_static/current')

    return True