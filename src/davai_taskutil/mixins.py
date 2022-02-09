#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Mixins for Tasks, containing useful functionalities.
"""

from __future__ import print_function, absolute_import, unicode_literals, division

from vortex import toolbox
from bronx.stdtypes.date import Period, utcnow
from davai.algo.mixins import context_info_for_task_summary  # a function in vortex


class IncludesTaskMixin(object):
    """Provide a method to input usual tools, known as 'Task Includes' in Olive."""

    def guess_pack(self, abspath=True, to_bin=True):
        """Guess and return pack according to self.conf.pack"""
        path_split = self.conf.pack.split(self.sh.path.sep)
        if abspath:
            guess = path_split
        else:
            guess = path_split[-1:]
        if to_bin:
            guess += 'bin'
        return self.sh.path.join(guess)

    def _load_usual_tools(self):
        if 'early-fetch' in self.steps:
            self.sh.title('Toolbox usual-tools tb_ut01')
            tb_ut01 = toolbox.input(
                role           = 'LFIScripts',
                format         = 'unknown',
                genv           = self.conf.commonenv,
                kind           = 'lfiscripts',
                local          = 'usualtools/tools.lfi.tgz',
            )
            print(self.ticket.prompt, 'tb_ut01 =', tb_ut01)
            print()
            #-------------------------------------------------------------------------------
            self.sh.title('Toolbox usual-tools tb_ut02')
            tb_ut02 = toolbox.input(
                role           = 'IOPoll',
                format         = 'unknown',
                genv           = self.conf.commonenv,
                kind           = 'iopoll',
                language       = 'perl',
                local          = 'usualtools/io_poll',
            )
            print(self.ticket.prompt, 'tb_ut02 =', tb_ut02)
            print()
            #-------------------------------------------------------------------------------
            self.sh.title('Toolbox usual-tools tb_ut03')
            tb_ut03 = toolbox.executable(
                role           = 'LFITOOLS',
                binmap         = 'gmap',
                format         = 'bullx',
                kind           = 'lfitools',
                local          = 'usualtools/lfitools',
                remote         = self.guess_pack(),
                setcontent     = 'binaries',
            )
            print(self.ticket.prompt, 'tb_ut03 =', tb_ut03)
            print()
            #-------------------------------------------------------------------------------
            self.sh.title('Toolbox usual-tools tb_ut04')
            tb_ut04 = toolbox.input(
                role           = 'AdditionalGribAPIDefinitions',
                format         = 'unknown',
                genv           = self.conf.commonenv,
                kind           = 'gribapiconf',
                local          = 'extra_grib_defs/gribdef.tgz',
                target         = 'definitions',
            )
            print(self.ticket.prompt, 'tb_ut04 =', tb_ut04)
            print()
        return tb_ut01, tb_ut02, tb_ut03, tb_ut04


class WrappedToolboxMixin(object):
    """
    Provide useful methods for IOs.

    Requires process() method to call _wrapped_init() to set additional attributes
    """

    REF_OUTPUT = '__archive_if_ref__'
    DEFAULT_OUTPUT_NAMESPACE = 'vortex.cache.fr'

    def output_namespace(self, namespace):
        if namespace == self.REF_OUTPUT and self.conf.archive_as_ref:
            return 'vortex.multi.fr'
        elif namespace in ('vortex.multi.fr', 'vortex.cache.fr', 'vortex.archive.fr'):
            return namespace
        else:
            return self.DEFAULT_OUTPUT_NAMESPACE

    def _wrapped_init(self):
        self._tb_input = []
        self._tb_promise = []
        self._tb_exec = []
        self._tb_output = []

    def _wrapped_input(self, **description):
        input_number = len(self._tb_input) + 1
        self.sh.title('Toolbox input {:02}'.format(input_number))
        r = toolbox.input(**description)
        self._tb_input.append(r)
        print(self.ticket.prompt, 'tb input {:02} ='.format(input_number), r)
        print()
        return r

    def _wrapped_promise(self, **description):
        promise_number = len(self._tb_promise) + 1
        self.sh.title('Toolbox promise {:02}'.format(promise_number))
        description['namespace'] = self.output_namespace(description.get('namespace'))
        r = toolbox.promise(**description)
        self._tb_promise.append(r)
        print(self.ticket.prompt, 'tb promise {:02} ='.format(promise_number), r)
        print()
        return r

    def _wrapped_executable(self, **description):
        exec_number = len(self._tb_exec) + 1
        self.sh.title('Toolbox executable {:02}'.format(exec_number))
        r = toolbox.executable(**description)
        self._tb_exec.append(r)
        print(self.ticket.prompt, 'tb exec {:02} ='.format(exec_number), r)
        print()
        return r

    def _wrapped_output(self, **description):
        output_number = len(self._tb_output) + 1
        self.sh.title('Toolbox output {:02}'.format(output_number))
        description['namespace'] = self.output_namespace(description.get('namespace'))
        r = toolbox.output(**description)
        self._tb_output.append(r)
        print(self.ticket.prompt, 'tb output {:02} ='.format(output_number), r)
        print()
        return r


class DavaiTaskMixin(WrappedToolboxMixin):
    """Provide useful methods for Davai IOs."""
    experts = []
    _taskinfo_kind = 'taskinfo'  # Flow taskinfo, can be forced to 'statictaskinfo' for non-flow tasks (e.g. pgd, build...)

    @property
    def lead_expert(self):
        """Default, can still be overwritten in class definition."""
        if len(self.experts) > 0:
            return self.experts[0]
        else:
            return None

    @property
    def obs_tslots(self):
        return '/'.join([str(self.conf.timeslots),
                         self.conf.window_start,
                         self.conf.window_length])

    @property
    def NDVar(self):
        return '4DVar' if int(self.conf.timeslots) > 1 else '3DVar'

    def guess_term(self, force_window_start=False):
        term = Period(self.conf.cyclestep)
        if self.NDVar == '4DVar' or force_window_start:
            # withdraw to window start
            term = term + Period(self.conf.window_start)
        return term.isoformat()

    def _split_rundate_obstype_couple(self):
        if 'rundate_obstype' in self.conf:
            self.conf.rundate, self.conf.obstype = self.conf.rundate_obstype.split('.')
            toolbox.defaults(date=self.conf.rundate)

    def _obstype_rundate_association(self):
        """Set rundate as associated with obstype in config."""
        if 'obstype' in self.conf and 'obstype_rundate_map' in self.conf:
            obstype = self.conf.obstype
            assert obstype in self.conf.obstype_rundate_map, \
                "config file not configurated to loop on obstype '{}' : no rundate associated".format(obstype)
            self.conf.rundate = self.conf.obstype_rundate_map[obstype]
            toolbox.defaults(date=self.conf.rundate)

    def guess_pack(self, abspath=True, homepack=None, to_bin=True):
        """Guess and return pack according to self.conf"""
        from ial_build.pygmkpack import GmkpackTool
        return GmkpackTool.guess_pack_name(self.conf.IAL_git_ref,
                                           self.conf.gmkpack_compiler_label,
                                           self.conf.gmkpack_compiler_flag,
                                           self.conf.gmkpack_packtype,
                                           abspath=abspath,
                                           homepack=homepack,
                                           to_bin=to_bin)

    def bundle_guess_pack(self, abspath=True, homepack=None, to_bin=True):
        """Guess and return pack according to self.conf"""
        from ial_build.bundle import IALBundle
        b = IALBundle(bundle_file)
        return b.gmkpack_guess_pack_name(self.conf.gmkpack_packtype,
                                         self.conf.gmkpack_compiler_label,
                                         self.conf.gmkpack_compiler_flag,
                                         abspath=abspath,
                                         homepack=homepack,
                                         to_bin=to_bin)

    def run_expertise(self):
        if 'compute' in self.steps:
            self.sh.title('Toolbox algo = tbexpertise')
            tbexpertise = toolbox.algo(**self._algo_expertise())
            print(self.ticket.prompt, 'tbexpertise =', tbexpertise)
            print()
            self.component_runner(tbexpertise, [None])

    @property
    def taskid(self):
        return self.output_block()

    def output_block(self):
        """
        Output block method: should map more or less Family tree.
        TO BE OVERWRITTEN in real tasks
        """
        return '-'.join([self.tag])

    def _tag_suffix(self):
        """Get the suffix part of the tag, in case of a LoopFamily-ed task."""
        return self.tag[len(self._configtag):]

    def _reference_continuity_listing(self):
        return dict(
            role           = 'Reference',
            binary         = '[model]',
            block          = self.output_block(),
            experiment     = self.conf.ref_xpid,
            fatal          = False,
            format         = 'ascii',
            kind           = 'plisting',
            local          = 'ref_listing.[format]',
            namespace      = self.conf.ref_namespace,
            seta           = '1',
            setb           = '1',
            task           = self._configtag,
            vconf          = self.conf.ref_vconf)

    def _promised_expertise(self):
        return dict(
            role           = 'TaskSummary',
            block          = self.output_block(),
            experiment     = self.conf.xpid,
            format         = 'json',
            hook_train     = ('davai.hooks.take_the_DAVAI_train',
                              self.conf.expertise_fatal_exceptions,
                              self.conf.hook_davai_wagons),
            kind           = self._taskinfo_kind,
            local          = 'task_summary.[format]',
            namespace      = self.REF_OUTPUT,
            nativefmt      = '[format]',
            scope          = 'itself',
            task           = 'expertise')

    def _reference_continuity_expertise(self):
        return dict(
            role           = 'Reference',
            namespace      = self.conf.ref_namespace,
            experiment     = self.conf.ref_xpid,
            block          = self.output_block(),
            fatal          = False,
            format         = 'json',
            kind           = self._taskinfo_kind,
            local          = 'ref_summary.[format]',
            nativefmt      = '[format]',
            scope          = 'itself',
            task           = 'expertise',
            vconf          = self.conf.ref_vconf)

    def _reference_consistency_expertise(self):
        return dict(
            role           = 'Reference',
            experiment     = self.conf.xpid,
            block          = self.conf.consistency_ref_block,
            fatal          = False,
            format         = 'json',
            kind           = self._taskinfo_kind,
            local          = 'ref_summary.[format]',
            nativefmt      = '[format]',
            scope          = 'itself',
            task           = 'expertise')

    def _algo_expertise(self):
        return dict(
            block          = self.output_block(),
            engine         = 'algo',
            experiment     = self.conf.xpid,
            experts        = self.experts,
            lead_expert    = self.lead_expert,
            fatal_exceptions = self.conf.expertise_fatal_exceptions,
            ignore_reference = self.conf.ignore_reference,
            kind           = 'expertise')

    def _notify_start_step(self, step):
        """Notify Ciboulai that a step has started."""
        from ial_expertise.task import TaskSummary, task_status
        task_summary = TaskSummary()
        if step == 'inputs':
            task_summary['Status'] = task_status['I...']
        elif step == 'compute':
            task_summary['Status'] = task_status['C...']
        notification_file = '.{}_started.json'.format(step)
        task_summary['Context'] = context_info_for_task_summary(self.ticket.context)
        task_summary['Updated'] = utcnow().isoformat().split('.')[0]
        task_summary.dump(notification_file)
        description = self._output_expertise()
        description['task'] = step
        description['local'] = notification_file
        description['namespace'] = 'vortex.cache.fr'
        toolbox.output(**description)
        self.ticket.sh.remove(notification_file)

    def _notify_start_inputs(self):
        if 'early-fetch' in self.steps:
            self._notify_start_step('inputs')

    def _notify_start_compute(self):
        if 'compute' in self.steps:
            self._notify_start_step('compute')

    def _output_expertise(self):
        return dict(
            role           = 'TaskSummary',
            kind           = self._taskinfo_kind,
            block          = self.output_block(),
            experiment     = self.conf.xpid,
            hook_train     = ('davai.hooks.take_the_DAVAI_train',
                              self.conf.expertise_fatal_exceptions,
                              self.conf.hook_davai_wagons),
            format         = 'json',
            local          = 'task_summary.[format]',
            namespace      = self.REF_OUTPUT,
            nativefmt      = '[format]',
            promised       = True,
            scope          = 'itself',
            task           = 'expertise')

    def _output_comparison_expertise(self):
        return dict(
            role           = 'TaskAgainstRef',
            kind           = self._taskinfo_kind,
            block          = self.output_block(),
            experiment     = self.conf.xpid,
            hook_train     = ('davai.hooks.take_the_DAVAI_train',
                              self.conf.expertise_fatal_exceptions,
                              self.conf.hook_davai_wagons),
            format         = 'json',
            local          = 'task_[scope].[format]',
            nativefmt      = '[format]',
            scope          = 'continuity,consistency',
            task           = 'expertise')


class DavaiIALTaskMixin(DavaiTaskMixin, IncludesTaskMixin):
    """Provide useful usual outputs for Davai IAL tests."""

    def _promised_listing(self):  # Promised to be able to export its cache/archive path to ciboulai
        return dict(
            role           = 'Listing',
            binary         = '[model]',
            block          = self.output_block(),
            experiment     = self.conf.xpid,
            format         = 'ascii',
            kind           = 'plisting',
            local          = 'NODE.001_01',
            namespace      = self.REF_OUTPUT,
            promised       = True,
            seta           = '1',
            setb           = '1',
            task           = self._configtag)

    def _output_listing(self):
        return dict(
            role           = 'Listing',
            binary         = '[model]',
            block          = self.output_block(),
            experiment     = self.conf.xpid,
            format         = 'ascii',
            kind           = 'plisting',
            local          = 'NODE.{glob:a:\d+}_{glob:b:\d+}',
            namespace      = self.REF_OUTPUT,
            promised       = True,
            seta           = '[glob:a]',
            setb           = '[glob:b]',
            task           = self._configtag)

    def _output_stdeo(self):
        return dict(
            role           = 'StdOut',
            binary         = '[model]',
            block          = self.output_block(),
            experiment     = self.conf.xpid,
            format         = 'ascii',
            kind           = 'plisting',
            local          = 'stdeo.{glob:n:\d+}',
            part           = 'stdeo.[glob:n]',
            task           = self._configtag)

    def _output_drhook_profiles(self):
        return dict(
            role           = 'DrHookProfiles',
            binary         = '[model]',
            block          = self.output_block(),
            experiment     = self.conf.xpid,
            fatal          = self.conf.drhook_profiling,
            format         = 'ascii',
            kind           = 'drhook',
            local          = 'drhook.prof.{glob:n:\d+}',
            mpi            = '[glob:n]',
            task           = self._configtag)

