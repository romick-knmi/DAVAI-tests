# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from .batodb import BatorODB
from .screening_LAM3D import Screening
from .minimCNT0_LAM3D import Minim as MinimCNT0
from .minimOOPS_LAM3D import Minim as MinimOOPS


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='arome', ticket=t, nodes=[
            Family(tag='3dvar', ticket=t, nodes=[
                LoopFamily(tag='rundates', ticket=t,
                    loopconf='rundates',
                    loopsuffix='.{}',
                    nodes=[
                    Family('BSM', ticket=t, on_error='delayed_fail', nodes=[
                        BatorODB(tag='batodb', ticket=t, **kw),
                        Screening(tag='screening', ticket=t, **kw),
                        MinimCNT0(tag='minimCNT0', ticket=t, on_error='delayed_fail', **kw),
                        MinimOOPS(tag='minimOOPS', ticket=t, **kw),
                        ], **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

