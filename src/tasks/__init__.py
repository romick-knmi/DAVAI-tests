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
        t.env.EC_MEMINFO = '0'


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
