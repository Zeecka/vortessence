# Volatility
# Copyright (C) 2007-2013 Volatility Foundation
#
# This file is part of Volatility.
#
# Volatility is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Volatility is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Volatility.  If not, see <http://www.gnu.org/licenses/>.
#

"""
@author:       Andrew Case
@license:      GNU General Public License 2.0
@contact:      atcuno@gmail.com
@organization: 
"""

import volatility.obj as obj
import volatility.plugins.linux.common as linux_common
import volatility.plugins.linux.pslist as linux_pslist
from volatility.renderers import TreeGrid
from volatility.renderers.basic import Address

class linux_proc_maps(linux_pslist.linux_pslist):
    """Gathers process memory maps"""

    def calculate(self):
        linux_common.set_plugin_members(self)
        tasks = linux_pslist.linux_pslist.calculate(self)

        for task in tasks:
            if task.mm:
                for vma in task.get_proc_maps():
                    yield task, vma            

    def unified_output(self, data):
        return TreeGrid([("Pid", int),
                       ("Start", Address),
                       ("End", Address),
                       ("Flags", str),
                       ("Pgoff", Address),
                       ("Major", int),
                       ("Minor", int),
                       ("Inode", int),
                       ("Path", str)],
                        self.generator(data))

    def generator(self, data):
        for task, vma in data:
            (fname, major, minor, ino, pgoff) = vma.info(task)

            yield (0, [int(task.pid),
                Address(vma.vm_start),
                Address(vma.vm_end),
                str(vma.vm_flags),
                Address(pgoff),
                int(major),
                int(minor),
                int(ino),
                str(fname)])
