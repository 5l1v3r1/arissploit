#!/usr/bin/env python3

#            ---------------------------------------------------
#                           Arissploit Framework                                 
#            ---------------------------------------------------
#                Copyright (C) <2019-2020>  <Entynetproject>
#
#        This program is free software: you can redistribute it and/or modify
#        it under the terms of the GNU General Public License as published by
#        the Free Software Foundation, either version 3 of the License, or
#        any later version.
#
#        This program is distributed in the hope that it will be useful,
#        but WITHOUT ANY WARRANTY; without even the implied warranty of
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#        GNU General Public License for more details.
#
#        You should have received a copy of the GNU General Public License
#        along with this program.  If not, see <http://www.gnu.org/licenses/>.

from core.exceptions import UnknownCommand
from core.exceptions import ModuleNotFound
from core.exceptions import VariableError
from core import cmethods
from core.module_manager import ModuleManager
from core import colors

class Commandhandler:
	mm = None
	notcommand = ["mcu"]
	cm = None
	api = False

	def __init__(self, gmm, enableapi):
		self.mm = gmm
		self.cm = cmethods.Cmethods(self.mm)
		if enableapi == True:
			self.api = True

	def handle(self, command):
		# String to list
		command = command.split()

		# Custom command
		if self.mm.moduleLoaded == 1:
				try:
					return self.cm.mcu(command)
				except IndexError:
					return
				except UnknownCommand:
					pass

		# Validate command

		if len(command) != 0 and command[0] in self.notcommand:
			print("["+colors.bold+colors.red+"err"+colors.end+"] Unrecognized command!"+colors.end)
			return
		try:
			method = getattr(self.cm, command[0])
		except AttributeError:
			print("["+colors.bold+colors.red+"err"+colors.end+"] Unrecognized command!"+colors.end)
			return
		except IndexError:
			return

		try:
			return method(command[1:])
		except UnknownCommand:
			print("["+colors.bold+colors.red+"err"+colors.end+"] Unrecognized command!"+colors.end)

		except ModuleNotFound:
			if self.api == True:
				raise ModuleNotFound("["+colors.bold+colors.red+"err"+colors.end+"] Module is not found!")

		except VariableError:
			if self.api == True:
				raise VariableError("["+colors.bold+colors.red+"err"+colors.end+"] Variable error!")
