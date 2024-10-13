import configparser
from pathlib import Path
import json
import re
import os

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

filename_regex = "^[A-Za-z0-9_-]+$"

def check_config_parameters(para_cfg_path:str = None) -> configparser.ConfigParser:
	default_str_cfg_path = "config.cfg"

	# Check and get config file Path
	config_path = 0
	if para_cfg_path is None or para_cfg_path == "":
		config_path = Path(default_str_cfg_path)
		if not config_path.is_file():
			print(f"ERR: no Path for Config-file is given, and the default path {default_str_cfg_path} is no file")
			return None
	else:
		config_path = Path(para_cfg_path)
		if not config_path.is_file():
			print(f"ERR: given Config file path -{para_cfg_path}- is not available or no file")
			return None
	print(f"LOG: Use cfg-file: {config_path.absolute()}")

	config = configparser.ConfigParser()
	config.read(config_path)

	# Check for space sections
	if len(config.sections()) < 1:
		print("ERR: no Space-section is found, check your config")
		return None
	
	return config #cofigparser.ConfigParser()
 
def sync_whitelisting(section:configparser.SectionProxy) -> bool:
	# Perform the "sync" based on the <whitelist>
	# read & check all pathes is the section
	pass

def sync_blacklisting(section: configparser.SectionProxy) -> bool:
	pass

def sync_section(para_section:configparser.SectionProxy) -> bool:

	# check if all section-propertys are present
	if config_naming.instance_id not in para_section:
		print(f"ERR: {config_naming.instance_id} is missing in {para_section.name}")
		return False
	if config_naming.local_config_path not in para_section:
		print(f"ERR: {config_naming.local_config_path} is missing in {para_section.name}")
		return False
	if config_naming.local_git_repro not in para_section:
		print(f"ERR: {config_naming.local_git_repro} is missing in {para_section.name}")
		return False
	if config_naming.blacklist not in para_section:
		print(f"ERR: {config_naming.blacklist} is missing in {para_section.name}")
		return False
	if config_naming.blacklist not in para_section:
		print(f"ERR: {config_naming.blacklist} is missing in {para_section.name}")
		return False
	
	

	# check for valid <instance_id> != ""
	try:
		match = re.fullmatch(filename_regex, para_section[config_naming.instance_id])
	except:
		print(f"ERR: broken instance_id given! only chars, digits, _ and - are allowed")
		return False
	if match:
		print(f"ERR: invalid instance_id given! only chars, digits, _ and - are allowed")
		return False

	# read & check config- and git-path
	if (not para_section[config_naming.local_config_path]) or (not para_section[config_naming.local_git_repro]):
		print(f"ERR: the config or git repro pathes sould not be empty")
		return False
	## Set pathes and resolve Enviroment variables and also (~) syntax
	config_path = os.path.expandvars(para_section[config_naming.local_config_path])
	config_path = Path(config_path).expanduser()
	repro_path = os.path.expandvars(para_section[config_naming.local_git_repro])
	repro_path = Path(repro_path).expanduser()
		#print(f"DBG: given config path: {para_section[config_naming.local_config_path]} was made to {config_path}")
		#print(f"DBG: given git-repro path: {para_section[config_naming.local_git_repro]} was made to {repro_path}")
	## check for valid paths
	if not (config_path.exists() and config_path.is_dir()):
		print(f"ERR: no valid config_path given")
		print(f"DBG: given config path: {para_section[config_naming.local_config_path]}")
		return False
	if not (repro_path.exists() and repro_path.is_dir()):
		print(f"ERR: no valid local git repository path is given")
		print(f"DBG: given git-repro path: {para_section[config_naming.local_git_repro]} was made to {repro_path}")
		return False
	## check for r/w rights on config_path and r/- rights on repro_path
	### TODO: do a proper test of this code!
	if not os.access(repro_path, os.R_OK):
		print(f"ERR: No read rights on {config_path}")
		return False
	if not os.access(config_path, os.R_OK):
		print(f"ERR: No read rights on {config_path}")
		return False
	if not os.access(config_path, os.W_OK):
		print(f"ERR: No write rights on {config_path}")
		return False
	
	

	# check ether for whitelisting or blacklistig:
	## if <whitelist> is not empty
	try:
		whitelist = json.loads(para_section.get(config_naming.whitelist))
	except:
		print(f"ERR: whitelist data is in non readable shape!")
		return False
	try:
		blacklist = json.loads(para_section.get(config_naming.blacklist))
	except:
		print(f"ERR: blacklist data is in non readable shape!")
		return False
	
	if (whitelist):
		return sync_whitelisting(para_section)
	if (blacklist):
		return sync_blacklisting(para_section)


	# All config parameters are set and valid!

	return True
	# check: if <local_config_path> and <local_git_repro> are presend in the FS and if we have r/w rights
	# check: if all files listed in <whitelist> are presend in <local_git_repro>
		# balacklists does not need to be present, ony test that the syncing file is not on the blacklist
	
	# Sync

	## git-pull/update
	# Update <local_git_repro>
	# Rollback if conflicts happend
	# give easy to resolve tips

	## start syncing (linking) files
	
	## link the (not already lined) - <instance_id> prefixed - files from <local_git_repro> to <local_config_path>
	# build list of files[potential_new_files] in <local_git_repro> that are not blacklisted and have the <instance_id> prefix
	potential_new_files = []

	## clear out the new filelist with all the files in <local_config_path> that are already linked
	# get list of files[linked_files] in <local_config_path> with prefix <instance_id>
	linked_files = []

	# Check: all [potential_new_files] that are present in <local_config_path> neads to be already linked to [potential_new_files]!
	for new in potential_new:
		if new.name in local_config.filenames and local_config.files[new.name].linkpath != "<local_git_repro>/new":
			print(f"ERROR: the File {new.name} is already presend in <local_config_path> but not linked to <local_git_repro>/new as it sould be \n\t Please resolve this conflict by ether deleting the file in your <local_config_path> or linke it properly as this app would do it.")
			continue
		


	## link new files
	# create file link from [potential_new_files] to <local_config_path> if not in [linked_files]
	for new in potentional_new_files:
		if new in linked_files:
			continue
		# create link from new to local (same filename)





	
	pass


def main(para_cfg_path:str = None) -> bool:
	
	# get the config object
	config = check_config_parameters(para_cfg_path)
	if config is None:
		return False
	
	# Start syncing
	# get first config section
	# get section as object
	for section_str in config.sections():
		config_section = config[section_str]
		sync_section(config_section)

	print(f"LOG: DONE")



if __name__ == "__main__":
	main()
