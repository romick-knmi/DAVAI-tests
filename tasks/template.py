# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

import footprints.util
from footprints import FPDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task, Driver
import davai
from davai_tbx.jobs import DavaiIALTaskPlugin, IncludesTaskPlugin


class EmptyTemplateTask(Task, DavaiIALTaskPlugin, IncludesTaskPlugin):

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
            pass
            #-------------------------------------------------------------------------------

        # E/ Flow Resources: produced by another task of the same job
        if 'fetch' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # F/ Compute step
        if 'compute' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # G/ Flow Resources: produced by this task and possibly used by a subsequent flow-dependant task
        if 'backup' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # H/ Davai expertise:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            pass
            #-------------------------------------------------------------------------------

        # I/ Other output resources of possible interest:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            pass
            #-------------------------------------------------------------------------------


class TemplateTask(Task, DavaiIALTaskPlugin, IncludesTaskPlugin):

    experts = [FPDict({'kind':'joTables'})] + davai.util.default_experts()
    lead_expert = experts[0]

    def output_block(self):
        return '.'.join([self.tag,
                         self.conf.model,
                         self.ND])

    def _obs_input_block(self):
        return '.'.join(['batorodb' + self._tag_suffix(),
                         self.conf.model,
                         self.ND])


    def process(self):
        self._tb_input = []
        self._tb_promise = []
        self._tb_exec = []
        self._tb_output = []

        # A/ Reference resources, to be compared to:
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_input(**self._reference_continuity_expertise())
            self._wrapped_input(**self._reference_continuity_listing())
            #-------------------------------------------------------------------------------

        # B.1/ Static Resources:
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._load_usual_tools()  # LFI tools, ecCodes defs, ...
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'RrtmConst',
                format         = 'unknown',
                genv           = self.conf.commonenv,
                kind           = 'rrtm',
                local          = 'rrtm.const.tgz',
            )
            #-------------------------------------------------------------------------------

        # B.2/ Static Resources (executables):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            tbio = self._wrapped_executable(
                role           = 'Binary',
                binmap         = 'gmap',
                format         = 'bullx',
                kind           = 'odbioassign',
                local          = 'ioassign',
                remote         = self.guess_pack_path_to_bin(),
                setcontent     = 'binaries',
            )
            #-------------------------------------------------------------------------------
            tbx = self._wrapped_executable(
                role           = 'Binary',
                binmap         = 'gmap',
                format         = 'bullx',
                kind           = 'mfmodel',
                local          = 'ARPEGE.EX',
                remote         = self.guess_pack_path_to_bin(),
                setcontent     = 'binaries',
            )
            #-------------------------------------------------------------------------------

        # C/ Initial Flow Resources: theoretically flow-resources, but statically stored in input_store
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_input(
                role           = 'Guess',
                block          = 'forecast',
                date           = '{0:s}/-PT6H'.format(self.conf.rundate.ymdh),
                experiment     = self.conf.input_store,
                format         = 'fa',
                kind           = 'historic',
                local          = 'ICMSHSCREINIT',
                term           = self.conf.guess_term,
            )
            #-------------------------------------------------------------------------------

        # D/ Promises
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_promise(**self._promised_listing())
            self._wrapped_promise(**self._promised_expertise())
            #-------------------------------------------------------------------------------

        # E/ Flow Resources: produced by another task of the same job
        if 'fetch' in self.steps:
            tbmap = self._wrapped_input(
                role           = 'Obsmap',
                block          = self._obs_input_block(),
                experiment     = self.conf.xpid,
                format         = 'ascii',
                kind           = 'obsmap',
                local          = 'bator_map',
                stage          = self.conf.mapstages,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Observations',
                block          = self._obs_input_block(),
                experiment     = self.conf.xpid,
                format         = 'odb',
                intent         = 'inout',
                helper         = tbmap[0].contents,
                kind           = 'observations',
                local          = 'ECMA.[part]',
                part           = tbmap[0].contents.dataset(),
                stage          = self.conf.mapstages,
            )
            #-------------------------------------------------------------------------------

        # F/ Compute step
        if 'compute' in self.steps:
            self.sh.title('Toolbox algo = tbalgo')
            tbalgo = toolbox.algo(
                crash_witness  = True,
                drhookprof     = self.conf.drhook_profiling,
                engine         = 'parallel',
                fcterm         = '6',
                ioassign       = tbio[0].container.localpath(),
                iomethod       = '4',
                kind           = 'screening',
                npool          = self.conf.obs_npools,
                slots          = self.conf.obs_tslots,
            )
            print(self.ticket.prompt, 'tbalgo =', tbalgo)
            print()
            self.component_runner(tbalgo, tbx)
            #-------------------------------------------------------------------------------
            self.sh.title('Toolbox algo = tbexpertise')
            tbexpertise = toolbox.algo(**self._algo_expertise())
            print(self.ticket.prompt, 'tbexpertise =', tbexpertise)
            print()
            self.component_runner(tbexpertise, [None])
            #-------------------------------------------------------------------------------

        # G/ Flow Resources: produced by this task and possibly used by a subsequent flow-dependant task
        if 'backup' in self.steps:
            self._wrapped_output(
                role           = 'Observations # CCMA',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                format         = 'odb',
                kind           = 'observations',
                layout         = 'ccma',
                local          = '[layout:upper]',
                part           = self.conf.obsout,
                stage          = 'screening',
            )
            #-------------------------------------------------------------------------------

        # H/ Davai expertise:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            self._wrapped_output(**self._output_expertise())
            self._wrapped_output(**self._output_comparison_expertise())
            #-------------------------------------------------------------------------------

        # I/ Other output resources of possible interest:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            self._wrapped_output(**self._output_listing())
            self._wrapped_output(**self._output_stdeo())
            self._wrapped_output(**self._drhook_profiles())
            #-------------------------------------------------------------------------------

