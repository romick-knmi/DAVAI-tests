DAVAI tests templates and running interface
===========================================

This project contains the necessary files to run the DAVAI tests.

It is composed of:
- tasks templates | `src/tasks`
- configuration files to implement actual tasks | `conf`
- wrappers to setup a DAVAI experiment, build executables from git, and run the families of tests | `src/runs`
- toolbox of utilities for DAVAI experiments and tasks | `src/davai_taskutil`

Installation
------------

Should be installed by the `davai-init` command of the [DAVAI-env](https://github.com/ACCORD-NWP/DAVAI-env) project.

Correspondance of tests version with IAL code to be tested
----------------------------------------------------------

To be used in `davai-prep_xp -v <davai_tests_version> ...`

| _What to test_ | Basis of the dev | Nominal tests version | Reference XPID |
|:-----------------|:-----------------|:----------------------|:---------------|
| Merge branch CY49 | `CY48T3` (tag) | `DV48T3` (tag) | ...tbd... |
| 48T3 dev branch | `mary_CY48T2_to_T3` (branch) | `dev` (branch) | `dv-0016-belenos@moureauxm` |
| Development on top of `48T2` | `CY48T2` (tag) | `DV48T2` (tag) | `dv-0016-belenos@moureauxm` |
| Dble branch `gco_CY48T1_op1` | `gco_CY48T1_op1` (branch) | `dev_DV48T1_op1` (branch) | ...tbd... |
| Development on top of `48T1_op0.04` | `CY48T1_op0.04` (tag) | `DV48T1_op0.04` (tag) | `dv-0016-belenos@moureauxm` |
