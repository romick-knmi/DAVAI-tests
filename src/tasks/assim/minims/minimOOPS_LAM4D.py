# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

from footprints import FPDict
from footprints.util import rangex

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task
from common.util.hooks import update_namelist
from common.util.hooks import arpifs_obs_error_correl_legacy2oops
import davai

from davai_taskutil.mixins import DavaiIALTaskMixin, IncludesTaskMixin
from davai_taskutil.hooks import hook_fix_model, hook_gnam, hook_disable_fullpos, hook_disable_flowdependentb



class Minim(Task, DavaiIALTaskMixin, IncludesTaskMixin):

    experts = [FPDict({'kind':'joTables'})] + davai.util.default_experts()

    def output_block(self):
        return '-'.join([self.conf.model,
                         self.NDVar,
                         self.tag])

    def obs_input_block(self):
        return '-'.join([self.conf.model,
                         self.NDVar,
                         'screening' + self._tag_suffix()])

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
            self._wrapped_input(
                role           = 'RCorrelations(MF)',
                format         = 'unknown',
                genv           = self.conf.commonenv,
                kind           = 'correlations',
                local          = 'rmtberr_[instrument].dat',
                intent         = 'inout',
                instrument     = 'iasi,cris',
                hook_convert   = (arpifs_obs_error_correl_legacy2oops,),
            )
            # FIXME: not anymore in Arpege cycle / commonenv
            #self._wrapped_input(
            #    role           = 'RCorrelations(MF)',
            #    format         = 'unknown',
            #    #genv           = self.conf.commonenv,
            #    genv           = self.conf.davaienv,
            #    kind           = 'correl',
            #    local          = '[scope]_correlation.dat',
            #    scope          = 'iasi,cris',
            #)
            #-------------------------------------------------------------------------------
            #self._wrapped_input(
            #    role           = 'RCorrelations(ECMWF & OOPS version - contains sigmaO)',
            #    format         = 'unknown',
            #    genv           = self.conf.commonenv,
            #    kind           = 'correl',
            #    local          = 'rmtb[scope].dat',
            #    scope          = 'err_iasi,err_cris',
            #)
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
                targetname     = 'ssmis,iasi',
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
                level          = '41',
                local          = 'stabal96.[stat]',
                stat           = 'bal,cv',
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
                objects        = 'minim-4DVar_aro',
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
                object         = ['observations_ala_tl','standard_geometry','bmatrix_aro',
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
                role           = 'OOPSFullposNamelists',
                binary         = 'arome',
                format         = 'ascii',
                genv           = self.conf.appenv,
                object         = ['26'],
                kind           = 'namelist',
                local          = 'fp_change_resol_[object].nam',
                source         = 'objects/fp_change_resol_[object].nam',
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
                object         = ['nonlinear_model_4dv_ala', 'linear_model_ala', 'traj_model_4dv_ala', 'standard_geometry_2x'],
                source         = 'objects/naml_[object]',
            )
            #-------------------------------------------------------------------------------
            tbnam_leftovers = self._wrapped_input(
                role           = 'NamelistLeftovers',
                binary         = 'arome',
                format         = 'ascii',
                genv           = self.conf.appenv,
                hook_cvaraux   = (hook_gnam, {'NAMVAR':{'LVARBC':False, 'LTOVSCV':False}}),
                intent         = 'inout',
                kind           = 'namelist',
                local          = 'fort.4',
                source         = 'objects/naml_leftovers_ala',
            )
            #-------------------------------------------------------------------------------

        # 1.1.3/ Static Resources (executables):
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            tbx = self.flow_executable(
                kind           = 'oopsbinary',
                run            = 'oovar',
                local          = 'OOVAR.X',
            )
            #-------------------------------------------------------------------------------

        # 1.2/ Flow Resources (initial): theoretically flow-resources, but statically stored in input_shelf
        if 'early-fetch' in self.steps or 'fetch' in self.steps:
            self._wrapped_input(
                role           = 'Guess',
#                block          = 'forecast',
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
                role           = 'BoundaryConditions',  
                block          = 'coupling',
                date           = self.conf.rundate,
                experiment     = self.conf.input_shelf,
                format         = '[nativefmt]',
                intent         = 'inout',
                kind           = 'boundary',
                local          = 'ELSCFOOPSALBC[term::fmt3h]',
                nativefmt      = 'fa',
                source_app     = 'ifs',
                source_conf    = 'determ',
                term           = rangex(0, self.conf.fcst_term,self.conf.coupling_frequency),
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
                role           = 'ClimAtmLR',
                format         = 'fa',
                genv           = self.conf.appenv_lam,
                kind           = 'clim_model',
                geometry       = 'nether20km',
                local          = 'Const.Clim_2x',
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

        # 2.2/ Compute step
        if 'compute' in self.steps:
            self._notify_start_compute()
            self.sh.title('Toolbox algo = tbalgo')
            tbalgo = toolbox.algo(
                crash_witness  = True,
                drhookprof     = self.conf.drhook_profiling,
                engine         = 'parallel',
                iomethod       = '4',
                kind           = 'oominim',
                npool          = self.conf.obs_npools,
                slots          = self.obs_tslots,
                mpiname        = self.conf.mpiname, 
                #withscreening  = True,         
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
                local          = 'ICMSHMXMI+0000',
                namespace      = self.REF_OUTPUT,
            )

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

