# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

from footprints import FPDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task
import davai

from davai_jobs_mixins import DavaiIALTaskMixin, IncludesTaskMixin
from davai_tbx.hooks import hook_adjust_DFI


class Screening(Task, DavaiIALTaskMixin, IncludesTaskMixin):

    experts = [FPDict({'kind':'joTables'})] + davai.util.default_experts()
    lead_expert = experts[0]

    def output_block(self):
        return '.'.join([self.conf.model,
                         self.NDVar,
                         self.tag])

    def obs_input_block(self):
        return '.'.join([self.conf.model,
                         self.NDVar,
                         'batodb' + self._tag_suffix()])

    def process(self):
        self._wrapped_init()

        # 0./ Promises
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_promise(**self._promised_listing())
            self._wrapped_promise(**self._promised_expertise())
            #-------------------------------------------------------------------------------

        # 1.1.0/ Reference resources, to be compared to:
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_input(**self._reference_continuity_expertise())
            self._wrapped_input(**self._reference_continuity_listing())
            #-------------------------------------------------------------------------------

        # 1.1.1/ Static Resources:
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._load_usual_tools()  # LFI tools, ecCodes defs, ...
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'GetIREmisAtlasInHDF',
                format         = 'ascii',
                genv           = self.conf.commonenv,
                instrument     = '[targetname]',
                kind           = 'atlas_emissivity',
                local          = 'uw_ir_emis_atlas_hdf5.tar',
                targetname     = 'iasi',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'RCorrelations(MF)',
                format         = 'unknown',
                genv           = self.conf.commonenv,
                kind           = 'correl',
                local          = '[scope]_correlation.dat',
                scope          = 'iasi,cris',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'AtlasEmissivity',
                format         = 'unknown',
                genv           = self.conf.commonenv,
                instrument     = '[targetname]',
                kind           = 'atlas_emissivity',
                local          = 'ATLAS_[targetname:upper].BIN',
                month          = self.conf.rundate.ymdh,
                targetname     = 'ssmis,iasi,an1,an2',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'CoverParams',
                format         = 'foo',
                genv           = self.conf.commonenv,
                kind           = 'coverparams',
                local          = 'ecoclimap_covers_param.tgz',
                source         = 'ecoclimap',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'AmvError',
                format         = 'ascii',
                genv           = self.conf.commonenv,
                kind           = 'amv_error',
                local          = 'amv_p_and_tracking_error',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'AmvBias',
                format         = 'ascii',
                genv           = self.conf.commonenv,
                kind           = 'amv_bias',
                local          = 'amv_bias_info',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'RrtmConst',
                format         = 'unknown',
                genv           = self.conf.commonenv,
                kind           = 'rrtm',
                local          = 'rrtm.const.tgz',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'RsBiasTables',
                format         = 'odb',
                genv           = self.conf.commonenv,
                kind           = 'odbraw',
                layout         = 'RSTBIAS,COUNTRYRSTRHBIAS,SONDETYPERSTRHBIAS',
                local          = '[layout:upper]',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Coefmodel',
                format         = 'unknown',
                genv           = self.conf.commonenv,
                kind           = 'coefmodel',
                local          = 'COEF_MODEL.BIN',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'ScatCmod5',
                format         = 'unknown',
                genv           = self.conf.commonenv,
                kind           = 'cmod5',
                local          = 'fort.36',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'RtCoef',
                format         = 'unknown',
                genv           = self.conf.commonenv,
                kind           = 'rtcoef',
                local          = 'var.sat.misc_rtcoef.01.tgz',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'IoassignScripts',
                format         = 'ascii',
                genv           = self.conf.commonenv,
                kind           = 'ioassign_script',
                language       = 'ksh',
                local          = '[purpose]_ioassign',
                purpose        = 'create,merge',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'ClimPGD',
                format         = 'fa',
                genv           = self.conf.appenv,
                gvar           = 'pgd_fa_[geometry::tag]',
                kind           = 'pgdfa',
                local          = 'Const.Clim.sfx',
            )
            #-------------------------------------------------------------------------------

        # 1.1.2/ Static Resources (namelist(s) & config):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_input(
                role           = 'ChannelsNamelist',
                binary         = 'arpege',
                channel        = 'cris331,iasi314',
                format         = 'ascii',
                genv           = self.conf.appenv,
                kind           = 'namelist',
                local          = 'namchannels_[channel]',
                source         = 'namelist[channel]',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Namelistsurf',
                binary         = self.conf.model,
                format         = 'ascii',
                genv           = self.conf.appenv,
                intent         = 'inout',
                kind           = 'namelist',
                local          = 'EXSEG1.nam',
                source         = 'namel_previ_surfex',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Namelist',
                binary         = '[model]',
                format         = 'ascii',
                genv           = self.conf.appenv,
                hook_dfi       = (hook_adjust_DFI, self.NDVar),
                intent         = 'inout',
                kind           = 'namelist',
                local          = 'fort.4',
                source         = 'namelistscreen_assim',
            )
            #-------------------------------------------------------------------------------

        # 1.1.3/ Static Resources (executables):
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
                kind           = 'mfmodel',
                local          = 'ARPEGE.EX',
                remote         = self.guess_pack(),
                setcontent     = 'binaries',
            )
            #-------------------------------------------------------------------------------

        # 1.2/ Flow Resources (initial): theoretically flow-resources, but statically stored in input_store
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_input(
                role           = 'BackgroundStdError',
                block          = 'sigmab',
                date           = '{}/-{}'.format(self.conf.rundate.ymdh, self.conf.cyclestep),
                experiment     = self.conf.input_store,
                format         = 'grib',
                kind           = 'bgstderr',
                local          = 'errgrib.[variable]',
                stage          = 'scr',
                term           = self.conf.cyclestep,
                variable       = 'u,v,t,q,r,lnsp,gh,btmp,vo',
                vapp           = self.conf.stores_vapp,
                vconf          = self.conf.stores_vconf,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'SurfaceGuess',
                block          = 'forecast',
                date           = '{}/-{}'.format(self.conf.rundate.ymdh, self.conf.cyclestep),
                experiment     = self.conf.input_store,
                format         = 'fa',
                kind           = 'historic',
                local          = 'ICMSHSCREINIT.sfx',
                model          = 'surfex',
                term           = self.guess_term(),
                vapp           = self.conf.stores_vapp,
                vconf          = self.conf.stores_vconf,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Guess',
                block          = 'forecast',
                date           = '{}/-{}'.format(self.conf.rundate.ymdh, self.conf.cyclestep),
                experiment     = self.conf.input_store,
                format         = 'fa',
                kind           = 'historic',
                local          = 'ICMSHSCREINIT',
                term           = self.guess_term(),
                vapp           = self.conf.stores_vapp,
                vconf          = self.conf.stores_vconf,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'VarBC',
                block          = '4dupd2',
                date           = '{}/-{}'.format(self.conf.rundate.ymdh, self.conf.cyclestep),
                experiment     = self.conf.input_store,
                format         = 'ascii',
                intent         = 'inout',
                kind           = 'varbc',
                local          = 'VARBC.cycle',
                stage          = 'traj',
                vapp           = self.conf.stores_vapp,
                vconf          = self.conf.stores_vconf,
            )
            #-------------------------------------------------------------------------------

        # 2.1/ Flow Resources: produced by another task of the same job
        if 'fetch' in self.steps:
            tbmap = self._wrapped_input(
                role           = 'Obsmap',
                block          = self.obs_input_block(),
                experiment     = self.conf.xpid,
                format         = 'ascii',
                kind           = 'obsmap',
                local          = 'bator_map',
                stage          = 'build',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Observations',
                block          = self.obs_input_block(),
                experiment     = self.conf.xpid,
                format         = 'odb',
                intent         = 'inout',
                helper         = tbmap[0].contents,
                kind           = 'observations',
                local          = 'ECMA.[part]',
                part           = tbmap[0].contents.odbset(),
                stage          = 'build',
            )
            #-------------------------------------------------------------------------------

        # 2.2/ Compute step
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
                slots          = self.obs_tslots,
                timestep       = self.conf.timestep,
            )
            print(self.ticket.prompt, 'tbalgo =', tbalgo)
            print()
            self.component_runner(tbalgo, tbx)
            #-------------------------------------------------------------------------------
            self.run_expertise()
            #-------------------------------------------------------------------------------

        # 2.3/ Flow Resources: produced by this task and possibly used by a subsequent flow-dependant task
        if 'backup' in self.steps:
            self._wrapped_output(
                role           = 'Observations # CCMA',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                format         = 'odb',
                kind           = 'observations',
                layout         = 'ccma',
                local          = '[layout:upper]',
                part           = 'mix',
                stage          = 'screening',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_output(
                role           = 'Observations # ALL',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                format         = 'odb',
                kind           = 'observations',
                local          = 'ECMA.{glob:ext:\w+}',
                part           = '[glob:ext]',
                stage          = 'screening',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_output(
                role           = 'VarBC # OUT',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                format         = 'ascii',
                kind           = 'varbc',
                local          = 'VARBC.cycle',
                stage          = 'screening',
            )
            #-------------------------------------------------------------------------------

        # 3.0.1/ Davai expertise:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            self._wrapped_output(**self._output_expertise())
            self._wrapped_output(**self._output_comparison_expertise())
            #-------------------------------------------------------------------------------

        # 3.0.2/ Other output resources of possible interest:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            self._wrapped_output(**self._output_listing())
            self._wrapped_output(**self._output_stdeo())
            self._wrapped_output(**self._output_drhook_profiles())
            #-------------------------------------------------------------------------------

