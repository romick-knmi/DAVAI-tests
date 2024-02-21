# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

from footprints import FPDict

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task
from common.util.hooks import update_namelist
import davai

from davai_taskutil.mixins import DavaiIALTaskMixin, IncludesTaskMixin
from davai_taskutil.hooks import hook_adjust_DFI, hook_gnam, hook_fix_model


class AnalyseLAM4D(Task, DavaiIALTaskMixin, IncludesTaskMixin):

    experts = [FPDict({'kind':'joTables'})] + davai.util.default_experts()

    def output_block(self):
        return '-'.join([self.conf.model,
                         self.NDVar,
                         self.tag])

    def obs_input_block(self):
        return '-'.join([self.conf.model,
                         self.NDVar,
                         'batodb' + self._tag_suffix()])

    def process(self):
        self._wrapped_init()
        self._obstype_rundate_association()
        self._notify_start_inputs()
        
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
            # FIXME: not anymore in Arpege cycle / commonenv
            self._wrapped_input(
                role           = 'GetIREmisAtlasInHDF',
                format         = 'ascii',
                #genv           = self.conf.commonenv,
                genv           = self.conf.davaienv,
                instrument     = '[targetname]',
                kind           = 'atlas_emissivity',
                local          = 'uw_ir_emis_atlas_hdf5.tar',
                targetname     = 'iasi',
            )
            #-------------------------------------------------------------------------------
            # FIXME: not anymore in Arpege cycle / commonenv
            self._wrapped_input(
                role           = 'RCorrelations(MF)',
                format         = 'unknown',
                #genv           = self.conf.commonenv,
                genv           = self.conf.davaienv,
                kind           = 'correl',
                local          = '[scope]_correlation.dat',
                scope          = 'iasi,cris',
            )
            #-------------------------------------------------------------------------------
            # FIXME: not anymore in Arpege cycle / commonenv
            self._wrapped_input(
                role           = 'AtlasEmissivity',
                format         = 'unknown',
                #genv           = self.conf.commonenv,
                genv           = self.conf.davaienv,
                instrument     = '[targetname]',
                kind           = 'atlas_emissivity',
                local          = 'ATLAS_[targetname:upper].BIN',
                month          = self.conf.rundate,
                targetname     = 'ssmis,iasi,seviri',
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
            #self._wrapped_input(
            #    role           = 'RsBiasTables',
            #    format         = 'odb',
            #    genv           = self.conf.commonenv,
            #    kind           = 'odbraw',
            #    layout         = 'RSTBIAS,COUNTRYRSTRHBIAS,SONDETYPERSTRHBIAS',
            #    local          = '[layout:upper]',
            #)
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
                level          = '41',
                local          = 'stabal96.[stat]',
                stat           = 'bal,cv',
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

        # 1.1.2/ Static Resources (namelist(s) & config):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_input(
                role           = 'Config',
                format         = 'json',
                genv           = self.conf.appenv,
                intent         = 'inout',
                kind           = 'config',
                local          = 'oops.[format]',
                nativefmt      = '[format]',
                objects        = 'analyse-4DVar_aro',
                scope          = 'oops',
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
                role           = 'OOPSObjectsNamelists',
                binary         = 'arome',
                format         = 'ascii',
                intent         = 'inout',
                genv           = self.conf.appenv,
                kind           = 'namelist',
                local          = 'naml_[object]',
                hook_write     = (hook_gnam, {'NAMOOPSWRITE':{'CDMEXP':'MXMINI'}}),
                object         = ['observations_aro','standard_geometry','bmatrix_aro',
                                  'write_analysis_aro'],
                source         = 'objects/naml_[object]',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'OOPSGomNamelists',
                binary         = 'arome',
                format         = 'ascii',
                genv           = self.conf.appenv,
                kind           = 'namelist',
                local          = 'namelist_[object]',
                object         = ['gom_setup', 'gom_setup_hres'],
                source         = 'objects/naml_[object]',
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'OOPSModelObjectsNamelists',
                binary         = 'arome',
                format         = 'ascii',
                genv           = self.conf.appenv,
                intent         = 'inout',
                kind           = 'namelist',
                local          = 'naml_[object]',
                hook_model     = (hook_fix_model,self.NDVar,self.conf.timestep,False),
#                hook_nstrin    = (hook_gnam, {'NAMRIP':{'FCSTOP':'NBPROC'}}),
#                hook_update    = (update_namelist),
                object         = ['nonlinear_model_4dv_aro', 'linear_model_aro', 'traj_model_4dv_aro'],
                source         = 'objects/naml_[object]',
            )
            #-------------------------------------------------------------------------------
            tbnam_leftovers = self._wrapped_input(
                role           = 'NamelistLeftovers',
                binary         = 'arome',
                format         = 'ascii',
                genv           = self.conf.appenv,
                intent         = 'inout',
                kind           = 'namelist',
                local          = 'fort.4',
                source         = 'objects/naml_leftovers_aro',
            )
            #-------------------------------------------------------------------------------

        # 1.1.3/ Static Resources (executables):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            tbio = self.flow_executable(
                kind           = 'odbioassign',
                local          = 'ioassign.x',
            )
            #-------------------------------------------------------------------------------
            tbx = self.flow_executable(
                kind           = 'oopsbinary',
                run            = 'oovar',
                local          = 'OOVAR.X',
            )
            #-------------------------------------------------------------------------------

        # 1.2/ Initial Flow Resources: theoretically flow-resources, but statically stored in input_shelf
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_input(
                role           = 'BackgroundStdError',
                block          = 'sigmab',
                date           = '{}/-{}'.format(self.conf.rundate, 'PT6H'),  # FIXME: should be sthg like: self.conf.cyclestep),
                experiment     = self.conf.input_shelf,
                format         = 'grib',
                geometry       = 'globalupd224',
                kind           = 'bgstderr',
                local          = 'errgrib.[variable]',
                model          = 'arpege',
                stage          = 'scr',
                term           = 'PT6H',  # FIXME: should be sthg like: self.conf.cyclestep,
                variable       = 'u,v,t,q,r,lnsp,gh,btmp,vo',
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Guess',
                block          = 'cplguess',
                date           = '{}/-{}'.format(self.conf.rundate, self.conf.cyclestep),
                experiment     = self.conf.input_shelf,
                format         = 'fa',
                kind           = 'historic',
                local          = 'ICMSHOOPSINIT',
                term           = self.guess_term(),
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'Surfex guess',
                block          = 'cplguess',
                date           = '{}/-{}'.format(self.conf.rundate, self.conf.cyclestep),
                experiment     = self.conf.input_shelf,
                format         = 'fa',
                kind           = 'historic',
                local          = 'ICMSHOOPSINIT.sfx',
                model          = 'surfex',
                term           = self.guess_term(),
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'BoundaryConditions',  # Initial
                block          = 'coupling',
                date           = self.conf.rundate,
                experiment     = self.conf.input_shelf,
                format         = '[nativefmt]',
                intent         = 'inout',
                kind           = 'boundary',
                local          = 'ELSCFOOPSALBC000',
#                local          = 'CPLIN+START',
                nativefmt      = 'fa',
                source_app     = 'ifs',
                source_conf    = 'determ',
                term           = 0,
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'BoundaryConditions',  # Initial
                block          = 'coupling',
                date           = self.conf.rundate,
                experiment     = self.conf.input_shelf,
                format         = '[nativefmt]',
                intent         = 'inout',
                kind           = 'boundary',
                local          = 'ELSCFOOPSALBC001',
#                local          = 'CPLIN+01',
                nativefmt      = 'fa',
                source_app     = 'ifs',
                source_conf    = 'determ',
                term           = 1,
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'BoundaryConditions',  # Initial
                block          = 'coupling',
                date           = self.conf.rundate,
                experiment     = self.conf.input_shelf,
                format         = '[nativefmt]',
                intent         = 'inout',
                kind           = 'boundary',
                local          = 'ELSCFOOPSALBC002',
 #               local          = 'CPLIN+02',
                nativefmt      = 'fa',
                source_app     = 'ifs',
                source_conf    = 'determ',
                term           = 2,
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'BoundaryConditions',  # Initial
                block          = 'coupling',
                date           = self.conf.rundate,
                experiment     = self.conf.input_shelf,
                format         = '[nativefmt]',
                intent         = 'inout',
                kind           = 'boundary',
                local          = 'ELSCFOOPSALBC003',
#                local          = 'CPLIN+03',
                nativefmt      = 'fa',
                source_app     = 'ifs',
                source_conf    = 'determ',
                term           = 3,
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'ClimAtmHR',
                format         = 'fa',
                genv           = self.conf.appenv_lam,
                kind           = 'clim_model',
                local          = 'Const.Clim',
                month          = self.conf.rundate.ymdh,
            )
            #-------------------------------------------------------------------------------
            self._wrapped_input(
                role           = 'ClimPGD',
                format         = 'fa',
                genv           = self.conf.appenv_lam,
                kind           = 'pgd',
                local          = 'Const.Clim.sfx',
            )
            #-------------------------------------------------------------------------------
            #self._wrapped_input(
            #    role           = 'BoundaryConditions',
            #    block          = 'coupling',
            #    date           = self.conf.rundate,
            #    experiment     = self.conf.input_shelf,
            #    format         = '[nativefmt]',
            #    intent         = 'inout',
            #    kind           = 'boundary',
            #    local          = 'CPLIN+[term::fmthm]',
            #    nativefmt      = 'fa',
            #    source_app     = 'ifs',
            #    source_conf    = 'determ',
            #    term           = rangex(self.conf.coupling_frequency, self.conf.fcst_term,
            #                            self.conf.coupling_frequency),
            #    vapp           = self.conf.shelves_vapp,
            #    vconf          = self.conf.shelves_vconf,
            #)
            #-------------------------------------------------------------------------------
            # FIXME: not consistent with oper arome (merge_varbc)
            self._wrapped_input(
                role           = 'VarBC',
                block          = 'minim',
                date           = '{}/-{}'.format(self.conf.rundate, self.conf.cyclestep),
                experiment     = self.conf.input_shelf,
                format         = 'ascii',
                intent         = 'inout',
                kind           = 'varbc',
                local          = 'VARBC.cycle',
                stage          = 'traj',
                vapp           = self.conf.shelves_vapp,
                vconf          = self.conf.shelves_vconf,
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
            self._notify_start_compute()
            self.sh.title('Toolbox algo = tbalgo')
            tbalgo = toolbox.algo(
                crash_witness  = True,
                drhookprof     = self.conf.drhook_profiling,
                engine         = 'parallel',
                iomethod       = '4',
                kind           = 'ooanalysis',
                npool          = self.conf.obs_npools,
                slots          = self.obs_tslots,
                mpiname        = self.conf.mpiname, 
                withscreening  = True,         
                #bindingmethod  = None,
                bindingmethod  = 'vortex',
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
                stage          = 'minim',
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
                role           = 'Analysis',
                block          = self.output_block(),
                experiment     = self.conf.xpid,
                format         = 'fa',
                kind           = 'analysis',
                local          = 'ICMSHMXMI+0000',
                namespace      = self.REF_OUTPUT,
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

