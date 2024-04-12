# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

print("In BSM_4D_lam before import vortex")

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from .raw2odb.batodb import BatorODB
from .minims.AnalyseOOPS_LAM4D import AnalyseLAM4D
from .minims.minimOOPS_LAM4D import Minim as MinimOOPS

print("In BSM_4D_lam after import AnalyseLAM4D")

def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='arome', ticket=t, nodes=[
            Family(tag='4dvar3h', ticket=t, nodes=[
                Family(tag='default_compilation_flavour', ticket=t, nodes=[
                    LoopFamily(tag='rundates', ticket=t,
                        loopconf='rundates',
                        loopsuffix='.{}',
                        nodes=[
                        Family('BSM', ticket=t, on_error='delayed_fail', nodes=[
                            BatorODB(tag='batodb', ticket=t, **kw),
#                            AnalyseLAM4D(tag='AnalyseLAM4D', ticket=t, **kw),
#                            Screening(tag='screening', ticket=t, **kw),
#                             delayed_fail to let the minimOOPS run before raising error
#                            MinimCNT0(tag='minimCNT0', ticket=t, on_error='delayed_fail', **kw),
#                            MinimOOPS(tag='minimOOPS', ticket=t, **kw),
                            ], **kw),
                        ], **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )
