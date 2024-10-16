import configparser
from pathlib import Path
import json
import re
import os
from sys import exc_info


filename_regex = "^[A-Za-z0-9_-]+$"

class ConfigurationError(Exception):
    pass

class MissingConfigError(ConfigurationError):
    pass

class MissingCFGSectionPropertyError(MissingConfigError):
	pass

class InvalidConfigValueError(ConfigurationError):
    pass

# Configuration Key-Value default pairs
##      [labor-orca] # Labor Space Orca profile Section
##      instance_name       = "LAB"
##      local_config_path   = "~/.config/OrcaSlicer/"
##      git_local_repro     = "~/git/Labor3D_Orca/"
##      file_blacklist      = []
##      file_whitelist       = []

class config_naming:
	instance_id = "instance_name"
	local_config_path = "local_config_path"
	local_git_repro = "git_local_repro"
	blacklist = "file_blacklist"
	whitelist = "file_whitelist"

class Section:
	name: str
	id: str
	config_dir: Path
	repro_dir: Path
	blacklist: list[str]
	whitelist: list[str]

	def __init__(self, section_cfg: configparser.ConfigParser):
		self.name = section_cfg.name
		try:
			self.check_set_section_properties(section_cfg)
		except Exception as e:
			raise ConfigurationError(e)
		
	def check_set_section_properties (self, section):
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
		if (not section[config_naming.local_config_path]) or (not section[config_naming.local_git_repro]):
			raise InvalidConfigValueError(f"config or git repro paths should not be empty")
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
		if self.whitelist != [] and self.blacklist != []:
			raise InvalidConfigValueError(f"Whitelisting and Blacklisting on the same time is not supported atm!")
		if self.whitelist != []:
			self.__sync_whitelisting()
			return
		if self.blacklist != []:
			self.__sync_blacklisting()
			return
		
		# Start Synchronizing all files from the repro to the config directory
		## TODO: get all json paths(files) with the "id_" as prefix in both dir's
		## TODO: Create a Dictionary in which all paths from the repro-dir gets tagged with {new,old or pass}
		### {new} for a new not existing file
		### {old} for an existing file thats outdated
		### {pass} for an existing file thats up-to-date

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

def check_config_parameters(para_cfg_path:str = None) -> tuple[configparser.ConfigParser, str]:
	default_str_cfg_path = "config.cfg"

	# Check and get config file Path
	config_path = 0
	if para_cfg_path is None or para_cfg_path == "":
		config_path = Path(default_str_cfg_path)
		if not config_path.is_file():
			raise FileNotFoundError(f"{default_str_cfg_path}")

	else:
		config_path = Path(para_cfg_path)
		if not config_path.is_file():
			raise FileNotFoundError(f"{para_cfg_path}")

	print(f"LOG: Use cfg-file: {config_path.absolute()}")

	config = configparser.ConfigParser()
	config.read(config_path)

	# Check for space sections
	if len(config.sections()) < 1:
		raise ConfigurationError(f"Config-file does not even hold one section.")

	
	return (config, config_path) #configparser.ConfigParser()
 
def sync_whitelisting(section:configparser.SectionProxy) -> bool:
	# Perform the "sync" based on the <whitelist>
	# read & check all paths is the section
	pass

def sync_blacklisting(section: configparser.SectionProxy) -> bool:
	pass
	

def sync_section(para_section:configparser.SectionProxy) -> bool:
	# All config parameters are set and valid!

	return True
	# check: if <local_config_path> and <local_git_repro> are present in the FS and if we have r/w rights
	# check: if all files listed in <whitelist> are present in <local_git_repro>
		# blacklists does not need to be present, ony test that the syncing file is not on the blacklist
	
	# Sync

	## git-pull/update
	# Update <local_git_repro>
	# Rollback if conflicts happened
	# give easy to resolve tips

	## start syncing (linking) files
	
	## link the (not already lined) - <instance_id> prefixed - files from <local_git_repro> to <local_config_path>
	# build list of files[potential_new_files] in <local_git_repro> that are not blacklisted and have the <instance_id> prefix
	potential_new_files = []

	## clear out the new filelist with all the files in <local_config_path> that are already linked
	# get list of files[linked_files] in <local_config_path> with prefix <instance_id>
	linked_files = []

	# Check: all [potential_new_files] that are present in <local_config_path> needs to be already linked to [potential_new_files]!
	for new in potential_new:
		if new.name in local_config.filenames and local_config.files[new.name].linkpath != "<local_git_repro>/new":
			print(f"ERROR: the File {new.name} is already present in <local_config_path> but not linked to <local_git_repro>/new as it sould be \n\t Please resolve this conflict by ether deleting the file in your <local_config_path> or linke it properly as this app would do it.")
			continue
		


	## link new files
	# create file link from [potential_new_files] to <local_config_path> if not in [linked_files]
	for new in potential_new_files:
		if new in linked_files:
			continue
		# create link from new to local (same filename)





	
	pass


def main(para_cfg_path:str = None) -> bool:
	
	# get the config object
	try:
		(config, path) = check_config_parameters(para_cfg_path)
		print(f"LOG: Configuration loaded successfully from: -{path}- ")
	except FileNotFoundError as e:
		print(f"ERR: File not Found: {e}")
		return False
	except ConfigurationError as e:
		print(f"ERR: bad Configuration: {e}")
		return False
	except e:
		print(f"ERR: Unexpected Error occurred: {e}")
		return False
	
	
	# Start syncing
	# get first config section
	# get section as object
	for section_str in config.sections():
		config_section = config[section_str]
		try:
			working_section = Section(config_section)
		except Exception as e:
			print(f"ERR: Unexpected Exception occures: see: {e}")
			break
		if not working_section:
			continue
		try:
			working_section.sync()
		except Exception as e:
			print(f"ERR: while syncing: see: {e}")
			break
	# DONE!
	print(f"LOG: DONE")



if __name__ == "__main__":
	main()
