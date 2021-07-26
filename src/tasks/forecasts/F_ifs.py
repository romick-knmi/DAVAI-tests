# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

from footprints import FPDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task, Family, Driver
from common.util.hooks import update_namelist
import davai

from .models.ifs import IFS_Forecast


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='ifs', ticket=t, nodes=[
            IFS_Forecast(tag='forecast', ticket=t, **kw),
            ], **kw),
        ],
    )

