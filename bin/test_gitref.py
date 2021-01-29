#/usr/bin/env python
"""
Create a Davai experiment based on a **gitref**.

syntax: test_gitref.py <gitref> [--usecase ELP] [--repository ~/repositories/arpifs]
"""

# mkdir $TMPDIR/<gitref>@<user>/davai/<usecase>/
# copy tasks/ and conf/
# set <gitref> and others in conf/davai_<usecase>.ini
# copy runs/?? (depending on <usecase>
# make links: vortex, davai_tbx, epygram, ia4h_scm
