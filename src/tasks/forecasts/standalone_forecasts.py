# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

from footprints import FPDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task, Family, Driver, LoopFamily
from common.util.hooks import update_namelist
import davai

from .standalone.ifs import StandaloneIFSForecast
from .standalone.arpege import StandaloneArpegeForecast
from .standalone.arome import StandaloneAromeForecast


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        LoopFamily(tag='gmkpack', ticket=t,
            loopconf='compilation_flavours',
            loopsuffix='.{}',
            nodes=[
                # Michael G 14/06/24: cy48t1_op1.16 was non-reproducable for the test
                # standalone-forecast-ifs-global21.impiifc2018.2ys, but this branch
                # is a dead end that should not be used for IFS, so this family of tests
                # can be disactivated.
                # Family(tag='ifs', ticket=t, on_error='delayed_fail', nodes=[
                #     Family(tag='global21', ticket=t, nodes=[
                #         StandaloneIFSForecast(tag='forecast-ifs-global21', ticket=t, **kw),
                #         ], **kw),
                #     ], **kw),
                Family(tag='arpege', ticket=t, on_error='delayed_fail', nodes=[
                    Family(tag='globaltst149c24', ticket=t, nodes=[
                        StandaloneArpegeForecast(tag='forecast-arpege-globaltst149c24', ticket=t, **kw),
                        ], **kw),
                    ], **kw),
                Family(tag='arome', ticket=t, on_error='delayed_fail', nodes=[
                    Family(tag='corsica2500', ticket=t, nodes=[
                        StandaloneAromeForecast(tag='forecast-arome-corsica2500', ticket=t, **kw),
                        ], **kw),
                    ], **kw),
            ], **kw),
        ],
    )

