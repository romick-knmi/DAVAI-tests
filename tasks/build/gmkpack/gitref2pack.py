# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task, Driver, Family

from davai_tbx.jobs import DavaiTaskMixin


def setup(t, **kw):
    return Driver(tag='packbuild', ticket=t, options=kw, nodes=[
        Family(tag='packbuild', ticket=t, nodes=[
            GitRef2Pack(tag='gitref2pack', ticket=t, **kw)
            ], **kw),
        ],
    )


class GitRef2Pack(Task, DavaiTaskMixin):

    def output_block(self):
        return self.tag

    def process(self):
        self._wrapped_init()

        # 0./ Promises
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_promise(**self._promised_expertise())
            #-------------------------------------------------------------------------------

        # 1.1.0/ Reference resources, to be compared to:
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            pass
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

        # 2.3/ Flow Resources: produced by this task and possibly used by a subsequent flow-dependant task
        if 'backup' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # 3.0.1/ Davai expertise:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            self._wrapped_output(**self._output_expertise())
            #-------------------------------------------------------------------------------

        # 3.0.2/ Other output resources of possible interest:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            pass
            #-------------------------------------------------------------------------------

