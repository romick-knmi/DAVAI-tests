# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

import footprints.util
from footprints import FPDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task, Driver

import davai
from davai_tbx.jobs import DavaiTaskPlugin


def setup(t, **kw):
    return Driver(
        tag     = 'packbuild',
        ticket  = t,
        nodes   = [
            PackCompileLink(tag='pack_compile_link', ticket=t, **kw)
        ],
        options=kw
    )


class PackCompileLink(Task, DavaiTaskPlugin):

    experts = [FPDict({'kind':'gmkpack_build'}),]
    lead_expert = experts[0]
    
    def process(self):
        t = self.ticket
        sh = self.sh

        if 'early-fetch' in self.steps:
            self._promised_expertise()
            self._reference_continuity_expertise()

        if 'compute' in self.steps:
            sh.title('Toolbox algo tb01 = tbalgo')
            tb01 = tbalgo = toolbox.algo(
                cleanpack      = self.conf.cleanpack,
                crash_witness  = True,
                engine         = 'algo',
                kind           = 'pack_build_executables',
                packname       = davai.util.guess_packname(self.conf.IA4H_gitref,
                                                           self.conf.gmkpack_compiler_label,
                                                           self.conf.gmkpack_packtype,
                                                           compiler_flag=self.conf.gmkpack_compiler_flag),
                other_options  = FPDict({'GMK_THREADS':self.conf.threads, 'Ofrt':self.conf.Ofrt}),
                regenerate_ics = self.conf.regenerate_ics,
                fatal_build_failure = self.conf.fatal_build_failure,
            )
            print(t.prompt, 'tb01 =', tb01)
            print()
            tbalgo.run()
            #-------------------------------------------------------------------------------
            tbexpertise = self._expertise()
            tbexpertise.run()

        if 'late-backup' in self.steps:
            self._output_expertise()
            self._output_comparison_expertise()

