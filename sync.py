import configparser
from pathlib import Path

# Configuration Key-Value default pairs
##      [labor-orca] # Labor Space Orca profile Section
##      instance_name       = "LAB"
##      local_config_path   = "/home/luke/.config/OrcaSlicer/"
##      git_local_repro     = "/home/luke/git/Labor3D_Orca/"
##      file_blacklist      = []
##      file_whitelist       = []

class config_naming:
	instance_id = "instance_name"
	local_config_path = "local_config_path"
	local_git_prepro = "git_local_repro"
	blacklist = "file_blacklist"
	whitelist = "file_whitelist"

def check_config_parameters(para_cfg_path:str = None) -> configparser.ConfigParser:
	default_str_cfg_path = "config.cfg"

	# Check and get config file Path
	cfg_path = 0
	if para_cfg_path is None or para_cfg_path == "":
		cfg_path = Path(default_str_cfg_path)
		if not cfg_path.is_file():
			print(f"ERR: no Path for Config-file is given, and the default path {default_str_cfg_path} is no file")
			return None
	else:
		cfg_path = Path(para_cfg_path)
		if not cfg_path.is_file():
			print(f"ERR: given Cinfig file path -{para_cfg_path}- is not available or no file")
			return None
	print(f"LOG: Use cfgfile: {cfg_path.absolute()}")

	config = configparser.ConfigParser()
	config.read(cfg_path)

	# Check for space sections
	if len(config.sections()) < 1:
		print("ERR: no Space-section is found, check your config")
		return None
	
	# go throu each space section and perferm a sychronisation
	spaces = config.sections()
	print(f"vLOG: use spaces: {spaces}")
	for space in spaces:
		sect = config[space]
		print(sect["git_local_repro"])
		# todo: execute function for syncronisation on the particular section. all datas are stored in the section variables.

	return config
 
def sync_whitelisting(section:configparser.SectionProxy) -> bool:
	# Perform the "sync" based on the <whitelist>
	pass

def sync_section(para_section:configparser.SectionProxy) -> bool:
	# read & check all pathes is the section
	# check for no deadlocks in whithe-blacklists

	# get list of keys for the section

	# ckeck: if all keys from <config_nameing> are present
	# check: if <local_config_path> and <local_git_repro> are presend in the FS and if we have r/w rights
	# check: if all files listed in <whitelist> are presend in <local_git_repro>
		# balacklists does not need to be present, ony test that the syncing file is not on the blacklist
	
	# Sync

	## git-pull/update
	# Update <local_git_repro>
	# Rollback if confickts happends
	# give easy to resolfe tipps

	## if <whitelist> is not empty
	return sync_whitelisting(para_section)

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
		sec = config[section_str]
		sync_section(sec)




if __name__ == "__main__":
	main()
