import os
from configparser import ConfigParser
from pathlib import Path
from scr.space_exceptions import *
from scr.Config_Names import config_naming
import re
import json
from loguru import logger

# Regex-str to determine a legitimate filename

class Section_Sync:
	name: str
	prefix: str
	dst_path: Path
	scr_path: Path
	#online_repo: str 			# not yet implemented
	blacklist: list[str]
	whitelist: list[str]
	#config_files: dict[str,str] #TODO: key=str(path) val=date(last-modified-time)
	#repro_files: dict[str,str]
	__filename_regex = "^[A-Za-z0-9_-]+$"

	def __init__(self, section_cfg: ConfigParser):
		self.name = section_cfg.name # the [<section_name>] from the cfg-file
		try:
			self._check_set_section_properties(section_cfg)
		except Exception as e:
			raise ConfigurationError(e)
	
	def __repr__(self) -> str:
		return (f"Section_Sync("
				f"name='{self.name}', "
				f"prefix='{self.prefix}', "
				f"dst_path='{self.dst_path}', "
				f"scr_path='{self.scr_path}', "
				f"blacklist={self.blacklist}, "
				f"whitelist={self.whitelist})")
		
	def _check_set_section_properties (self, section):
		"""Checking if given Section is in a readable shape and all paths are accessible as expected.

		Args:
			section (ConfigParser): A Section in an *.cfg Config file

		Raises:
			MissingCFGSectionPropertyError: Missing the named element form the given Section
			InvalidConfigValueError: Invalid element-value given in the specified Section-element
			FileNotFoundError: Given Path not found
			PermissionError: Cant access given path with read or write permission - see output

		Returns:
			None: No Return
		"""
		# check if all section-property's are present
		if config_naming.prefix not in section:
			raise MissingCFGSectionPropertyError(f"{config_naming.prefix}")
		if config_naming.dst_path not in section:
			raise MissingCFGSectionPropertyError(f"{config_naming.dst_path}")
		if config_naming.scr_path not in section:
			raise MissingCFGSectionPropertyError(f"{config_naming.scr_path}")
		if config_naming.blacklist not in section:
			raise MissingCFGSectionPropertyError(f"{config_naming.blacklist}")
		if config_naming.whitelist not in section:
			raise MissingCFGSectionPropertyError(f"{config_naming.whitelist}")

		
		# check for valid <instance_prefix> != ""
		try:
			match = re.fullmatch(self.__filename_regex, section[config_naming.prefix])
		except Exception as e:
			raise InvalidConfigValueError(f"broken instance_prefix({section[config_naming.prefix]}) was given! see: Error: {e}")
		if match is None: # No mach was found
			raise InvalidConfigValueError(f"invalid instance_prefix given! only chars, digits, _ and - are allowed")
		# set the prefix
		self.prefix = section[config_naming.prefix]


		# read & check destination- and source-path
		if (not section[config_naming.dst_path]):
			raise InvalidConfigValueError(f"config repro paths should not be empty")
		if (not section[config_naming.scr_path]):
			raise InvalidConfigValueError(f"git repro paths should not be empty")
		## Set paths and resolve Environment variables and also (~) syntax
		dst_cfg_path = os.path.expandvars(section[config_naming.dst_path])
		dst_cfg_path = Path(dst_cfg_path).expanduser()
		scr_cfg_path = os.path.expandvars(section[config_naming.scr_path])
		scr_cfg_path = Path(scr_cfg_path).expanduser()
			#logger.debug(f"DBG: given config path: {para_section[config_naming.local_config_path]} was made to {config_path}")
			#logger.debug(f"DBG: given git-repro path: {para_section[config_naming.local_git_repro]} was made to {repro_path}")
		## check for valid paths
		if not (dst_cfg_path.exists()):
			raise FileNotFoundError(f"Config-path: ({dst_cfg_path})")
		if not dst_cfg_path.is_dir():
			raise InvalidConfigValueError(f"Config-path({dst_cfg_path}) is no Directory")
		if not (scr_cfg_path.exists()):
			raise FileNotFoundError(f"Repro-path: ({scr_cfg_path})")
		if not scr_cfg_path.is_dir():
			raise InvalidConfigValueError(f"Repro-path({scr_cfg_path}) is no Directory")
		## check for r/w rights on config_path and r/- rights on repro_path
		### TODO: do a proper test of this code!
		if not os.access(scr_cfg_path, os.R_OK):
			raise PermissionError(f"with reading on Repro-Path: {scr_cfg_path}")
		if not os.access(dst_cfg_path, os.R_OK):
			raise PermissionError(f"with reading on Config-Path: {dst_cfg_path}")
		if not os.access(dst_cfg_path, os.W_OK):
			raise PermissionError(f"with writing on Config-Path: {dst_cfg_path}")
		
		self.dst_path = dst_cfg_path
		self.scr_path = scr_cfg_path
		
		
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
		## TODO: get all json-files(paths) with the prefix in both dir's
		## TODO: Create a Dictionary in which all paths from the repro-dir gets tagged with {new,old or pass}
		### {new} for a new not existing file
		### {old} for an existing file thats outdated
		### {pass} for an existing file thats up-to-date

		for f in self.dst_path.walk():
			# check if file needs to be sychroniced == {instance_prefix}[a-z].*\.json$
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
