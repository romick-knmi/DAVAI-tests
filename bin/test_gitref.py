#/usr/bin/env python
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
                                      os.path.join(os.environ.get('HOME'), 'repositories', 'davai'))
PACKAGES = {'vortex': '/home/mf/dp/marp/verolive/vortex/vortex-olive-dev',
            'epygram': '/home/gmap/mrpe/mary/public/EPyGrAM/next',
            'davai_tbx': '/home/gmap/mrpe/mary/public/davai/dev/davai_tbx',
            'ia4h_scm': '/home/gmap/mrpe/mary/public/ia4h-scm/dev/ia4h_scm',
            }


def main(IAL_git_ref,
         usecase='NRV',
         IAL_repository=DAVAI_IAL_REPOSITORY,
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
    # create XP directory
    xpid = '{}@{}'.format(IAL_git_ref, os.environ['LOGNAME'])
    xp_path = os.path.join(DAVAI_XP_DIRECTORY, xpid)
    if os.path.exists(xp_path):
        if not preexisting_xp:
            raise FileExistsError('XP directory: {} exists while argument **preexisting_xp** is False'.format(xp_path))
        else:
            assert os.path.isdir(xp_path)
    else:
        os.makedirs(xp_path)
    os.chdir(xp_path)
    # tasks & conf: copy or link in dev mode
    if dev_mode:
        os.symlink(os.path.join(DAVAI_API, 'tasks'), 'tasks')
        os.symlink(os.path.join(DAVAI_API, 'conf'), 'conf')
    else:
        shutil.copytree(os.path.join(DAVAI_API, 'tasks'), 'tasks')
        shutil.copytree(os.path.join(DAVAI_API, 'conf'), 'conf')
    # conf: set <git_ref> and others in conf/davai_<vconf>.ini
    set_config = {'<IAL_git_ref>': IAL_git_ref,
                  '<IAL_repository>': IAL_repository,
                  '<usecase>': usecase}
    vconf = usecase.lower()
    config_template = 'davai_{}.tpl'.format(vconf)
    config_file = 'davai_{}.ini'.format(vconf)
    with io.open(os.path.join('conf', config_template), 'r') as f:
        config = f.readlines()
    for i, line in enumerate(config):
        if not line.startswith('#'):
            for k, v in set_config.items():
                if k in line:
                    config[i] = '='.join([line.split('=')[0], v + '\n'])
    with io.open(os.path.join('conf', config_file), 'w') as f:
        f.writelines(config)
    # runs
    for r in ('run.sh', 'run_ciboulai_setup.sh', 'run_packbuild.sh',
              'run_singletask.sh',
              'run_{}_tests.sh'.format(usecase)):
        shutil.copy(os.path.join(DAVAI_API, 'runs', r), r)
    # make links for the useful python packages
    for package, path in PACKAGES:
        os.symlink(path, package)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a Davai experiment based on a Git reference.')
    parser.add_argument('IAL_git_ref',
                        help="IFS-Arpege-LAM Git reference to be tested")
    parser.add_argument('-u', '--usecase',
                        default='NRV',
                        help="Usecase: NRV (restrained set of canonical tests) or ELP (extended elementary tests)")
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
         IAL_repository=args.IAL_repository,
         preexisting_xp=args.preexisting_xp,
         dev_mode=args.dev_mode)
