import configparser
import argparse
from pathlib import Path
import json
import re
import os
import sys
from sys import exc_info
from space_exceptions import *
from dataclasses import dataclass

# logger.debug, info, warning, error, critical
from loguru import logger

# Local Section syncing Class
import Section_Sync



# Configuration Key-Value default pairs
##      [labor-orca] # Labor Space Orca profile Section
##      instance_name       = "LAB"
##      local_config_path   = "~/.config/OrcaSlicer/"
##      git_local_repro     = "~/git/Labor3D_Orca/"
##      file_blacklist      = []
##      file_whitelist       = []



def check_cfg_file(para_cfg_path:str) -> configparser.ConfigParser:
	
	"""Checks if the given path to a configuration (*.cfg) file is valid and if the file has minimal one section.

	Args:
		para_cfg_path (str): path to the file

	Raises:
		FileNotFoundError: If the path is no file, or does not exists.
		ConfigurationError: If no section is found in the config file.

	Returns:
		configparser.ConfigParser: A configuration object of the cfg-file
	"""	
	# Check and get config file Path
	logger.debug("Testing if (given) config file exists")
	config_path = Path(para_cfg_path)
	if not config_path.is_file():
		logger.exception(f"Path to config-file does not exists: {config_path}")
		raise FileNotFoundError(f"{config_path}")

	logger.info(f"found and accept config file: {config_path.absolute()}")

	config = configparser.ConfigParser()
	config.read(config_path)

	# Check for space sections
	if len(config.sections()) < 1:
		logger.error(f"Config file has no section, must have one or more.")
		raise ConfigurationError(f"Config-file does not even hold one section.")
	
	return config #configparser.ConfigParser()
 
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


def main(para_cfg_path:str) -> bool:
	
	path = para_cfg_path
	# get the config object
	try:
		config = check_cfg_file(para_cfg_path)
		logger.info(f"Configuration loaded successfully from: -{path}- ")
	except FileNotFoundError as e:
		logger.error(f"File not Found: {e}")
		return False
	except ConfigurationError as e:
		logger.error(f"bad Configuration: {e}")
		return False
	except e:
		logger.error(f"Unexpected Error occurred: {e}")
		return False
	
	
	# Start syncing
	# get first config section
	# get section as object
	skipped_section_strs = []
	failed_section_strs = []

	logger.debug(f"start syncing sections: {config.sections()}")
	for section_str in config.sections():
		try:
			working_section = Section_Sync(config[section_str])
		except Exception as e:
			logger.error(f"Unexpected Exception occurs: see: {e}")
			logger.warning(f"Skipped section {section_str}")
			skipped_section_strs.append(section_str)
			continue
		if not working_section:
			logger.warning(f"got no object for {section_str}, continue with the next")
			skipped_section_strs.append(section_str)
			continue
		try:
			logger.debug(f"Start syncing section: {section_str}")
			working_section.sync()
		except Exception as e:
			logger.error(f"while syncing: see: {e}")
			logger.warning(f"Section {section_str} did not properly synced, see the error above!")
			failed_section_strs.append(section_str)
			continue
	# DONE!
	if len(skipped_section_strs) > 0:
		logger.warning(f"Syncing has finished, but with {len(skipped_section_strs)} skipped sections!")
	if len(failed_section_strs) > 0:
		logger.error(f"Syncing has finished, but with {len(skipped_section_strs)} failed sections!")
	logger.info(f"DONE")



if __name__ == "__main__":
	# First parse CLI Parameters:
	# Set up parser
	parser = argparse.ArgumentParser(description="A tool to handel diverse Space-Device Configs like 3D-Printer or Laser-CNC configurations for your Software.")
	parser.add_argument(
		"--cfg_path", "-f", 
		type=str, 
		default="config.cfg", 
		help="Path to the configuration file (default: 'config.cfg')"
	)
	args = parser.parse_args()

	# Start the main code
	main(args.cfg_path)

