#!/usr/bin/python3
#distributes an archive to the web servers, using the function do_deploy:
import os.path
from fabric.api import env, put, run, local, task

env.hosts = ["100.25.37.85", "100.26.228.112"]


@task
def do_pack():
    """1-pack_web_static.py do_pack"""

    formatted_dt = datetime.now().strftime('%Y%m%d%H%M%S')
    mkdir = "mkdir -p versions"
    path = "versions/web_static_{}.tgz".format(formatted_dt)
    print("Packing web_static to {}".format(path))
    if local("{} && tar -cvzf {} web_static".format(mkdir, path)).succeeded:
        return path
    return None


@task
def do_deploy(archive_path):
     
     """Deploys an archive to a web server."""
     if os.path.isfile(archive_path) is False:
            return False
     file = archive_path.split("/")[-1]
     name = file.split(".")[0]

     if put(archive_path, "/tmp/{}".format(file)).failed is True:
             return False
     if run("rm -rf /data/web_static/releases/{}/".format(name)).failed is True:
             return False
     if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed is True:
             return False
     if run("tar -xzf /tmp/{} -c /data/web_static/releases/{}/".format(file, name)).failed is True:
             return False
     if run("rm /tmp/{}".format(file)).failed is True:
             return False
     if run("mv /data/web_static/releases/{}/web_static/* ""/data/web_static/releases/{}/".format(name, name)).failed is True:
             return False
     if run("rm -rf /data/web_static/releases/{}/web_static".format(name)).failed is True:
             return False
     if run("rm -rf /data/web_static/current").failed is True:
             return False
     if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name)).failed is True:
            return False
     return True
          
