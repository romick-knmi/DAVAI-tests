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

| _What to test_ | Basis of the dev | Nominal tests version | Reference XPID |
|:-----------------|:-----------------|:----------------------|:---------------|
| Merge branch CY49 | `tag: CY48T3` | ??? | ??? |
| 48T3 dev branch | `branch: mary_CY48T2_to_T3` | `branch: dev` | `dv-0120@mary` |
| Development on top of 48T2 | `tag: CY48T2` | `tag: DV48T2` | `dv-0120@mary` |
