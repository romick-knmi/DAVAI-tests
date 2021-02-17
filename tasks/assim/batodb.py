# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

from footprints import FPDict, FPSet

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task
from common.util.hooks import update_namelist

from davai_tbx.jobs import DavaiTaskPlugin


class BatorODB(Task, DavaiTaskPlugin):

    experts = [FPDict({'kind':'bator_obscount'}), FPDict({'kind':'bator_profile'})]
    lead_expert = experts[0]

    def output_block(self):
        return '.'.join([self.conf.model,
                         self.ND,
                         self.tag])

    def process(self):
        self._tb_input = []
        self._tb_promise = []
        self._tb_exec = []
        self._tb_output = []

        # A/ Reference resources, to be compared to:
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_input(**self._reference_continuity_expertise())

        # B.1/ Static Resources:
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_input(
                role           = 'AvgMasks',
                format         = 'ascii',
                genv           = self.conf.commonenv,
                kind           = 'avgmask',
                local          = 'mask.[sensor]',
                sensor         = 'atms,ssmis',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'BatodbConfigurationFile',
                format         = 'ascii',
                genv           = self.conf.commonenv,
                kind           = 'batodbconf',
                local          = 'param.cfg',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'CreateIoassignScript',
                format         = 'ascii',
                genv           = self.conf.commonenv,
                kind           = 'ioassign_script',
                language       = 'ksh',
                local          = '[purpose]_ioassign',
                purpose        = 'create',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'GPSList',
                format         = 'ascii',
                genv           = self.conf.appenv,
                kind           = 'gpslist',
                local          = 'list_gpssol',
            )
            #-------------------------------------------------------------------------------
            tbnamreduc = self._wrapped_input(
                role           = 'BatodbReductionDelta',
                binary         = 'batodb',
                format         = 'ascii',
                genv           = self.conf.appenv,
                kind           = 'namutil',
                local          = '[source]',
                source         = 'delta-bator_reduction.global.davai.nam',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'NamelistBatodb',
                binary         = 'batodb',
                format         = 'ascii',
                genv           = self.conf.appenv,
                hook_obs_reduc = (update_namelist, tbnamreduc),
                intent         = 'inout',
                kind           = 'namutil',
                local          = 'NAMELIST',
                source         = 'namel_bator_assim',
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
                remote         = self.guess_pack(),
                setcontent     = 'binaries',
            )
            #-------------------------------------------------------------------------------
            tbx = self._wrapped_executable(
                role           = 'Binary',
                binmap         = 'gmap',
                format         = 'bullx',
                kind           = 'batodb',
                local          = 'BATODB.EX',
                remote         = self.guess_pack(),
                setcontent     = 'binaries',
            )
            #-------------------------------------------------------------------------------

        # C/ Initial Flow Resources: theoretically flow-resources, but statically stored in input_store
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            obstype = self.conf.get('obstype', None)
            tbmap = self._wrapped_input(
                role           = 'Obsmap',
                block          = 'obsraw',
                experiment     = self.conf.input_store,
                format         = 'ascii',
                kind           = 'obsmap',
                local          = 'batodb_map',
                # if obstype is not specified (in conf or loop), get all obstypes from Bator Map:
                only           = FPSet([obstype]) if obstype else None,
                stage          = 'void',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Observations',
                block          = 'obsraw',
                experiment     = self.conf.input_store,
                fatal          = False,
                format         = '[helper:getfmt]',
                helper         = tbmap[0].contents,
                kind           = 'observations',
                local          = '[actualfmt].[part]',
                part           = tbmap[0].contents.dataset(),
                stage          = 'void',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'BlacklistGlobal',
                block          = 'obsraw',
                experiment     = self.conf.input_store,
                format         = 'ascii',
                kind           = 'blacklist',
                local          = 'LISTE_NOIRE_DIAP',
                scope          = 'global',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'BlacklistLocal',
                block          = 'obsraw',
                experiment     = self.conf.input_store,
                format         = 'ascii',
                kind           = 'blacklist',
                local          = 'LISTE_LOC',
                scope          = 'local',
            )
            #-------------------------------------------------------------------------------

        # D/ Promises
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_promise(**self._promised_expertise())
            #-------------------------------------------------------------------------------

        # E/ Flow Resources: produced by another task of the same job
        if 'fetch' in self.steps:
            pass

        # F/ Compute step
        if 'compute' in self.steps:
            self.sh.title('Toolbox algo = tbalgo')
            tbalgo = toolbox.algo(
                engine         = 'parallel',
                ioassign       = tbio[0].container.localpath(),
                iomethod       = '4',
                kind           = 'raw2odb',
                npool          = self.conf.obs_npools,
                ntasks         = self.conf.ntasks,
                parallel_const = self.conf.obs_paraconst,
                slots          = self.conf.obs_tslots,
                taskset        = 'socketpacked',
            )
            print(self.ticket.prompt, 'tbalgo =', tbalgo)
            print()
            self.component_runner(tbalgo, tbx)
            #-------------------------------------------------------------------------------
            self.run_expertise()
            #-------------------------------------------------------------------------------

        # G/ Flow Resources: produced by this task and possibly used by a subsequent flow-dependant task
        if 'backup' in self.steps:
            tbmapout = self._wrapped_output(
                role           = 'ObsmapUsed',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                format         = 'ascii',
                kind           = 'obsmap',
                local          = 'batodb_map.out',
                stage          = 'build',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_output(
                role           = 'ObservationsODB',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                format         = 'odb',
                kind           = 'observations',
                local          = 'ECMA.[part]',
                part           = tbmapout[0].contents.odbset(),
                stage          = 'build',
            )
            #-------------------------------------------------------------------------------

        # H/ Davai expertise:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            self._wrapped_output(**self._output_expertise())
            self._wrapped_output(**self._output_comparison_expertise())
            #-------------------------------------------------------------------------------

        # I/ Other output resources of possible interest:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            self._wrapped_output(
                role           = 'Listing',
                binary         = 'batodb',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                format         = 'ascii',
                kind           = 'listing',
                local          = 'listing.[part]',
                part           = tbmapout[0].contents.odbset(),
                task           = self._configtag,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_output(
                role           = 'ParallelExecSynthesis',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                format         = 'json',
                kind           = 'taskinfo',
                local          = 'parallel_exec_synthesis.[format]',
                nativefmt      = '[format]',
                scope          = 'parallelprofiling',
                task           = self._configtag,
            )
            #-------------------------------------------------------------------------------
