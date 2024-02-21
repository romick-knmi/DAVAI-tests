#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Hooks on resources for Davai tasks.
"""
from __future__ import print_function, absolute_import, unicode_literals, division


def hook_fix_varbc(t, rh, withvarbc):
    """Hook to (de-)activate VarBC on-the-fly in namelist."""
    if 'NAMVAR' in rh.contents:
        if withvarbc:
            print("Set ['NAMVAR']['LVARBC'] = True")
            rh.contents['NAMVAR']['LVARBC'] = True
            print("Set ['NAMVAR']['LTOVSCV'] = True")
            rh.contents['NAMVAR']['LTOVSCV'] = True
        else:
            print("Set ['NAMVAR']['LVARBC'] = False")
            rh.contents['NAMVAR']['LVARBC'] = False
            print("Set ['NAMVAR']['LTOVSCV'] = False")
            rh.contents['NAMVAR']['LTOVSCV'] = False
    rh.save()


def hook_disable_fullpos(t, rh):
    """Hook to disable FullPos (incomplete???)."""
    if 'NAMFPC' in rh.contents:
        print("Set ['NAMFPC']['NFPCLI'] = 0")
        rh.contents['NAMFPC']['NFPCLI'] = 0
    if 'NAMPHYDS' in rh.contents:
        print("Set ['NAMPHYDS']['NPPVCLIX'] = 0")
        rh.contents['NAMPHYDS']['NPPVCLIX'] = 0
    rh.save()


def hook_disable_flowdependentb(t, rh):
    """Hook to disable flow-dependent B (model namelist)."""
    if 'NAMJG' in rh.contents:
        print("Set ['NAMJG']['CONFIG%LSPFCE'] = True")
        rh.contents['NAMJG']['CONFIG%LSPFCE'] = True
    if 'NAMWAVELETJB' in rh.contents:
        print("Set ['NAMWAVELETJB']['WJBCONF%LJBWAVELET'] = False")
        rh.contents['NAMWAVELETJB']['WJBCONF%LJBWAVELET'] = False
    if 'NAMVAR' in rh.contents:
        print("Set ['NAMVAR']['LUSEWAVRENORM'] = False")
        rh.contents['NAMVAR']['LUSEWAVRENORM'] = False
    rh.save()


def hook_fix_model(t, rh, NDVar, tstep, isCNT0):
    """
    Hook for model namelist
    """
    if NDVar == '3DVar':
        # 3DVar case
        if 'NAMRIP' in rh.contents:
            print("Set ['NAMRIP']['CSTOP'] = 'h0'")
            rh.contents['NAMRIP']['CSTOP'] = 'h0'
    if 'NAMRIP' in rh.contents:
        print("Set ['NAMRIP']['TSTEP'] = 1800.")
        rh.contents['NAMRIP']['TSTEP'] = 1800
    if NDVar == '4DVar':
        # 4DVar case
        if 'NAMRIP' in rh.contents:
            print("Set ['NAMRIP']['CSTOP'] = 'h3'")
            rh.contents['NAMRIP']['CSTOP'] = 'h3'
            print("Set ['NAMRIP']['TSTEP'] = ", tstep)
            rh.contents['NAMRIP']['TSTEP'] = int(tstep)
    if isCNT0:
        if 'NAMOOPS' in rh.contents:
            rh.contents['NAMOOPS'].delvar('LMODEL_WITH_SPECRT')
        if 'NAMSIMPHL' in rh.contents:
            print("Set ['NAMSIMPHL']['LTRAJPST'] = .FALSE.")
            rh.contents['NAMSIMPHL']['LTRAJPST'] = False
            print("Set ['NAMSIMPHL']['LTRAJPS'] = .FALSE.")
            rh.contents['NAMSIMPHL']['LTRAJPS'] = True
    rh.save()


def hook_adjust_DFI(t, rh, NDVar):
    """
    Runtime tuning of DFI in Screening:

    - unplug DFI in 3DVar case
    - or tune number of steps to timestep
    """
    if NDVar == '3DVar':
        # because no DFI in 3DVar screening (and avoiding to duplicate model namelists)
        print("Unplug DFI")
        if 'NAMINI' in rh.contents:
            rh.contents['NAMINI']['LDFI'] = False
            rh.contents['NAMINI'].delvar('NEINI')
        if 'NAMDFI' in rh.contents:
            rh.contents['NAMDFI'].delvar('NEDFI')
            rh.contents['NAMDFI'].delvar('NTPDFI')
            rh.contents['NAMDFI'].delvar('TAUS')
        if 'NAMRIP' in rh.contents:
            rh.contents['NAMRIP']['CSTOP'] = 'h0'
    else:
        # Because timestep is not that of the operational screening
        print("Adjust NSTDFI to timestep")
        rh.contents['NAMDFI']['NSTDFI'] = 6
    rh.save()


def hook_gnam(t, rh, gnam_as_dict):
    """Modify a namelist based on a dict(BLOCK={KEY:VALUE, ...}, ...)"""
    from bronx.datagrip.namelist import NamelistSet
    gnam = NamelistSet()
    for blockname, block in gnam_as_dict.items():
        for key, value in block.items():
            print("Gnam setting: {}:{} = {}".format(blockname, key, value))
            if blockname not in gnam:
                gnam.newblock(blockname)
            gnam[blockname][key] = value
    rh.contents.merge(gnam)
    rh.save()


def hook_OOPS_2_CNT0(t, rh):
    """Hook to turn OOPS namelist into CNT0 namelist."""
    gnam = {'NAMARG': {'CNMEXP':'MINI'},
            'NAMCT0': {'L_OOPS':False}}
    hook_gnam(t, rh, gnam)


def hook_ensemble_build(t, rh, nbmembers):
    """Hook to build namelist files for members of an ensemble."""
    naml_fmt = "naml_write_dx_m{:03}"
    for mb in range(1, int(nbmembers)+1):
        fnaml = naml_fmt.format(mb)
        naml = open(fnaml, 'w')
        naml.write('&NAMOOPSWRITE\n')
        naml.write('  LWRSPEC=.TRUE.,\n')
        naml.write('  LWRSPECA_GP=.TRUE.,\n')
        naml.write('  LWRSPECA_GP_UV=.TRUE.,\n')
        naml.write('  LINC=.FALSE.,\n')
        naml.write('  CDMEXP="M{:03}",\n'.format(mb))
        naml.write('/\n')
        naml.close()
