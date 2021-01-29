# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

import footprints.util

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task, Driver

import davai
from .gitref2pack import GitRef2Pack
from .compile_link import PackCompileLink


def setup(t, **kw):
    return Driver(
        tag     = 'packbuild',
        ticket  = t,
        nodes   = [
            GitRef2Pack(tag='gitref2pack', ticket=t, **kw),
            PackCompileLink(tag='pack_compile_link', ticket=t, **kw)
        ],
        options=kw
    )

