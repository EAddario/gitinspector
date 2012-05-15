# coding: utf-8
#
# Copyright © 2012 Ejwa Software. All rights reserved.
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

from changes import FileDiff
import comment
import missing
import system

__metric_eloc__ = {"java": 500, "c": 500, "cpp": 500, "h": 300, "hpp": 300, "py": 500, "glsl": 1000,
                   "rb": 500, "js": 500, "sql": 1000, "xml": 1000}

class Metrics:
	def __init__(self, repo, hard):
		self.eloc = {}
		ls_tree_r = system.run(repo, "git ls-tree --name-only -r HEAD")

		for i in ls_tree_r.readlines():
			if FileDiff.is_valid_extension(i):
				if not missing.add(repo, i.strip()):
					file_r = system.open_file(repo, i.strip())
					extension = FileDiff.get_extension(i)
					lines = Metrics.get_eloc(file_r, extension)

					if __metric_eloc__[extension] < lines:
						self.eloc[i.strip()] = lines

	@staticmethod
	def get_eloc(file_r, extension):
		is_inside_comment = False
		eloc_counter = 0

		for j in file_r.readlines():
			if comment.has_comment_begining(extension, j):
				is_inside_comment = True

			if not comment.is_comment(extension, j) and not is_inside_comment:
				eloc_counter += 1

			if comment.has_comment_end(extension, j):
				is_inside_comment = False

		return eloc_counter

def output(repo, hard):
	metrics = Metrics(repo, hard)

	if not metrics.eloc:
		print "\nNo metrics violations were found in the repository."
	else:
		print "\nThe following files are suspiciously big (in order of severity):"
		for i in sorted(set([(j, i) for (i, j) in metrics.eloc.items()]), reverse = True):
			print i[1] + " (" + str(i[0]) + " eloc)"