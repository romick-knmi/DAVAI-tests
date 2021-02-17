# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task, Driver, Family

from davai_tbx.jobs import DavaiTaskPlugin


def setup(t, **kw):
    return Driver(tag='packbuild', ticket=t, options=kw, nodes=[
        Family(tag='packbuild', ticket=t, nodes=[
            GitRef2Pack(tag='gitref2pack', ticket=t, **kw)
            ], **kw),
        ],
    )


class GitRef2Pack(Task, DavaiTaskPlugin):

    def output_block(self):
        return self.tag

    def process(self):
        self._tb_input = []
        self._tb_promise = []
        self._tb_exec = []
        self._tb_output = []

        # A/ Reference resources, to be compared to:
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # B.1/ Static Resources:
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # B.2/ Static Resources (executables):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # C/ Initial Flow Resources: theoretically flow-resources, but statically stored in input_store
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # D/ Promises
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_promise(**self._promised_expertise())
            #-------------------------------------------------------------------------------

        # E/ Flow Resources: produced by another task of the same job
        if 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # F/ Compute step
        if 'compute' in self.steps:
            self.sh.title('Toolbox algo = tbalgo')
            tbalgo = toolbox.algo(
                cleanpack      = self.conf.cleanpack,
                compiler_flag  = self.conf.gmkpack_compiler_flag,
                compiler_label = self.conf.gmkpack_compiler_label,
                crash_witness  = True,
                engine         = 'algo',
                git_ref        = self.conf.IAL_git_ref,
                homepack       = self.conf.get('homepack', None),
                kind           = 'ia4h_gitref2{}pack'.format(self.conf.gmkpack_packtype),
                link_filter_file = self.conf.link_filter_file,
                packname       = '__guess__',
                populate_filter_file = self.conf.populate_filter_file,
                preexisting_pack = self.conf.preexisting_pack,
                repository     = self.conf.IAL_repository,
                rootpack       = self.conf.get('rootpack', self.env.get('ROOTPACK', None))
            )
            print(self.ticket.prompt, 'tbalgo =', tbalgo)
            print()
            self.component_runner(tbalgo, [None])
            #-------------------------------------------------------------------------------
            self.run_expertise()
            #-------------------------------------------------------------------------------

        # G/ Flow Resources: produced by this task and possibly used by a subsequent flow-dependant task
        if 'backup' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # H/ Davai expertise:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            self._wrapped_output(**self._output_expertise())
            #-------------------------------------------------------------------------------

        # I/ Other output resources of possible interest:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            pass
            #-------------------------------------------------------------------------------

