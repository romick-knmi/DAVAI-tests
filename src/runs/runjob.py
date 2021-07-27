#!/usr/bin/env python3
# -*- coding:Utf-8 -*-
"""
Wrapper to call mkjob.py with profile taken from config file.
"""
from __future__ import print_function, absolute_import, unicode_literals, division

import os
import argparse
import configparser
import subprocess


def main(task, name):
    vapp = os.path.basename(os.path.dirname(os.getcwd()))
    vconf = os.path.basename(os.getcwd())
    config = configparser.ConfigParser()
    config.read(os.path.join('conf', '{}_{}.ini'.format(vapp, vconf)))
    profile = config['DEFAULT']['mkjob_profile']
    subprocess.check_call(['python3', 'vortex/bin/mkjob.py',
                           '-j', 'profile=' + profile.strip(),
                           'task=' + task.strip(),
                           'name=' + name.strip()])


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Wrapper to call mkjob.py with profile taken from config file.")
    parser.add_argument('-t', '--task',
                        help="Task to be ran, e.g. 'forecasts.F_ifs'.",
                        required=True)
    parser.add_argument('-n', '--name',
                        help="Name of job (section in config file).",
                        required=True)
    args = parser.parse_args()
    main(**vars(args))
