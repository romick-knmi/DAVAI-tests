# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

import footprints.util

import vortex
from vortex import toolbox
from vortex.layout.nodes import Task, Driver

import davai


def setup(t, **kw):
    return Driver(
        tag     = 'setup',
        ticket  = t,
        nodes   = [
            CiboulaiXpSetup(tag='ciboulai_xpsetup', ticket=t, **kw),
        ],
        options=kw
    )


class CiboulaiXpSetup(Task):
    conf2env = ('IA4H_gitref',  # for packname
                'gmkpack_compiler_label', 'gmkpack_packtype', 'gmkpack_compiler_flag',  # for packname
                'HOMEPACK',  # for packname (path)
                'comment', 'usecase', 'ref_xpid',  # the xp itself
                'appenv_LAM', 'appenv_global', 'commonenv', 'appenv_clim',  # shelves: env
                'input_store_LAM', 'input_store_global',  # shelves: input stores
                )
    def _set_env_from_conf(self):
        """Export some conf variables to environment."""
        for v in self.conf2env:
            if v in self.conf and v.upper() not in self.env:
                self.env.setvar(v.upper(), self.conf.get(v))
    
    def process(self):
        t = self.ticket
        sh = self.sh
        self._set_env_from_conf()

        if 'compute' in self.steps or 'early-fetch' in self.steps:  # it should run on transfert nodes
            sh.title('Toolbox algo tb01 = tbalgo')
            tb01 = tbalgo = toolbox.algo(
                engine         = 'algo',
                kind           = 'xpsetup',
                xpid           = self.conf.xpid,
            )
            print(t.prompt, 'tb01 =', tb01)
            print()
            tbalgo.run(None)

        if 'late-backup' in self.steps:
            sh.title('Toolbox output tb02')
            tb02 = toolbox.output(
                role           = 'XPinfo',
                block          = 'summaries_stack',
                experiment     = self.conf.xpid,
                format         = 'json',
                hook_send      = ('davai.hooks.send_to_DAVAI_server', self.conf.expertise_fatal_exceptions),
                kind           = 'xpinfo',
                local          = 'xpinfo.[format]',
                namespace      = self.conf.namespace,
                nativefmt      = '[format]',
            )
            print(t.prompt, 'tb02 =', tb02)
            print()


