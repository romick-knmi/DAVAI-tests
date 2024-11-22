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
from .standalone.alaro import StandaloneAlaroForecast


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        LoopFamily(tag='gmkpack', ticket=t,
            loopconf='compilation_flavours',
            loopsuffix='.{}',
            nodes=[
                Family(tag='ifs', ticket=t, on_error='delayed_fail', nodes=[
                    Family(tag='global21', ticket=t, nodes=[
                        StandaloneIFSForecast(tag='forecast-ifs-global21', ticket=t, **kw),
                        ], **kw),
                    ], **kw),
                Family(tag='arpege', ticket=t, on_error='delayed_fail', nodes=[
                    Family(tag='globaltst149c24', ticket=t, nodes=[
                        StandaloneArpegeForecast(tag='forecast-arpege-globaltst149c24', ticket=t,
                                                 on_error='delayed_fail', **kw),
                        StandaloneArpegeForecast(tag='forecast-arpege_nosfx-globaltst149c24', ticket=t, **kw),
                        ], **kw),
                    ], **kw),
                Family(tag='corsica2500', ticket=t, on_error='delayed_fail', nodes=[
                    Family(tag='arome', ticket=t, on_error='delayed_fail', nodes=[
                        StandaloneAromeForecast(tag='forecast-arome-corsica2500', ticket=t, **kw),
# romick-knmi : 2024-Nov : attempting to start a harmonie arome forecast - this currently will only try to load from 4dvarfr Arpege - might not work properly
                        StandaloneAromeForecast(tag='forecast-harmoniearome-corsica2500', ticket=t, **kw),
                        ], **kw),
                    ], **kw),
                Family(tag='alaro', ticket=t, on_error='delayed_fail', nodes=[
                    Family(tag='antwrp1300', ticket=t, on_error='delayed_fail', nodes=[
                        StandaloneAlaroForecast(tag='forecast-alaro0-antwrp1300', ticket=t, on_error='delayed_fail', **kw),
                        StandaloneAlaroForecast(tag='forecast-alaro1-antwrp1300', ticket=t, on_error='delayed_fail', **kw),
                        ], **kw),
                    Family(tag='chmh2325', ticket=t, nodes=[
                        StandaloneAlaroForecast(tag='forecast-alaro1_sfx-chmh2325', ticket=t, **kw),
                        ], **kw),
                    ], **kw),
                ], **kw),
        ],
    )

