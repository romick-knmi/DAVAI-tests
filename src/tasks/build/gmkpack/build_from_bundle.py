# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, LoopFamily

from .bundle2pack import Bundle2Pack
from .pack2bin import Pack2Bin

from davai_taskutil import gmkpack_executables_block_tag


def setup(t, **kw):
    return Driver(
        tag     = 'build',
        ticket  = t,
        nodes   = [
            LoopFamily(tag='gmkpack', ticket=t,
                loopconf='compilation_flavours',
                loopsuffix='.{}',
                nodes=[
                    Bundle2Pack(tag='bundle2pack', ticket=t, **kw),
                    Pack2Bin(tag=gmkpack_executables_block_tag, ticket=t, **kw)
                ], **kw),
        ],
        options=kw
    )

