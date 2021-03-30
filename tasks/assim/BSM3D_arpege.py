# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from .batodb import BatorODB
from .screening import Screening
from .minimCNT0 import Minim as MinimCNT0
from .minimOOPS import Minim as MinimOOPS


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='arpege', ticket=t, nodes=[
            Family(tag='3dvar', ticket=t, nodes=[
                BatorODB(tag='batodb', ticket=t, **kw),
                Screening(tag='screening', ticket=t, **kw),
                MinimCNT0(tag='minimCNT0', on_error='delayed_fail', ticket=t, **kw),
                MinimOOPS(tag='minimOOPS', ticket=t, **kw),
                ], **kw),
            ], **kw),
        ],
    )
