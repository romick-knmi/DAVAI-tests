#!/usr/bin/env python3
# -*- coding:Utf-8 -*-
"""
Create a Davai experiment based on a **gitref**.
"""
from __future__ import print_function, absolute_import, unicode_literals, division

import os
import shutil
import io
import argparse
import re
import configparser

DAVAI_THIS_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAVAI_XP_DIRECTORY = os.environ.get('DAVAI_XP_DIRECTORY',
                                    os.path.join(os.environ.get('WORKDIR'), 'davai'))
DAVAI_IAL_REPOSITORY = os.environ.get('DAVAI_IAL_REPOSITORY',
                                      os.path.join(os.environ.get('HOME'), 'repositories', 'arpifs'))
DAVAI_HOSTNAME = os.environ.get('DAVAI_HOSTNAME', 'belenos')
DAVAI_PACKAGES_CONFIG = os.path.join(DAVAI_THIS_REPO, 'conf', 'packages.ini')
DAVAI_LOCAL_PACKAGES_CONFIG = os.path.join(os.environ['HOME'], '.davairc', 'packages.ini')


class Packages(object):
    """Handle the packages to be linked in experiment."""
    def __init__(self, default_hostname=DAVAI_HOSTNAME):
        self.default_hostname = default_hostname
        self.config = configparser.ConfigParser()
        print("(read {})".format(DAVAI_PACKAGES_CONFIG))
        self.config.read(DAVAI_PACKAGES_CONFIG)
        self.read_local_config()

    def read_local_config(self):
        loc = configparser.ConfigParser()
        if os.path.exists(DAVAI_LOCAL_PACKAGES_CONFIG):
            print("(read {})".format(DAVAI_LOCAL_PACKAGES_CONFIG))
            loc.read(DAVAI_LOCAL_PACKAGES_CONFIG)
        else:
            print("({} does not exist: ignore)".format(DAVAI_LOCAL_PACKAGES_CONFIG))
        for section in loc.sections():
            if not self.config.has_section(section):
                self.config.add_section(section)
            for k in loc[section]:
                self.config[section][k] = loc[section][k]

    def get(self, package, hostname=None):
        if hostname is None:
            hostname = self.default_hostname
        if not self.config.has_section(hostname):
            raise ValueError("hostname unknown in config packages.ini: " + hostname)
        return self.config[hostname][package]

    def list(self, hostname=None):
        if hostname is None:
            hostname = self.default_hostname
        if not self.config.has_section(hostname):
            raise ValueError("hostname unknown in config packages.ini: " + hostname)
        return [package for package in self.config[hostname]]


def main(IAL_git_ref,
         usecase='NRV',
         IAL_repository=DAVAI_IAL_REPOSITORY,
         comment=None,
         preexisting_xp=False,
         hostname=DAVAI_HOSTNAME,
         dev_mode=False):
    """
    Create a Davai experiment based on a Git reference.

    :param IAL_git_ref: IAL Git reference to be tested
    :param usecase: use case: NRV (restrained set of canonical tests) or ELP (extended elementary tests)
    :param IAL_repository: IAL Git repository local path
    :param preexisting_xp: if the xp directory supposedly preexists
    :param hostname: name of host machine, in order to find paths to necessary packages
    :param dev_mode: to link tasks sources rather than to copy them
    """
    ### initializations
    print("=> DAVAI xp creation starts...")
    xpid = '{}.{}@{}'.format(IAL_git_ref, usecase, os.environ['LOGNAME'])
    print("* xpid:", xpid)
    vconf = usecase.lower()
    print("* usecase:", usecase, "-- vconf:", vconf)
    ### create XP directory
    xp_path = os.path.join(DAVAI_XP_DIRECTORY, xpid, 'davai', vconf)
    print("* xpid path:", xp_path)
    if os.path.exists(xp_path):
        if not preexisting_xp:
            raise FileExistsError('XP directory: {} exists while argument **preexisting_xp** is False'.format(xp_path))
        else:
            assert os.path.isdir(xp_path)
    else:
        os.makedirs(xp_path)
    os.chdir(xp_path)
    ### tasks: copy or link in dev mode
    if dev_mode:
        os.symlink(os.path.join(DAVAI_THIS_REPO, 'tasks'), 'tasks')
    else:
        shutil.copytree(os.path.join(DAVAI_THIS_REPO, 'tasks'), 'tasks')
    ### conf: set <git_ref> and others in conf/davai_<vconf>.ini
    os.makedirs('conf')
    config_file = 'davai_{}.ini'.format(vconf)
    if dev_mode:
        os.symlink(os.path.join(DAVAI_THIS_REPO, 'conf', config_file),
                   os.path.join('conf', config_file))
    else:
        shutil.copy(os.path.join(DAVAI_THIS_REPO, 'conf', config_file),
                    os.path.join('conf', config_file))
    set_in_config = {'IAL_git_ref': IAL_git_ref,
                     'IAL_repository': IAL_repository,
                     'usecase': usecase,
                     'comment':comment if comment is not None else IAL_git_ref}
    config_set(config_file, set_in_config)
    ### runs: copy
    for r in ('run.sh', 'setup_ciboulai.sh', 'packbuild.sh',
              #'run_singletask.sh',
              'test_{}.sh'.format(usecase)):
        if dev_mode:
            os.symlink(os.path.join(DAVAI_THIS_REPO, 'runs', r), r)
        else:
            shutil.copy(os.path.join(DAVAI_THIS_REPO, 'runs', r), r)
    os.symlink('test_{}.sh'.format(usecase), 'tests.sh')
    ### python packages: make links
    packages = Packages(default_hostname=hostname)
    for package in packages.list():
        os.symlink(packages.get(package), package)
    print("... xp setup complete")
    print("---------------------")


def config_set(config_file, update_dict):
    """
    Replace **update_dict**'s *keys* by *values* in **config_file**.
    """
    # we do not use ConfigParser to keep the comments
    # read
    with io.open(os.path.join('conf', config_file), 'r') as f:
        config = f.readlines()
    # update
    for i, line in enumerate(config):
        if line[0] not in (' ', '#', '['):  # special lines
            for k, v in update_dict.items():
                pattern = '(?P<k>{}\s*=).*\n'.format(k)
                match = re.match(pattern, line)
                if match:
                    config[i] = match.group('k') + ' {}\n'.format(v)
    # write
    with io.open(os.path.join('conf', config_file), 'w') as f:
        f.writelines(config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a Davai experiment based on a Git reference.')
    parser.add_argument('IAL_git_ref',
                        help="IFS-Arpege-LAM Git reference to be tested")
    parser.add_argument('-u', '--usecase',
                        default='NRV',
                        help="Usecase: NRV (default, restrained set of canonical tests) or ELP (extended elementary tests)")
    parser.add_argument('-c', '--comment',
                        default=None,
                        help="Comment about experiment. Defaults to IAL_git_ref.")
    parser.add_argument('-r', '--IAL_repository',
                        default=DAVAI_IAL_REPOSITORY,
                        help="Path to IFS-Arpege-LAM Git repository. " +
                             " Default ({}) can be set through $DAVAI_IAL_REPOSITORY".format(DAVAI_IAL_REPOSITORY))
    parser.add_argument('-e', '--preexisting_xp',
                        default=False,
                        action='store_true',
                        help="Assume the experiment directory to already exist")
    parser.add_argument('--hostname',
                        default=DAVAI_HOSTNAME,
                        help="name of host machine, in order to find paths to necessary packages. " +
                             "Default ({}) can be set through $DAVAI_HOSTNAME".format(DAVAI_HOSTNAME))
    parser.add_argument('-d', '--dev_mode',
                        default=False,
                        action='store_true',
                        help="to link tasks sources rather than to copy them")
    args = parser.parse_args()

    main(args.IAL_git_ref,
         usecase=args.usecase,
         comment=args.comment,
         IAL_repository=args.IAL_repository,
         preexisting_xp=args.preexisting_xp,
         hostname=args.hostname,
         dev_mode=args.dev_mode)
