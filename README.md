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

It is installed as a sub-project of the broader `davai-env` project.

Correspondance of tests version with IAL code to be tested
----------------------------------------------------------

| _What to test_ | Basis of the dev | Nominal tests version | Reference XPID |
|:-----------------|:-----------------|:----------------------|:---------------|
| Contribution to 48T2 | `tag: CY48T1` | `tag: DV48T1` | `0047-CY48T1@mary` |
| 48T2 Integration branch | `branch: CY48T1_toT2` | `branch: DV48T1_toT2` | `0047-CY48T1@mary` (to start with) |

