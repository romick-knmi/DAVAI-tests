#!/usr/bin/env python
# -*- coding:Utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

import vortex
from vortex.layout.jobs import JobAssistantPlugin


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
        t.env.DAVAI_SERVER = self.masterja.conf.DAVAI_SERVER
        t.env.EC_MEMINFO = '0'  # FIXME: without, some exec crash at EC_MEMINFO setup...

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
