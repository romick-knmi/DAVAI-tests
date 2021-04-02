#!/usr/bin/env python3
# -*- coding:Utf-8 -*-
"""
Guess host from (by order of resolution):
  - $DAVAI_HOST
  - resolution from socket.gethostname() through:
    * $HOME/.davairc/user_config.ini
    * {davai_api install}/conf/general.ini
"""
from __future__ import print_function, absolute_import, unicode_literals, division

import os
import re
import configparser
import socket

davai_home = os.path.join(os.environ['HOME'], '.davairc')
this_repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# config
general_config_file = os.path.join(this_repo, 'conf', 'general.ini')
general_config = configparser.ConfigParser()
general_config.read(general_config_file)
user_config_file = os.path.join(davai_home, 'user_config.ini')
user_config = configparser.ConfigParser()
if os.path.exists(user_config_file):
    user_config.read(user_config_file)


def guess_host():
    """
    Guess host from (by order of resolution):
      - $DAVAI_HOST
      - resolution from socket.gethostname() through:
        * $HOME/.davairc/user_config.ini
        * {davai_api install}/conf/general.ini
    """
    socket_hostname = socket.gethostname()
    host = os.environ.get('DAVAI_HOST', None)
    if not host:
        for config in (user_config, general_config):
            if 'hosts' in config.sections():
                for h, pattern in config['hosts'].items():
                    if re.match(pattern, socket_hostname):
                        host = h[:-len('_re_pattern')]  # h is '{host}_re_pattern'
                        break
                if host:
                    break
    if not host:
        raise ValueError("Couldn't find host in $DAVAI_HOST, " +
                         "nor guess from hostname ({}) and keys '{host}_re_pattern' " +
                         "in section 'hosts' of config files: ('{}', '{}')".format(
            socket_hostname, user_config_file, general_config_file))
    return host


if __name__ == '__main__':
    print(guess_host())

