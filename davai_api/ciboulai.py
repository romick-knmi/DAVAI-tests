#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Useful objects/functions.
"""

from __future__ import print_function, absolute_import, division, unicode_literals
import six

import json
import sys
import os

from bronx.stdtypes import date
import ial_expertise

from . import __version__


class XPMetadata(object):
    """Collect metadata about XP and save it."""
    env_catalog_variables = ('APPENV', 'APPENV_LAM', 'APPENV_GLOBAL',
                             'APPENV_CLIM', 'COMMONENV')

    def __init__(self, xpid):
        ref_xpid = os.environ.get('REF_XPID')
        if ref_xpid == xpid:
            ref_xpid = None
        self._dict = {'xpid':xpid,
                      'initial_time_of_launch':date.utcnow().isoformat().split('.')[0],
                      'davai_api':__version__,
                      'ial_expertise':ial_expertise.__version__,
                      'user':os.environ['USER'],
                      # absent-safe
                      'ref_xpid':ref_xpid,
                      'usecase':os.environ.get('USECASE'),
                      'IAL_git_ref':os.environ.get('IAL_GIT_REF'),
                      'comment':os.environ.get('COMMENT'),
                      }
        self._dict.update(self._gmkpack_info())
        for k in self.env_catalog_variables:
            e = os.environ.get(k)
            if e:
                self.set(k.lower(), e)
        for k in ('INPUT_STORE', 'INPUT_STORE_LAM', 'INPUT_STORE_GLOBAL',
                  'INPUT_SHELF', 'INPUT_SHELF_LAM', 'INPUT_SHELF_GLOBAL'):
            s = os.environ.get(k)
            if s:
                self.set(k.lower(), s)
        self._set_details()

    def _gmkpack_info(self):
        from ia4h_scm.algos import guess_packname
        pack = guess_packname(os.environ.get('IA4H_GITREF', os.environ.get('IAL_GIT_REF')),
                              os.environ.get('GMKPACK_COMPILER_LABEL'),
                              os.environ.get('GMKPACK_PACKTYPE'),
                              os.environ.get('GMKPACK_COMPILER_FLAG'))
        return {'gmkpack_packname':pack,
                'homepack':os.environ.get('HOMEPACK'),
                'rootpack':os.environ.get('ROOTPACK'),
                'GMKPACK_COMPILER_LABEL':os.environ.get('GMKPACK_COMPILER_LABEL'),
                'GMKPACK_COMPILER_FLAG':os.environ.get('GMKPACK_COMPILER_FLAG'),
                'pack':pack,  # CLEANME: to be pruned at some point
                }

    def set(self, k, v):
        self._dict[k] = v

    def get(self, k=None):
        if k is None:
            return copy.copy(self._dict)
        else:
            return self._dict[k]

    @property
    def _which_env_catalog_details(self):
        """Get keys and values of necessary env-catalogs to be detailed."""
        return {k.lower():self._dict.get(k.lower())
                for k in self.env_catalog_variables
                if k.lower() in self._dict}

    @classmethod
    def _get_env_catalog_details(cls, env):
        from gco.tools import uenv, genv
        if any([env.startswith(scheme) for scheme in ('uget:', 'uenv:')]):
            # uenv
            details = uenv.nicedump(env,
                                    scheme='uget',
                                    netloc='uget.multi.fr')
        else:
            # genv
            details = ['%s="%s"' % (k, v)
                       for (k, v) in genv.autofill(env).items()]
        return details

    def _set_details(self):
        for k, env in self._which_env_catalog_details.items():
            details = self._get_env_catalog_details(env)
            self._dict['{}_details'.format(k.lower())] = '<br>'.join(details)

    def write(self):
        """Dump in file (xpinfo.json)."""
        with open('xpinfo.json', 'w') as out:
            json.dump(self._dict, out, indent=4, sort_keys=True)
