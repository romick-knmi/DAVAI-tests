# -*- coding: utf-8 -*-
"""
Fi = Forecast (inline fullpos)
"""
from __future__ import print_function, absolute_import, unicode_literals, division

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from tasks.surfex.pgd import PGD
from tasks.surfex.prep import Prep
from .models.arpege_FP import ArpegeForecastFullPosInline as Forecast


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='arpege', ticket=t, nodes=[
            Forecast(tag='forecast', ticket=t, **kw),
            ], **kw),
        ],
    )

