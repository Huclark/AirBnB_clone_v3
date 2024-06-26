#!/usr/bin/python3
"""
Fabric script that generates a tgz archive from the contents of the web_static
folder of the AirBnB Clone repo
"""

from datetime import datetime
from fabric.api import local


def do_pack():
    """generates a tgz archive"""
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    local("mkdir -p versions")
    file_name = "versions/web_static_{}.tgz".format(date)
    local("tar -cvzf {} web_static".format(file_name))
    return file_name
