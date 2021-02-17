# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

from footprints import FPDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task
from common.util.hooks import update_namelist
import davai
from davai_tbx.jobs import DavaiIALTaskPlugin, IncludesTaskPlugin


def hook_temporary_OOPS_3D_fix(t, rh, obs_tslots):
    """
    Temporary hook for model namelist, until OOPS better handles time in 3D case
    (and to avoid to duplicate model namelists in for 3D/4D versions)
    """
    if int(obs_tslots[0]) == 1:
        # 3DVar case
        if 'NAMRIP' in rh.contents:
            print("Set ['NAMRIP']['CSTOP'] = 'h0'")
            rh.contents['NAMRIP']['CSTOP'] = 'h0'
    rh.save()


def hook_OOPS_2_CNT0(t, rh):
    """Hook to turn OOPS namelist into CNT0 namelist."""
    print("Set ['NAMARG']['CNMEXP'] = 'MINI'")
    rh.contents['NAMARG']['CNMEXP'] = 'MINI'
    print("Set ['NAMCT0']['L_OOPS'] = .FALSE.")
    rh.contents['NAMCT0']['L_OOPS'] = False
    rh.save()


class Minim(Task, DavaiIALTaskPlugin, IncludesTaskPlugin):

    experts = [FPDict({'kind':'joTables'})] + davai.util.default_experts()
    lead_expert = experts[0]

    def output_block(self):
        return '.'.join([self.conf.model,
                         self.ND,
                         self.tag])

    def obs_input_block(self):
        return '.'.join([self.conf.model,
                         self.ND,
                         'screening' + self._tag_suffix()])

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
                role           = 'Stabal',
                format         = 'unknown',
                genv           = self.conf.appenv,
                kind           = 'stabal',
                level          = '96',
                local          = 'stabal[level].[stat]',
                stat           = 'bal,cv',
            )
            #-------------------------------------------------------------------------------
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
            tbnam_objects = self._wrapped_input(
                role           = 'OOPSObjectsNamelists',
                binary         = 'arpifs',
                format         = 'ascii',
                genv           = self.conf.appenv,
                kind           = 'namelist',
                local          = 'naml_[object]',
                object         = ['observations_tlad','standard_geometry','bmatrix'],
                source         = 'OOPS/naml_[object]',
            )
            #-------------------------------------------------------------------------------
            tbnam_modelobjects = self._wrapped_input(
                role           = 'OOPSModelObjectsNamelists',
                binary         = 'arpifs',
                format         = 'ascii',
                genv           = self.conf.appenv,
                hook_OOPS3D    = (hook_temporary_OOPS_3D_fix,
                                  self.conf.obs_tslots),
                intent         = 'inout',
                kind           = 'namelist',
                local          = 'naml_[object]',
                object         = 'traj_model',
                source         = 'OOPS/naml_[object]',
            )
            #-------------------------------------------------------------------------------
            tbnam_leftovers = self._wrapped_input(
                role           = 'NamelistLeftovers',
                binary         = 'arpifs',
                format         = 'ascii',
                genv           = self.conf.appenv,
                hook_oops2cnt0 = (hook_OOPS_2_CNT0,),
                intent         = 'inout',
                kind           = 'namelist',
                local          = 'namelist_oops',
                source         = 'OOPS/namelist_oops_leftovers',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Namelist',
                binary         = 'arpege',
                format         = 'ascii',
                genv           = self.conf.appenv,
                hook_merge_nam = (update_namelist,
                                  tbnam_leftovers, tbnam_modelobjects, tbnam_objects),
                intent         = 'inout',
                kind           = 'namelist',
                local          = 'fort.4',
                source         = 'namelistmin1312_assim',
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
                kind           = 'mfmodel',
                local          = 'ARPEGE.EX',
                remote         = self.guess_pack(),
                setcontent     = 'binaries',
            )
            #-------------------------------------------------------------------------------

        # C/ Initial Flow Resources: theoretically flow-resources, but statically stored in input_store
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_input(
                role           = 'BackgroundStdError',
                block          = 'sigmab',
                date           = '{0:s}/-PT6H'.format(self.conf.rundate.ymdh),
                experiment     = self.conf.input_store,
                format         = 'grib',
                kind           = 'bgstderr',
                local          = 'errgrib.[variable]',
                stage          = 'vor',
                term           = '3',
                variable       = ['vo','ucdv','lnsp','t','q'],
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'SurfaceGuess',
                block          = 'forecast',
                date           = '{0:s}/-PT6H'.format(self.conf.rundate.ymdh),
                experiment     = self.conf.input_store,
                format         = 'fa',
                kind           = 'historic',
                local          = 'ICMSHSCREINIT.sfx',
                model          = 'surfex',
                term           = self.conf.guess_term,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Guess',
                block          = 'forecast',
                date           = '{0:s}/-PT6H'.format(self.conf.rundate.ymdh),
                experiment     = self.conf.input_store,
                format         = 'fa',
                kind           = 'historic',
                local          = 'ICMSHMINIINIT',
                term           = self.conf.guess_term,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'InitialCondition',
                block          = 'forecast',
                date           = '{0:s}/-PT6H'.format(self.conf.rundate.ymdh),
                experiment     = self.conf.input_store,
                format         = 'fa',
                kind           = 'historic',
                local          = 'ICMSHMINIIMIN',
                term           = self.conf.guess_term,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Background',
                block          = 'forecast',
                date           = '{0:s}/-PT6H'.format(self.conf.rundate.ymdh),
                experiment     = self.conf.input_store,
                format         = 'fa',
                kind           = 'historic',
                local          = 'ICMRFMINI0000',
                term           = self.conf.guess_term,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'VarBC',
                block          = '4dupd2',
                date           = '{0:s}/-PT6H'.format(self.conf.rundate.ymdh),
                experiment     = self.conf.input_store,
                format         = 'ascii',
                intent         = 'inout',
                kind           = 'varbc',
                local          = 'VARBC.cycle',
                stage          = 'traj',
            )
            #-------------------------------------------------------------------------------

        # D/ Promises
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_promise(**self._promised_listing())
            self._wrapped_promise(**self._promised_expertise())
            #-------------------------------------------------------------------------------

        # E/ Flow Resources: produced by another task of the same job
        if 'fetch' in self.steps:
            self._wrapped_input(
                role           = 'Observations',
                block          = self.obs_input_block(),
                experiment     = self.conf.xpid,
                format         = 'odb',
                intent         = 'inout',
                kind           = 'observations',
                layout         = 'ccma',
                local          = 'CCMA',
                part           = 'mix',
                stage          = 'screening',
            )
            #-------------------------------------------------------------------------------

        # F/ Compute step
        if 'compute' in self.steps:
            self.sh.title('Toolbox algo = tbalgo')
            tbalgo = toolbox.algo(
                crash_witness  = True,
                drhookprof     = self.conf.drhook_profiling,
                engine         = 'parallel',
                iomethod       = '4',
                kind           = 'minim',
                npool          = self.conf.obs_npools,
                slots          = self.conf.obs_tslots,
            )
            print(self.ticket.prompt, 'tbalgo =', tbalgo)
            print()
            self.component_runner(tbalgo, tbx)
            #-------------------------------------------------------------------------------
            self.run_expertise()
            #-------------------------------------------------------------------------------

        # G/ Flow Resources: produced by this task and possibly used by a subsequent flow-dependant task
        if 'backup' in self.steps:
            self._wrapped_output(
                role           = 'Observations',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                format         = 'odb',
                kind           = 'observations',
                layout         = 'ccma',
                local          = '[layout:upper]',
                part           = 'mix',
                stage          = 'minim',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_output(
                role           = 'Analysis',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                format         = 'fa',
                kind           = 'analysis',
                local          = 'MXMINI999+0000',
            )

        # H/ Davai expertise:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            self._wrapped_output(**self._output_expertise())
            self._wrapped_output(**self._output_comparison_expertise())
            #-------------------------------------------------------------------------------

        # I/ Other output resources of possible interest:
        if 'late-backup' in self.steps or 'backup' in self.steps:
            self._wrapped_output(**self._output_listing())
            self._wrapped_output(**self._output_stdeo())
            self._wrapped_output(**self._output_drhook_profiles())
            #-------------------------------------------------------------------------------

