# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

import footprints.util

import vortex
from vortex.layout.nodes import Task, Driver

from davai_taskutil.mixins import BuildMixin

def setup(t, **kw):
    return Driver(
        tag     = 'setup',
        ticket  = t,
        nodes   = [
            Wait4BuildInit(tag='wait4build_init', ticket=t, **kw),
        ],
        options=kw
    )


class Wait4BuildInit(Task, BuildMixin):

    def process(self):
        self.tasks2wait4_init()

