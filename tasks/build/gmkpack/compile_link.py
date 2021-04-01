# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

from footprints import FPDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task, Driver

from davai_jobs_mixins import DavaiTaskMixin


def setup(t, **kw):
    return Driver(
        tag     = 'packbuild',
        ticket  = t,
        nodes   = [
            PackCompileLink(tag='pack_compile_link', ticket=t, **kw)
        ],
        options=kw
    )


class PackCompileLink(Task, DavaiTaskMixin):

    experts = [FPDict({'kind':'gmkpack_build'}),]
    lead_expert = experts[0]

    def process(self):
        self._wrapped_init()
        self._notify_start()

        # 0./ Promises
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_promise(**self._promised_expertise())
            #-------------------------------------------------------------------------------

        # 1.1.0/ Reference resources, to be compared to:
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_input(**self._reference_continuity_expertise())
            #-------------------------------------------------------------------------------

        # 1.1.1/ Static Resources:
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # 1.1.2/ Static Resources (namelist(s) & config):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # 1.1.3/ Static Resources (executables):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # 1.2/ Initial Flow Resources: theoretically flow-resources, but statically stored in input_store
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # 2.1/ Flow Resources: produced by another task of the same job
        if 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # 2.2/ Compute step
        if 'compute' in self.steps:
            self.sh.title('Toolbox algo = tbalgo')
            tbalgo = toolbox.algo(
                cleanpack      = self.conf.cleanpack,
                crash_witness  = True,
                engine         = 'algo',
                homepack       = self.conf.get('homepack', None),
                kind           = 'pack_build_executables',
                packname       = self.guess_pack(abspath=False, to_bin=False),
                other_options  = FPDict({'GMK_THREADS':self.conf.threads, 'Ofrt':self.conf.Ofrt}),
                regenerate_ics = self.conf.regenerate_ics,
                fatal_build_failure = self.conf.fatal_build_failure,
            )
            print(self.ticket.prompt, 'tbalgo =', tbalgo)
            print()
            self.component_runner(tbalgo, [None])
            #-------------------------------------------------------------------------------
            self.run_expertise()
            #-------------------------------------------------------------------------------

        # 2.3/ Flow Resources: produced by this task and possibly used by a subsequent flow-dependant task
        if 'backup' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # 3.0.1/ Davai expertise:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            self._wrapped_output(**self._output_expertise())
            self._wrapped_output(**self._output_comparison_expertise())
            #-------------------------------------------------------------------------------

        # 3.0.2/ Other output resources of possible interest:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            pass
            #-------------------------------------------------------------------------------

