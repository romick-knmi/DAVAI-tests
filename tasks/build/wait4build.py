# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

import footprints.util
import time

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task, Driver

import common


def setup(t, **kw):
    return Driver(
        tag     = 'setup',
        ticket  = t,
        nodes   = [
            Wait4Build(tag='packbuild', ticket=t, **kw),
        ],
        options=kw
    )


class Wait4Build(Task):
    
    def _expertise_available(self, start_of_run, **expertise_description):
        """Check if expertise is available and posterior to run start."""
        ok = False
        exists = bool(toolbox.rload(**expertise_description)[0].check())
        #print(toolbox.rload(**expertise_description)[0].locate())
        if exists:
            last_modified_time = self.sh.path.getmtime(toolbox.rload(**expertise_description)[0].locate())
            if last_modified_time > start_of_run:
                ok = True
        return ok

    def check_build(self, expertise_rh):
        """Check in expertise if task succeeded."""
        expertise = expertise_rh.contents.data
        task_OK = expertise['Status']['short'].startswith('Ended')
        if not task_OK:
            print("Task failed:", expertise['Exception'])
            exit(1)
 
    def get_expertise(self, **expertise_description):
        """Get expertise, waiting for it if necessary."""
        t = self.ticket
        sh = self.sh
        # timings
        start_of_run = float(self.sh.environ.get('DAVAI_START_BUILD', time.time()))
        walltime = self.conf.time
        # get compilation task time (e.g. 02:00:00) in seconds
        walltime_in_seconds = sum([60**(2-i) * int(v)
                                   for i,v in enumerate(walltime.split(':'))]
                                  ) + 600  # a large 10 mins margin for step.01 of packbuild
        walltime += '(+ 10:00 margin for queueing)'
        print("Begin waiting for '{}' expertise, for up to".format(expertise_description['block']),
              "{} == {} seconds".format(walltime, walltime_in_seconds))
        # start waiting for expertise
        while not self._expertise_available(start_of_run, **expertise_description):
            # wait for compilation expertise to be present in cache
            if walltime_in_seconds <= 0:
                print("Could not get expertise after supposed maximum Elapsed time: check manually. Exit")
                exit(-1)
            print("Time to expiration: {:5d} (s)".format(walltime_in_seconds))
            wait = 10
            time.sleep(wait)
            walltime_in_seconds -= wait
        else:
            # expertise available: continue
            print("Expertise available !")
            # fetch it
            expertise = toolbox.input(**expertise_description)
            print(t.prompt, 'expertise =', expertise)
        return expertise[0]

    def process(self):
        expertise_description = dict(
            kind           = 'taskinfo',
            experiment     = self.conf.xpid,
            format         = 'json',
            local          = 'compilation_output.[format]',
            namespace      = 'vortex.cache.fr',
            nativefmt      = '[format]',
            scope          = 'itself',
            task           = 'expertise',)
        for block in ('gitref2pack', 'pack_compile_link'):
            # get compilation expertise
            expertise = self.get_expertise(block=block, **expertise_description)
            # check that all builds are successful
            self.check_build(expertise)

