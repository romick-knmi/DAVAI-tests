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
    
    _gmkpack_build_block = 'pack_compile_link'

    def _gmkpack_check_build(self, expertise_rh):
        gmkpack_expertise = expertise_rh.contents.data['gmkpack_build']
        compil_OK = gmkpack_expertise['All OK']
        if compil_OK:
            print("Build successful !")
        else:
            print("Builds failed:", gmkpack_expertise['Executables failed'])
            exit(1)

    @property
    def build_block(self):
        """Vortex block of the task that builds executables."""
        if self.conf.building_system == 'gmkpack':
            return self._gmkpack_build_block
        else:
            raise NotImplementedError("building_system:{}".format(self.conf.building_system))

    def check_build(self, expertise_rh):
        """Check in expertise that executables have been successfully built."""
        if self.conf.building_system == 'gmkpack':
            self._gmkpack_check_build(expertise_rh)
        else:
            raise NotImplementedError("building_system:{}".format(self.conf.building_system))


    def get_expertise(self):
        """Get expertise, waiting for it if necessary."""
        t = self.ticket
        sh = self.sh
        expertise_description = dict(
            kind           = 'taskinfo',
            block          = self.build_block,
            experiment     = self.conf.xpid,
            format         = 'json',
            local          = 'compilation_output.[format]',
            namespace      = 'vortex.cache.fr',
            nativefmt      = '[format]',
            scope          = 'itself',
            task           = 'expertise',)
        # timings
        now = time.time()
        walltime = self.conf.time
        walltime_in_seconds = sum([60**(2-i) * int(v)
                                   for i,v in enumerate(walltime.split(':'))]
                                  ) + 600  # a large 10 mins margin for step.01 of packbuild
        walltime += '(+ 10:00 margin)'

        def expertise_available():
            ok = False
            exists = bool(toolbox.rload(**expertise_description)[0].check())
            if exists:
                mtime = self.sh.path.getmtime(toolbox.rload(**expertise_description)[0].locate())
                if mtime > now:
                    ok = True
            return ok
 
        # get compilation task time (e.g. 02:00:00) in seconds
        print("Begin waiting for Compilation expertise, for up to",
              "{} == {} seconds".format(walltime, walltime_in_seconds))
        while not expertise_available():
            # wait for compilation expertise to be present in cache
            if walltime_in_seconds <= 0:
                raise RuntimeError("Could not get Compilation expertise after supposed maximum Elapsed time.")
            print("Time to expiration: {:5d} (s)".format(walltime_in_seconds))
            wait = 30
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
        # get compilation expertise
        expertise = self.get_expertise()
        # check that all builds are successful
        self.check_build(expertise)


