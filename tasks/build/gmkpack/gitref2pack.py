# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

import footprints.util

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task, Driver, Family

import davai
from davai_tbx.jobs import DavaiTaskPlugin


def setup(t, **kw):
    return Driver(
        tag     = 'packbuild',
        ticket  = t,
        nodes   = [
            Family(tag = 'packbuild',
               ticket  = t,
               nodes   = [
                   GitRef2Pack(tag='gitref2pack', ticket=t, **kw)
               ],
               **kw),
        ],
        options=kw
    )


class GitRef2Pack(Task, DavaiTaskPlugin):
    
    def process(self):
        t = self.ticket
        sh = self.sh

        if 'early-fetch' in self.steps:
            self._promised_expertise()

        if 'compute' in self.steps:
            sh.title('Toolbox algo tb02 = tbalgo')
            tb02 = tbalgo = toolbox.algo(
                cleanpack      = self.conf.cleanpack,
                compiler_flag  = self.conf.gmkpack_compiler_flag,
                compiler_label = self.conf.gmkpack_compiler_label,
                crash_witness  = True,
                engine         = 'algo',
                git_ref        = self.conf.IAL_git_ref,
                kind           = 'ia4h_gitref2{}pack'.format(self.conf.gmkpack_packtype),
                link_filter_file = self.conf.link_filter_file,
                packname       = '__guess__',
                populate_filter_file = self.conf.populate_filter_file,
                preexisting_pack = self.conf.preexisting_pack,
                repository     = self.conf.IAL_repository,
            )
            print(t.prompt, 'tb02 =', tb02)
            print()
            tbalgo.run()
            #-------------------------------------------------------------------------------
            tbexpertise = self._expertise()
            tbexpertise.run()

        if 'late-backup' in self.steps:
            self._output_expertise()

