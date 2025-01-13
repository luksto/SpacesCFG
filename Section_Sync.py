import configparser
import os
from pathlib import Path
from space_exceptions import *
from Config_Names import config_naming
import re
import json


# Regex-str to determine a legitimate filename
filename_regex = "^[A-Za-z0-9_-]+$"

class Section_Sync:
	name: str
	id: str
	config_dir: Path
	repro_dir: Path
	blacklist: list[str]
	whitelist: list[str]
	config_files: dict[str,str] #TODO: key=str(path) val=date(last-modified-time)
	repro_files: dict[str,str]

	def __init__(self, section_cfg: configparser.ConfigParser):
		self.name = section_cfg.name
		try:
			self._check_set_section_properties(section_cfg)
		except Exception as e:
			raise ConfigurationError(e)
		
	def _check_set_section_properties (self, section):
		"""Checking if given Section is in a readable shape and all paths are accessible as expected.

		Args:
			section (configparser.ConfigParser): A Section in an *.cfg Config file

		Raises:
			MissingCFGSectionPropertyError: Missing the named element form the given Section
			InvalidConfigValueError: Invalid element-value given in the specified Section-element
			FileNotFoundError: Given Path not found
			PermissionError: Cant access given path with read or write permission - see output

		Returns:
			None: No Return
		"""
		# check if all section-property's are present
		if config_naming.instance_id not in section:
			raise MissingCFGSectionPropertyError(f"{config_naming.instance_id}")
		if config_naming.local_config_path not in section:
			raise MissingCFGSectionPropertyError(f"{config_naming.local_config_path}")
		if config_naming.local_git_repro not in section:
			raise MissingCFGSectionPropertyError(f"{config_naming.local_git_repro}")
		if config_naming.blacklist not in section:
			raise MissingCFGSectionPropertyError(f"{config_naming.blacklist}")
		if config_naming.whitelist not in section:
			raise MissingCFGSectionPropertyError(f"{config_naming.whitelist}")

		
		# check for valid <instance_id> != ""
		try:
			match = re.fullmatch(filename_regex, section[config_naming.instance_id])
		except Exception as e:
			raise InvalidConfigValueError(f"broken instance_id({section[config_naming.instance_id]}) was given! see: Error: {e}")
		if match: # No mach was found
			raise InvalidConfigValueError(f"invalid instance_id given! only chars, digits, _ and - are allowed")
		
		self.id = section[config_naming.instance_id]


		# read & check config- and git-path
		if (not section[config_naming.local_config_path]):
			raise InvalidConfigValueError(f"config repro paths should not be empty")
		if (not section[config_naming.local_git_repro]):
			raise InvalidConfigValueError(f"git repro paths should not be empty")
		## Set paths and resolve Environment variables and also (~) syntax
		config_path = os.path.expandvars(section[config_naming.local_config_path])
		config_path = Path(config_path).expanduser()
		repro_path = os.path.expandvars(section[config_naming.local_git_repro])
		repro_path = Path(repro_path).expanduser()
			#print(f"DBG: given config path: {para_section[config_naming.local_config_path]} was made to {config_path}")
			#print(f"DBG: given git-repro path: {para_section[config_naming.local_git_repro]} was made to {repro_path}")
		## check for valid paths
		if not (config_path.exists()):
			raise FileNotFoundError(f"Config-path: ({config_path})")
		if not config_path.is_dir():
			raise InvalidConfigValueError(f"Config-path({config_path}) is no Directory")
		if not (repro_path.exists()):
			raise FileNotFoundError(f"Repro-path: ({repro_path})")
		if not repro_path.is_dir():
			raise InvalidConfigValueError(f"Repro-path({repro_path}) is no Directory")
		## check for r/w rights on config_path and r/- rights on repro_path
		### TODO: do a proper test of this code!
		if not os.access(repro_path, os.R_OK):
			raise PermissionError(f"with reading on Repro-Path: {repro_path}")
		if not os.access(config_path, os.R_OK):
			raise PermissionError(f"with reading on Config-Path: {config_path}")
		if not os.access(config_path, os.W_OK):
			raise PermissionError(f"with writing on Config-Path: {config_path}")
		
		self.config_dir = config_path
		self.repro_dir = repro_path
		
		
		# check ether for whitelisting or blacklisting:
		## if <whitelist> is not empty
		try:
			whitelist = json.loads(section.get(config_naming.whitelist))
		except Exception as e:
			raise InvalidConfigValueError(f"whitelist data is in non readable shape! See: {e}")

		try:
			blacklist = json.loads(section.get(config_naming.blacklist))
		except Exception as e:
			raise InvalidConfigValueError(f"blacklist data is in non readable shape! See: {e}")
		
		self.whitelist = whitelist
		self.blacklist = blacklist
		
		return True

	def sync(self) -> bool:
		# Brainstorming
		## Possible Synchronisation Cases:
		### all New: No file from repro_dir should exists in config_dir and therefore all files will get syced(linked) to the config dir
		### new files in repro_dir: these one gets additional linked to the config_dir
		### removed file in repro_dir: links are not working anymore and should be removed
		### renamed file in repro_dir: TODO how to recorgnice a renaming? to be able to redirect the link?
		#### => old link is not valid: => remove it
		#### => new name(file-link) does not exists => create new link!
		#### => done! :)
		if self.whitelist != [] and self.blacklist != []:
			raise InvalidConfigValueError(f"Whitelisting and Blacklisting on the same time is not supported atm!")
		if self.whitelist != []:
			self.__sync_whitelisting()
			return
		if self.blacklist != []:
			self.__sync_blacklisting()
			return
		
		# Start Synchronizing all files from the repro to the config directory
		## TODO: get all json-files(paths) with the "id_" as prefix in both dir's
		## TODO: Create a Dictionary in which all paths from the repro-dir gets tagged with {new,old or pass}
		### {new} for a new not existing file
		### {old} for an existing file thats outdated
		### {pass} for an existing file thats up-to-date

		for f in self.config_dir.walk():
			# check if file needs to be sychroniced == {instance_id}[a-z].*\.json$
			# TODO: if match: => add file and date to config_files dictionary
			pass
		# TODO: same for repro_dir and repro_files dictionary
		
		# Compare repro_files and config_files dictonary in path-names and newer dates
		# TODO: get overlaping key-value pares


		# Go thro the dictionary and start the appropriate synchronization function for each path(file)
		## TODO:

	def __sync_new(self, r_path: Path, c_path: Path):
		# TODO: Copy the r(repro)_path to the c(config)_path
		pass

	def __sync_old(self, r_path: Path, c_path: Path):
		# TODO: Update the c(config)_path on the destination with the newer file in r(repro)_path
		pass

	def __sync_whitelisting(self):
		pass

	def __sync_blacklisting(self):
		pass
