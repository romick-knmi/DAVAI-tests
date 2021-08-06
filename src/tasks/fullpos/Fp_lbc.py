# -*- coding: utf-8 -*-
"""
Fi = Forecast (inline fullpos)
"""
from __future__ import print_function, absolute_import, unicode_literals, division

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from .lbc import LBCbyFullpos


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='arpege', ticket=t, nodes=[
            LBCbyFullpos(tag='fb_lbc.from-arpege', ticket=t, **kw),
            ], **kw),
        #Family(tag='ifs', ticket=t, nodes=[
        #    LBCbyFullpos(tag='fp_lbc.ifs', ticket=t, **kw),
        #    ], **kw),
        #Family(tag='arome', ticket=t, nodes=[
        #    LBCbyFullpos(tag='fp_lbc.arome', ticket=t, **kw),
        #    ], **kw),
        ],
    )

