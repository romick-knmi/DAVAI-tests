#!/usr/bin/env python
# -*- coding:Utf-8 -*-
"""
Create a Davai experiment based on a **gitref**.
"""
from __future__ import print_function, absolute_import, unicode_literals, division

import os
import shutil
import io
import argparse

DAVAI_API = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAVAI_XP_DIRECTORY = os.environ.get('DAVAI_XP_DIRECTORY',
                                    os.path.join(os.environ.get('WORKDIR'), 'davai'))
DAVAI_IAL_REPOSITORY = os.environ.get('DAVAI_IAL_REPOSITORY',
                                      os.path.join(os.environ.get('HOME'), 'repositories', 'arpifs'))
PACKAGES = {'vortex': '/home/mf/dp/marp/verolive/vortex/vortex-olive-dev',
            'epygram': '/home/gmap/mrpe/mary/public/EPyGrAM/next',
            #'davai_tbx': '/home/gmap/mrpe/mary/public/davai/dev/davai_tbx',
            'davai_tbx': '/home/gmap/mrpe/mary/repositories/davai_tbx/dev/davai_tbx',
            'ia4h_scm': '/home/gmap/mrpe/mary/public/ia4h-scm/dev/ia4h_scm',
            }


def main(IAL_git_ref,
         usecase='NRV',
         IAL_repository=DAVAI_IAL_REPOSITORY,
         comment=None,
         preexisting_xp=False,
         dev_mode=False):
    """
    Create a Davai experiment based on a Git reference.

    :param IAL_git_ref: IAL Git reference to be tested
    :param usecase: use case: NRV (restrained set of canonical tests) or ELP (extended elementary tests)
    :param IAL_repository: IAL Git repository local path
    :param preexisting_xp: if the xp directory supposedly preexists
    :param dev_mode: to link tasks sources rather than to copy them
    """
    ### initializations
    print("=> DAVAI xp creation starts...")
    xpid = '{}@{}'.format(IAL_git_ref, os.environ['LOGNAME'])
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
        os.symlink(os.path.join(DAVAI_API, 'tasks'), 'tasks')
    else:
        shutil.copytree(os.path.join(DAVAI_API, 'tasks'), 'tasks')
    ### conf: set <git_ref> and others in conf/davai_<vconf>.ini
    os.makedirs('conf')
    config_file = 'davai_{}.ini'.format(vconf)
    os.copyfile(os.path.join(DAVAI_API, 'conf', config_file),
                os.path.join('conf', config_file))
    set_in_config = {'IAL_git_ref': IAL_git_ref,
                     'IAL_repository': IAL_repository,
                     'usecase': usecase,
                     'comment':comment if comment is not None else IAL_git_ref}
    config_set(config_file, set_in_config)
    ### runs: copy
    for r in ('run.sh', 'run_ciboulai_setup.sh', 'run_packbuild.sh',
              'run_singletask.sh',
              'run_{}_tests.sh'.format(usecase)):
        shutil.copy(os.path.join(DAVAI_API, 'runs', r), r)
    os.symlink('run_{}_tests.sh'.format(usecase), 'run_tests.sh')
    ### python packages: make links
    for package, path in PACKAGES.items():
        os.symlink(path, package)
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
                        help="Usecase: NRV (restrained set of canonical tests) or ELP (extended elementary tests)")
    parser.add_argument('-c', '--comment',
                        default=None,
                        help="Comment about experiment. Defaults to IAL_git_ref.")
    parser.add_argument('-r', '--IAL_repository',
                        default=DAVAI_IAL_REPOSITORY,
                        help="Path to IFS-Arpege-LAM Git repository")
    parser.add_argument('-e', '--preexisting_xp',
                        default=False,
                        action='store_true',
                        help="Assume the experiment directory to already exist")
    parser.add_argument('-d', '--dev_mode',
                        default='NRV',
                        help="to link tasks sources rather than to copy them")
    args = parser.parse_args()

    main(args.IAL_git_ref,
         usecase=args.usecase,
         comment=args.comment,
         IAL_repository=args.IAL_repository,
         preexisting_xp=args.preexisting_xp,
         dev_mode=args.dev_mode)