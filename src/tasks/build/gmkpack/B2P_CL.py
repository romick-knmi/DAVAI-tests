# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver

from .bundle2pack import Bundle2Pack
from .compile_link import PackCompileLink


def setup(t, **kw):
    return Driver(
        tag     = 'packbuild',
        ticket  = t,
        nodes   = [
            Bundle2Pack(tag='bundle2pack', ticket=t, **kw),
            PackCompileLink(tag='pack_compile_link', ticket=t, **kw)
        ],
        options=kw
    )

