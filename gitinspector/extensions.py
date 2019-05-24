# coding: utf-8
#
# Copyright © 2012-2015 Ejwa Software. All rights reserved.
#
# This file is part of gitinspector.
#
# gitinspector is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gitinspector is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gitinspector. If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

DEFAULT_EXTENSIONS = ["ada", "adb", "ads", "java", "c", "cc", "cpp", "cs", "json", "h", "hh", "html", "hpp", "hs",
                      "php", "pl", "py", "po", "pot", "rb", "scala", "tf", "js", "sh", "sql", "xml", "yml"]

__extensions__ = DEFAULT_EXTENSIONS
__located_extensions__ = set()


def get():
    return __extensions__


def define(string):
    global __extensions__
    __extensions__ = string.split(",")


def add_located(string):
    if len(string) == 0:
        __located_extensions__.add("*")
    else:
        __located_extensions__.add(string)


def get_located():
    return __located_extensions__
