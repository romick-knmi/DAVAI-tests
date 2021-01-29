# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

import footprints.util

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task, Driver

import davai
from davai_tbx.jobs import DavaiTaskPlugin


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
                git_ref        = self.conf.IA4H_gitref,
                kind           = 'ia4h_gitref2{}pack'.format(self.conf.gmkpack_packtype),
                packname       = '__guess__',
                preexisting_pack = self.conf.preexisting_pack,
                repository     = self.conf.IA4H_repository,
            )
            print(t.prompt, 'tb02 =', tb02)
            print()
            tbalgo.run()
            #-------------------------------------------------------------------------------
            tbexpertise = self._expertise()
            tbexpertise.run()

        if 'late-backup' in self.steps:
            self._output_expertise()

