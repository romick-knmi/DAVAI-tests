#!/usr/bin/env python
# -*- coding:Utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

import io

import vortex
from vortex.layout.jobs import JobAssistantPlugin
from bronx.fancies import loggers
logger = loggers.getLogger(__name__)


class DavaiJobAssistantPlugin(JobAssistantPlugin):
    """JobAssistant plugin for Davai."""
    _footprint = dict(
        info = 'Davai JobAssistant Plugin',
        attr = dict(
            kind = dict(
                values = ['davai', ]
            ),
        ),
    )

    def plugable_env_setup(self, t, **kw):  # @UnusedVariable
        t.env.DAVAI_SERVER = self.masterja.conf.davai_server
        t.env.EC_MEMINFO = '0'  # FIXME: without, some exec crash at EC_MEMINFO setup... -> fixed in CY49 !
        # set token from file if not in env
        ciboulai_token = None
        if 'CIBOULAI_TOKEN' not in t.env:
            if 'ciboulai_token_file' in self.masterja.conf:
                logger.info("Ciboulai token not in env; read in file, as set in config")
                try:
                    with io.open(self.masterja.conf.ciboulai_token_file, 'r') as tf:
                        ciboulai_token = tf.readline().strip()
                except FileNotFoundError:
                    pass
            if ciboulai_token is None:
                logger.warning("Ciboulai token not found in env var CIBOULAI_TOKEN " +
                               "nor in file provided in config's 'ciboulai_token_file' attribute. " +
                               "Ignored: token is not necessary for internal Ciboulai servers.")
            else:
                t.env.CIBOULAI_TOKEN = ciboulai_token

    def plugable_extra_session_setup(self, t, **kw):  # @UnusedVariable
        """genv cycles need to be "registered" using '*_cycle' config variables"""
        self.masterja.conf['davai_cycle'] = self.masterja.conf['davaienv']
        for appenv in [k for k in self.masterja.conf if k.startswith("appenv_")]:
            self.masterja.conf['{}_cycle'.format(appenv[7:])] = self.masterja.conf[appenv]
        self.plugable_toolbox_setup(t, **kw)  # FIXME: should not be called from here but automatically from
                                              # _toolbox_setup, but that doesn't work for some reason

    # FIXME: not called automatically from _toolbox_setup, for some reason ?
    def plugable_toolbox_setup(self, t, **kw):  # @UnusedVariable
        """Set 'vortex_set_aside' toolbox variable in order to export input resources to bucket"""
        if self.masterja.conf.shelves2bucket:
            vortex_set_aside = dict(defaults=dict(namespace='vortex.archive.fr',
                                                  storage='shelves.bucket.localhost'),
                                    includes=[self.masterja.conf.input_shelf_global,
                                              self.masterja.conf.input_shelf_lam])
            self.masterja.conf.vortex_set_aside = vortex_set_aside
            vortex.toolbox.defaults(vortex_set_aside=vortex_set_aside)

    def plugable_system_setup(self, t, **kw):
        if self.masterja.conf.promote_coredump:
            # Unlimited size for core-dump files
            t.sh.setulimit('core')
            # Intel wants this variable to be in lowercase... ifort is such a nice compiler :-(
            t.env.setvar('decfort_dump_flag', 'TRUE', enforce_uppercase=False)


class DavaiDevJobAssistantPlugin(DavaiJobAssistantPlugin):
    """JobAssistant plugin for Davai development."""
    _footprint = dict(
        info = 'Davai dev JobAssistant Plugin',
        attr = dict(
            kind = dict(
                values = ['davaidev', ]
            ),
        ),
    )

    def plugable_toolbox_setup(self, t, **kw):
        vortex.toolbox.active_promise = False  # deactivate the cleaning of promises in cache


class GitJobAssistantPlugin(JobAssistantPlugin):
    """JobAssistant plugin for Git."""
    _footprint = dict(
        info = 'Git JobAssistant Plugin',
        attr = dict(
            kind = dict(
                values = ['git', ]
            ),
        ),
    )

    def plugable_env_setup(self, t, **kw):  # @UnusedVariable
        target = t.sh.target()
        git_installdir = target.config.get('git', 'git_installdir')
        logger.info("Loading git from:", git_installdir)
        if git_installdir not in ('', None):
            t.env.setbinpath(t.sh.path.join(git_installdir, 'bin'), 0)
            t.env['GIT_EXEC_PATH'] = t.sh.path.join(git_installdir,
                                                    'libexec',
                                                    'git-core')
