# -*- coding: utf-8 -*-
"""
PGD_geo = PGD on a range of LAM geometries
"""
from __future__ import print_function, absolute_import, unicode_literals, division

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from tasks.surfex.pgd import PGD


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='arome', ticket=t, nodes=[
            Family(tag='physio_aro', ticket=t, nodes=[
                LoopFamily(tag='geometries', ticket=t,
                    loopconf='geometrys',
                    loopsuffix='.{0.tag}',
                    nodes=[PGD(tag='pgd', ticket=t, **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

