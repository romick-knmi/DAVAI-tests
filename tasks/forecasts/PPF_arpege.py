# -*- coding: utf-8 -*-
"""
PPF = PGD-Prep-Forecast (to test the update of Surfex PGD and IC files before forecast
"""
from __future__ import print_function, absolute_import, unicode_literals, division

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from tasks.surfex.pgd import PGD
from tasks.surfex.prep import Prep
#from .arpege_forecast import ArpegeForecast as Forecast


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='arpege', ticket=t, nodes=[
            Family(tag='physio_arp', ticket=t, nodes=[
                PGD(tag='pgd', ticket=t, **kw),
                ], **kw),
            Prep(tag='prep', ticket=t, **kw),
                #Forecast(tag='pgd', ticket=t, **kw),
                #], **kw),
            ], **kw),
        ],
    )

